# integracao/webhooks/dispatcher.py
import logging
from importlib import import_module
from django.conf import settings

logger = logging.getLogger(__name__)


# Mapa configurável: (sistema_codigo, evento) → caminho do handler.
# Pode vir de settings (WEBHOOK_HANDLERS) ou de banco, conforme preferir.
def _resolver_handler(sistema_codigo: str, evento: str):
    mapa = getattr(settings, 'WEBHOOK_HANDLERS', {})
    caminho = (
        mapa.get(f'{sistema_codigo}.{evento}')
        or mapa.get(f'*.{evento}')       # handler genérico por evento
        or mapa.get(f'{sistema_codigo}.*')  # handler único por sistema
    )
    if not caminho:
        return None
    modulo, funcao = caminho.rsplit('.', 1)
    return getattr(import_module(modulo), funcao)


def despachar_webhook(webhook_id: int):
    """
    Aplica mapeamento WEBHOOK (se houver) e chama o handler registrado.
    Se não houver handler, apenas marca como processado (auditoria).
    """
    from ..models import WebhookRecebido, MapeamentoCampo, OperacaoIntegracao, Direcao
    from ..engine.mapper import mapear

    wh = WebhookRecebido.objects.get(id=webhook_id)
    if not wh.sistema:
        return {'ok': False, 'motivo': 'Webhook sem sistema associado'}

    # Aplicar mapeamento WEBHOOK, se a operação do mesmo nome existir
    operacao = OperacaoIntegracao.objects.filter(
        sistema=wh.sistema, codigo=wh.evento
    ).first()

    payload_canonico = wh.corpo
    if operacao:
        mapeamentos = list(MapeamentoCampo.objects.filter(
            operacao=operacao, direcao=Direcao.WEBHOOK
        ))
        if mapeamentos:
            payload_canonico = mapear(wh.corpo, mapeamentos)

    handler = _resolver_handler(wh.sistema.codigo, wh.evento)
    if not handler:
        logger.info('Webhook %s/%s sem handler — apenas auditado.',
                    wh.sistema.codigo, wh.evento)
        return {'ok': True, 'sem_handler': True, 'payload_canonico': payload_canonico}

    return handler(webhook=wh, payload=payload_canonico)