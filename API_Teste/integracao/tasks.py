from __future__ import annotations
import logging
import random
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded, MaxRetriesExceededError
from django.utils import timezone

from .engine.engine import IntegrationEngine
from .engine.exceptions import classificar_erro
from .models import (
    SistemaExterno, OperacaoIntegracao,
    RegistroIntegracao, DeadLetterQueue, StatusDLQ,
)

logger = logging.getLogger(__name__)

# Configuração de retry
MAX_TENTATIVAS = 5
BACKOFF_BASE = 2          # segundos
BACKOFF_MAX = 600         # teto de 10 minutos
JITTER_MAX = 2            # segundos de aleatoriedade


def _backoff_exponencial(tentativa: int, retry_after: int | None = None) -> int:
    """
    Calcula delay exponencial com jitter.
    tentativa começa em 1 (primeira falha).
    Se o sistema externo devolveu Retry-After, respeita (com pequena folga).
    """
    if retry_after:
        return min(retry_after + random.randint(0, JITTER_MAX), BACKOFF_MAX)
    delay = min(BACKOFF_BASE * (2 ** (tentativa - 1)), BACKOFF_MAX)
    return delay + random.randint(0, JITTER_MAX)


def _resolver_fila(sistema: SistemaExterno, operacao: OperacaoIntegracao) -> str:
    """Roteia para fila conforme prioridade configurada."""
    if operacao.prioridade >= 8:
        return 'integracao_alta'
    if operacao.prioridade <= 3:
        return 'integracao_baixa'
    return 'integracao_normal'


def _enviar_para_dlq(sistema, operacao_codigo, registro_id, payload, excecao,
                     tentativas, correlation_id):
    """Persiste na DLQ para inspeção/reprocessamento manual."""
    registro = RegistroIntegracao.objects.filter(id=registro_id).first()
    DeadLetterQueue.objects.create(
        origem='INTEGRACAO',
        sistema=sistema,
        operacao_codigo=operacao_codigo,
        registro_integracao=registro,
        payload=payload,
        ultima_excecao=str(excecao),
        ultima_excecao_tipo=type(excecao).__name__,
        total_tentativas=tentativas,
        correlation_id=correlation_id,
        status=StatusDLQ.PENDENTE,
    )
    logger.error(
        'Integração %s.%s enviada para DLQ após %d tentativas. Erro: %s',
        sistema.codigo if sistema else '?', operacao_codigo, tentativas, excecao,
    )


@shared_task(
    bind=True,
    name='integracao.executar',
    max_retries=MAX_TENTATIVAS - 1,  # Celery conta retries, não tentativas
    acks_late=True,
    track_started=True,
)
def executar_integracao_async(
    self,
    sistema_codigo: str,
    operacao_codigo: str,
    payload: dict,
    correlation_id: str | None = None,
):
    """
    Task GENÉRICA — serve para qualquer operação de qualquer sistema.
    Não existe uma task por operação. O motor resolve tudo em runtime.
    """
    tentativa = self.request.retries + 1  # 1, 2, 3, ...

    try:
        resultado = IntegrationEngine().executar(
            sistema_codigo, operacao_codigo, payload, correlation_id=correlation_id,
        )
        logger.info(
            'Integração %s.%s OK (tentativa %d)',
            sistema_codigo, operacao_codigo, tentativa,
        )
        return resultado

    except SoftTimeLimitExceeded as e:
        # Nossa própria task estourou tempo antes do adapter — trata como transiente
        logger.warning('SoftTimeLimitExceeded em %s.%s', sistema_codigo, operacao_codigo)
        return _decidir_retry(
            self, e, 'transiente', tentativa, sistema_codigo, operacao_codigo,
            payload, correlation_id,
        )

    except Exception as e:
        categoria = classificar_erro(e)
        return _decidir_retry(
            self, e, categoria, tentativa, sistema_codigo, operacao_codigo,
            payload, correlation_id,
        )


def _decidir_retry(task, excecao, categoria, tentativa, sistema_codigo,
                   operacao_codigo, payload, correlation_id):
    sistema = SistemaExterno.objects.filter(codigo=sistema_codigo).first()

    if categoria == 'definitivo':
        logger.error(
            'Erro DEFINITIVO em %s.%s — sem retry. %s',
            sistema_codigo, operacao_codigo, excecao,
        )
        _enviar_para_dlq(
            sistema, operacao_codigo, None, payload, excecao,
            tentativas=tentativa, correlation_id=correlation_id,
        )
        return {
            'sucesso': False,
            'erro': str(excecao),
            'categoria': 'definitivo',
            'dlq': True,
        }

    # Transiente ou rate_limit: verifica se ainda pode retentar
    if tentativa > MAX_TENTATIVAS:
        logger.error(
            'Esgotou %d tentativas em %s.%s. Enviando para DLQ.',
            MAX_TENTATIVAS, sistema_codigo, operacao_codigo,
        )
        _enviar_para_dlq(
            sistema, operacao_codigo, None, payload, excecao,
            tentativas=tentativa, correlation_id=correlation_id,
        )
        return {
            'sucesso': False,
            'erro': str(excecao),
            'categoria': categoria,
            'dlq': True,
            'tentativas_esgotadas': True,
        }

    retry_after = getattr(excecao, 'retry_after', None)
    delay = _backoff_exponencial(tentativa, retry_after)

    logger.warning(
        'Falha transiente em %s.%s (tentativa %d/%d). Retry em %ds. Erro: %s',
        sistema_codigo, operacao_codigo, tentativa, MAX_TENTATIVAS, delay, excecao,
    )
    raise task.retry(exc=excecao, countdown=delay)


