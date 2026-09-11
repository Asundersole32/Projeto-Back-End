"""
Endpoints de provisionamento.

Três views:
  - ProvisionarSistemaView    → cria/atualiza sistema + operações + mapeamentos
  - DesprovisionarSistemaView → remove sistema (cascade apaga operações/mapeamentos)
  - TemplateProvisionamentoView → devolve payload de exemplo + capacidades
"""

import logging

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .engine.crypto import cifrar
from .models import (
    SistemaExterno,
    OperacaoIntegracao,
    MapeamentoCampo,
    Direcao,
)
from .serializers_provisionamento import (
    ProvisionarPayloadSerializer,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Provisionar
# ============================================================================

class ProvisionarSistemaView(APIView):
    """
    POST /api/integracoes/provisionar/

    Query params:
        ?validate_only=true  → só valida, não grava
        ?upsert=true         → atualiza sistema existente
        ?replace=true        → apaga mapeamentos antigos e recria
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ProvisionarPayloadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'sucesso': False, 'erros': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        dados = serializer.validated_data
        sistema_data = dados['sistema']
        operacoes_data = dados.get('operacoes', [])

        validate_only = request.query_params.get('validate_only', 'false').lower() == 'true'
        upsert = request.query_params.get('upsert', 'false').lower() == 'true'
        replace = request.query_params.get('replace', 'false').lower() == 'true'

        codigo = sistema_data['codigo']
        existente = SistemaExterno.objects.filter(codigo=codigo).first()

        if existente and not upsert:
            return Response(
                {
                    'sucesso': False,
                    'erros': {
                        'sistema.codigo': [
                            f'Sistema "{codigo}" já existe. Use ?upsert=true para atualizar.'
                        ]
                    },
                },
                status=status.HTTP_409_CONFLICT,
            )

        if validate_only:
            return Response({
                'sucesso': True,
                'validate_only': True,
                'sistema_codigo': codigo,
                'operacoes': len(operacoes_data),
                'mapeamentos': sum(
                    len(op.get('mapeamentos_request', []))
                    + len(op.get('mapeamentos_response', []))
                    + len(op.get('mapeamentos_webhook', []))
                    for op in operacoes_data
                ),
                'mensagem': 'Payload válido. Nada foi gravado (validate_only=true).',
            }, status=status.HTTP_200_OK)

        try:
            with transaction.atomic():
                sistema = self._gravar_sistema(sistema_data, existente=existente)
                stats = self._gravar_operacoes(sistema, operacoes_data, replace=replace)
        except Exception as e:
            logger.exception('Falha no provisionamento de %s', codigo)
            return Response(
                {'sucesso': False, 'erros': {'_geral': [str(e)]}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({
            'sucesso': True,
            'sistema_id': sistema.id,
            'sistema_codigo': sistema.codigo,
            'criado': existente is None,
            'operacoes_criadas': stats['operacoes'],
            'mapeamentos_criados': stats['mapeamentos'],
            'avisos': [],
        }, status=status.HTTP_201_CREATED if existente is None else status.HTTP_200_OK)

    # ------------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------------

    def _gravar_sistema(self, dados: dict, existente: SistemaExterno = None):
        dados = dict(dados)  # não mutar o validated_data
        webhook = dados.pop('webhook', None) or {}
        credenciais = dados.pop('credenciais', None) or {}

        campos = dict(dados)

        if credenciais:
            campos['credenciais_cifradas'] = cifrar(credenciais)

        if webhook:
            campos['webhook_habilitado'] = webhook.get('habilitado', False)
            campos['webhook_auth_strategy'] = webhook.get('auth_strategy', 'HMAC_SHA256')
            campos['webhook_auth_params'] = webhook.get('auth_params', {})
            campos['webhook_tolerancia_segundos'] = webhook.get('tolerancia_segundos', 300)

            if webhook.get('segredo_atual'):
                campos['webhook_hmac_atual_cifrado'] = cifrar(
                    {'segredo': webhook['segredo_atual']}
                )
            if webhook.get('segredo_anterior'):
                campos['webhook_hmac_anterior_cifrado'] = cifrar(
                    {'segredo': webhook['segredo_anterior']}
                )

        if existente:
            for k, v in campos.items():
                setattr(existente, k, v)
            existente.save()
            return existente

        return SistemaExterno.objects.create(**campos)

    def _gravar_operacoes(self, sistema: SistemaExterno, operacoes: list, replace: bool):
        total_ops = 0
        total_mapeamentos = 0

        for op_data in operacoes:
            op_data = dict(op_data)
            codigo = op_data['codigo']
            mapeamentos_req = op_data.pop('mapeamentos_request', [])
            mapeamentos_resp = op_data.pop('mapeamentos_response', [])
            mapeamentos_wh = op_data.pop('mapeamentos_webhook', [])

            operacao, _criada = OperacaoIntegracao.objects.update_or_create(
                sistema=sistema,
                codigo=codigo,
                defaults=op_data,
            )

            if replace:
                MapeamentoCampo.objects.filter(operacao=operacao).delete()

            self._criar_mapeamentos(operacao, Direcao.REQUEST, mapeamentos_req)
            self._criar_mapeamentos(operacao, Direcao.RESPONSE, mapeamentos_resp)
            self._criar_mapeamentos(operacao, Direcao.WEBHOOK, mapeamentos_wh)

            total_ops += 1
            total_mapeamentos += (
                len(mapeamentos_req) + len(mapeamentos_resp) + len(mapeamentos_wh)
            )

        return {'operacoes': total_ops, 'mapeamentos': total_mapeamentos}

    def _criar_mapeamentos(self, operacao, direcao, lista):
        for i, m in enumerate(lista):
            MapeamentoCampo.objects.create(
                operacao=operacao,
                direcao=direcao,
                ordem=m.get('ordem', i),
                origem_path=m['origem_path'],
                destino_path=m['destino_path'],
                transformacoes=m.get('transformacoes', []),
                valor_padrao=m.get('valor_padrao'),
                obrigatorio=m.get('obrigatorio', False),
            )


# ============================================================================
# Desprovisionar
# ============================================================================

class DesprovisionarSistemaView(APIView):
    """
    DELETE /api/integracoes/provisionar/{codigo}/
    Remove o sistema e tudo em cascata (operações, mapeamentos).
    """
    permission_classes = [IsAdminUser]

    def delete(self, request, codigo):
        sistema = SistemaExterno.objects.filter(codigo=codigo).first()
        if not sistema:
            return Response(
                {
                    'sucesso': False,
                    'erros': {'codigo': [f'Sistema "{codigo}" não existe.']},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        nome = sistema.nome
        sistema.delete()
        return Response({
            'sucesso': True,
            'mensagem': f'Sistema "{codigo}" ({nome}) removido com todas as operações.',
        }, status=status.HTTP_200_OK)


# ============================================================================
# Template
# ============================================================================

class TemplateProvisionamentoView(APIView):
    """
    GET /api/integracoes/provisionar/template/
    Devolve um payload de exemplo e as capacidades registradas (adapters,
    auth strategies, webhook strategies, transforms). Útil para quem vai
    montar o JSON de provisionamento.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        from .engine.registry import listar_capacidades

        return Response({
            'template': {
                'sistema': {
                    'codigo': 'meu-erp-prd',
                    'nome': 'Meu ERP',
                    'tipo': 'ERP',
                    'protocolo': 'REST',
                    'base_url': 'https://erp.exemplo.com/api/v1',
                    'tipo_auth': 'BEARER',
                    'credenciais': {'token': '<token>'},
                    'auth_extra': {},
                    'headers_padrao': {},
                    'timeout_segundos': 30,
                    'verify_ssl': True,
                    'webhook': {
                        'habilitado': False,
                        'auth_strategy': 'HMAC_SHA256',
                        'auth_params': {
                            'header_signature': 'X-Signature',
                            'header_timestamp': 'X-Timestamp',
                        },
                        'segredo_atual': '<segredo-32-bytes>',
                        'tolerancia_segundos': 300,
                    },
                },
                'operacoes': [{
                    'codigo': 'exemplo_operacao',
                    'nome': 'Exemplo',
                    'descricao': '',
                    'metodo_http': 'POST',
                    'caminho': '/recurso',
                    'content_type': 'application/json',
                    'prioridade': 5,
                    'adapter_params': {},
                    'ativo': True,
                    'mapeamentos_request': [
                        {
                            'origem_path': '$.campo',
                            'destino_path': 'field',
                            'transformacoes': [],
                            'obrigatorio': False,
                        }
                    ],
                    'mapeamentos_response': [],
                    'mapeamentos_webhook': [],
                }],
            },
            'capacidades_disponiveis': listar_capacidades(),
            'query_params': {
                'validate_only': 'true|false — valida sem gravar',
                'upsert': 'true|false — atualiza se já existe',
                'replace': 'true|false — apaga mapeamentos antigos antes de recriar',
            },
        })