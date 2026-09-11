"""
Views do motor de integração.

Views neste arquivo:
  - CapacidadesView          → GET  /capacidades/
  - ExecutarOperacaoView     → POST /<sistema>/<operacao>/
  - DryRunView               → POST /<sistema>/<operacao>/dry-run/
  - WebhookReceberView       → POST /webhooks/<sistema>/<evento>/
  - HistoricoIntegracaoView  → GET  /historico/
"""

import json
import logging

from django.conf import settings as django_settings
from rest_framework import status
from rest_framework.parsers import BaseParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .engine.crypto import decifrar
from .engine.engine import IntegrationEngine
from .engine.exceptions import OperacaoNaoEncontrada, SistemaBloqueado
from .engine.registry import listar_capacidades, obter_auth_webhook
from .models import (
    RegistroIntegracao,
    SistemaExterno,
    WebhookRecebido,
)
from .tasks import processar_webhook_async
from .webhooks.idempotencia import ja_processado, marcar_processado

logger = logging.getLogger(__name__)


# ============================================================================
# Capacidades
# ============================================================================

class CapacidadesView(APIView):
    """GET /capacidades/ — lista adapters, auth, transforms registrados."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(listar_capacidades())


# ============================================================================
# Execução real
# ============================================================================

class ExecutarOperacaoView(APIView):
    """
    POST /<sistema>/<operacao>/
    Body: { ...payload canônico... }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, sistema, operacao):
        try:
            resultado = IntegrationEngine().executar(sistema, operacao, request.data)
            return Response(resultado, status=status.HTTP_200_OK)
        except (OperacaoNaoEncontrada, SistemaBloqueado) as e:
            return Response({'erro': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception('Falha na execução da operação')
            return Response(
                {'erro': 'Falha na integração', 'detalhe': str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )


# ============================================================================
# Dry-run
# ============================================================================

class DryRunView(APIView):
    """
    POST /<sistema>/<operacao>/dry-run/
    Body:
        {
            "payload": { ...canônico... },
            "payload_resposta_simulado": { ...opcional... }
        }
    Query params:
        ?auth=true  → executa a strategy de auth de verdade
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, sistema, operacao):
        payload = request.data.get('payload')
        if payload is None:
            return Response(
                {'erro': 'Campo "payload" é obrigatório no body.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payload_resposta = request.data.get('payload_resposta_simulado')
        rodar_auth = request.query_params.get('auth', 'false').lower() == 'true'

        try:
            resultado = IntegrationEngine().dry_run(
                sistema_codigo=sistema,
                operacao_codigo=operacao,
                payload=payload,
                payload_resposta_simulado=payload_resposta,
                rodar_auth=rodar_auth,
            )
            http_status = (
                status.HTTP_200_OK
                if resultado.get('sucesso')
                else status.HTTP_422_UNPROCESSABLE_ENTITY
            )
            return Response(resultado, status=http_status)
        except OperacaoNaoEncontrada as e:
            return Response({'erro': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception('Erro no dry-run')
            return Response(
                {'erro': 'Erro no dry-run', 'detalhe': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ============================================================================
# Webhooks
# ============================================================================

class RawBodyParser(BaseParser):
    """Preserva o corpo bruto — obrigatório para HMAC bater."""
    media_type = '*/*'

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()


class WebhookReceberView(APIView):
    """
    POST /webhooks/<sistema>/<evento>/
    Sem autenticação DRF — valida via HMAC da strategy configurada.
    """
    authentication_classes = []
    permission_classes = []
    parser_classes = [RawBodyParser]

    def post(self, request, sistema, evento):
        sistema_obj = SistemaExterno.objects.filter(
            codigo=sistema, ativo=True, webhook_habilitado=True
        ).first()

        if not sistema_obj:
            return Response(
                {'erro': 'Sistema não encontrado ou webhook desabilitado'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 1) Resolver strategy
        try:
            strategy_cls = obter_auth_webhook(sistema_obj.webhook_auth_strategy)
        except KeyError as e:
            logger.error('Strategy de webhook não encontrada: %s', e)
            return Response(
                {'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        segredos = {
            'atual': decifrar(sistema_obj.webhook_hmac_atual_cifrado).get('segredo'),
            'anterior': (
                decifrar(sistema_obj.webhook_hmac_anterior_cifrado).get('segredo')
                if sistema_obj.webhook_hmac_anterior_cifrado
                else None
            ),
        }

        # 2) Validar assinatura
        strategy = strategy_cls(sistema_obj, segredos, sistema_obj.webhook_auth_params)

        # Modo dev — pula validação se WEBHOOK_ALLOW_UNSIGNED=True
        if getattr(django_settings, 'WEBHOOK_ALLOW_UNSIGNED', False):
            from .webhooks.base import ResultadoValidacao
            resultado = ResultadoValidacao(True, motivo='WEBHOOK_ALLOW_UNSIGNED=True')
        else:
            resultado = strategy.validar(request)

        assinatura_recebida = (
            request.headers.get(
                sistema_obj.webhook_auth_params.get('header_signature', 'X-Signature'),
                '',
            )
            or request.headers.get('X-Hub-Signature-256', '')
            or request.headers.get('Stripe-Signature', '')
        )

        # 3) Registrar ANTES de validar (auditoria de inválidos também)
        try:
            corpo_dict = json.loads(request.body.decode() or '{}')
        except Exception:
            corpo_dict = {'_raw': request.body.decode(errors='replace')}

        wh = WebhookRecebido.objects.create(
            sistema=sistema_obj,
            evento=evento,
            headers=dict(request.headers),
            corpo=corpo_dict,
            assinatura_recebida=assinatura_recebida[:255],
            assinatura_valida=resultado.valido,
            delivery_id=resultado.delivery_id or '',
            ip_origem=self._get_ip(request),
        )

        if not resultado.valido:
            logger.warning(
                'Webhook rejeitado: %s / %s — %s', sistema, evento, resultado.motivo
            )
            return Response(
                {'erro': 'Assinatura inválida', 'motivo': resultado.motivo},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 4) Idempotência
        if ja_processado(sistema_obj.codigo, resultado.delivery_id):
            logger.info(
                'Webhook duplicado ignorado: %s / %s / %s',
                sistema, evento, resultado.delivery_id,
            )
            return Response({'ok': True, 'duplicado': True}, status=status.HTTP_200_OK)

        marcar_processado(sistema_obj.codigo, resultado.delivery_id)

        # 5) Enfileirar processamento — retorna rápido
        processar_webhook_async.apply_async(args=[wh.id], queue='integracao_normal')

        return Response(
            {'ok': True, 'webhook_id': wh.id},
            status=status.HTTP_202_ACCEPTED,
        )

    @staticmethod
    def _get_ip(request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


# ============================================================================
# Histórico
# ============================================================================

class HistoricoIntegracaoView(APIView):
    """
    GET /historico/
    Query params: sistema, status (true/false), dry_run (true/false), page, page_size
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sistema = request.query_params.get('sistema')
        status_filtro = request.query_params.get('status')
        dry_run = request.query_params.get('dry_run')

        queryset = RegistroIntegracao.objects.all()

        if sistema:
            queryset = queryset.filter(sistema__codigo=sistema)
        if status_filtro is not None:
            queryset = queryset.filter(sucesso=status_filtro.lower() == 'true')
        if dry_run is not None:
            queryset = queryset.filter(dry_run=dry_run.lower() == 'true')

        try:
            page = max(int(request.query_params.get('page', 1)), 1)
            page_size = min(max(int(request.query_params.get('page_size', 50)), 1), 200)
        except ValueError:
            page, page_size = 1, 50

        start = (page - 1) * page_size
        end = start + page_size

        registros = queryset[start:end]
        data = [
            {
                'id': r.id,
                'sistema': r.sistema.codigo if r.sistema else None,
                'operacao': r.operacao_codigo,
                'direcao': r.direcao,
                'sucesso': r.sucesso,
                'dry_run': r.dry_run,
                'status_code': r.status_code,
                'duracao_ms': r.duracao_ms,
                'criado_em': r.criado_em.isoformat(),
                'erro': r.erro,
            }
            for r in registros
        ]

        return Response({
            'total': queryset.count(),
            'page': page,
            'page_size': page_size,
            'resultados': data,
        })