# ============================================================================
# REPROCESSAMENTO DA DLQ
# ============================================================================

@shared_task(name='integracao.reprocessar_dlq')
def reprocessar_dlq(dlq_id: int):
    """Reprocessa um item da DLQ manualmente (após correção)."""
    item = DeadLetterQueue.objects.filter(id=dlq_id, status=StatusDLQ.PENDENTE).first()
    if not item:
        return {'ok': False, 'motivo': 'Item não encontrado ou já processado'}

    item.status = StatusDLQ.REPROCESSANDO
    item.save(update_fields=['status', 'atualizado_em'])

    try:
        if item.origem == 'INTEGRACAO':
            resultado = IntegrationEngine().executar(
                item.sistema.codigo, item.operacao_codigo, item.payload,
                correlation_id=item.correlation_id,
            )
        else:
            # origem WEBHOOK — reprocessar via handler
            from .webhooks import despachar_webhook
            resultado = despachar_webhook(item.webhook_recebido_id)

        item.status = StatusDLQ.RESOLVIDO
        item.observacoes = f'Reprocessado em {timezone.now().isoformat()}'
        item.save(update_fields=['status', 'observacoes', 'atualizado_em'])
        return {'ok': True, 'resultado': resultado}

    except Exception as e:
        item.status = StatusDLQ.PENDENTE  # volta para fila
        item.ultima_excecao = str(e)
        item.ultima_excecao_tipo = type(e).__name__
        item.total_tentativas += 1
        item.save()
        logger.exception('Falha ao reprocessar DLQ #%s', dlq_id)
        return {'ok': False, 'erro': str(e)}


@shared_task(name='integracao.reprocessar_dlq_em_lote')
def reprocessar_dlq_em_lote(limite: int = 50):
    """Roda periodicamente (beat) para tentar DLQs antigas automaticamente."""
    itens = DeadLetterQueue.objects.filter(
        status=StatusDLQ.PENDENTE,
        total_tentativas__lt=3,  # limite de reprocessamentos automáticos
    ).order_by('criado_em')[:limite]

    resultados = []
    for item in itens:
        resultados.append(reprocessar_dlq.delay(item.id).id)
    return {'disparados': len(resultados), 'task_ids': resultados}

# integracao/tasks.py (adicione)

@shared_task(
    bind=True,
    name='integracao.processar_webhook',
    max_retries=3,
    acks_late=True,
)
def processar_webhook_async(self, webhook_id: int):
    from .models import WebhookRecebido, DeadLetterQueue
    from .webhooks.dispatcher import despachar_webhook

    wh = WebhookRecebido.objects.filter(id=webhook_id).first()
    if not wh:
        return {'ok': False, 'motivo': 'Webhook não encontrado'}

    if wh.processado:
        return {'ok': True, 'ja_processado': True}

    wh.processando = True
    wh.tentativas_processamento += 1
    wh.save(update_fields=['processando', 'tentativas_processamento'])

    try:
        resultado = despachar_webhook(webhook_id)
        wh.processado = True
        wh.processando = False
        wh.processado_em = timezone.now()
        wh.save(update_fields=['processado', 'processando', 'processado_em'])
        return {'ok': True, 'resultado': resultado}

    except Exception as e:
        wh.processando = False
        wh.erro = str(e)
        wh.save(update_fields=['processando', 'erro'])

        categoria = classificar_erro(e)
        if categoria == 'definitivo' or self.request.retries >= 3:
            DeadLetterQueue.objects.create(
                origem='WEBHOOK',
                sistema=wh.sistema,
                operacao_codigo=wh.evento,
                webhook_recebido=wh,
                payload=wh.corpo,
                ultima_excecao=str(e),
                ultima_excecao_tipo=type(e).__name__,
                total_tentativas=wh.tentativas_processamento,
            )
            return {'ok': False, 'erro': str(e), 'dlq': True}

        delay = _backoff_exponencial(self.request.retries + 1)
        raise self.retry(exc=e, countdown=delay)