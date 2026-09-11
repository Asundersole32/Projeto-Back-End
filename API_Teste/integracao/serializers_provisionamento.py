from rest_framework import serializers

from .models import (
    SistemaExterno, OperacaoIntegracao, MapeamentoCampo,
    TipoSistema, Protocolo, TipoAuth,
)


# ============================================================================
# Mapeamento
# ============================================================================

class TransformacaoSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=60)
    params = serializers.DictField(required=False, default=dict)

    def validate_nome(self, value):
        from .engine.registry import listar_capacidades
        disponiveis = listar_capacidades()['transforms']
        if value not in disponiveis:
            raise serializers.ValidationError(
                f'Transform "{value}" não registrada. Disponíveis: {disponiveis}'
            )
        return value


class MapeamentoCampoSerializer(serializers.Serializer):
    origem_path = serializers.CharField(max_length=255)
    destino_path = serializers.CharField(max_length=255)
    transformacoes = TransformacaoSerializer(many=True, required=False, default=list)
    valor_padrao = serializers.JSONField(required=False, allow_null=True, default=None)
    obrigatorio = serializers.BooleanField(required=False, default=False)
    ordem = serializers.IntegerField(required=False, default=0)

    def validate_origem_path(self, value):
        # Valida o JSONPath se ele começar com $
        if value.startswith('$'):
            try:
                from jsonpath_ng.ext import parse
                parse(value)
            except Exception as e:
                raise serializers.ValidationError(f'JSONPath inválido: {e}')
        return value


# ============================================================================
# Operação
# ============================================================================

class OperacaoIntegracaoSerializer(serializers.Serializer):
    codigo = serializers.SlugField(max_length=100)
    nome = serializers.CharField(max_length=120)
    descricao = serializers.CharField(required=False, allow_blank=True, default='')
    metodo_http = serializers.ChoiceField(
        choices=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'], default='POST'
    )
    caminho = serializers.CharField(max_length=255)
    content_type = serializers.CharField(max_length=80, default='application/json')
    prioridade = serializers.IntegerField(min_value=0, max_value=10, default=5)
    adapter_params = serializers.JSONField(required=False, default=dict)
    ativo = serializers.BooleanField(default=True)

    mapeamentos_request = MapeamentoCampoSerializer(many=True, required=False, default=list)
    mapeamentos_response = MapeamentoCampoSerializer(many=True, required=False, default=list)
    mapeamentos_webhook = MapeamentoCampoSerializer(many=True, required=False, default=list)


# ============================================================================
# Webhook do sistema
# ============================================================================

class WebhookConfigSerializer(serializers.Serializer):
    habilitado = serializers.BooleanField(default=False)
    auth_strategy = serializers.CharField(max_length=60, default='HMAC_SHA256')
    auth_params = serializers.JSONField(required=False, default=dict)
    segredo_atual = serializers.CharField(
        required=False, allow_blank=True, write_only=True,
        help_text='Segredo HMAC. Cifrado ao salvar. Não retornado em GETs.'
    )
    segredo_anterior = serializers.CharField(
        required=False, allow_blank=True, write_only=True,
        help_text='Usado na rotação de segredo. Opcional.'
    )
    tolerancia_segundos = serializers.IntegerField(min_value=0, default=300)

    def validate_auth_strategy(self, value):
        from .engine.registry import listar_capacidades
        disponiveis = listar_capacidades()['auth_webhook']
        if value not in disponiveis:
            raise serializers.ValidationError(
                f'Strategy "{value}" não registrada. Disponíveis: {disponiveis}'
            )
        return value


# ============================================================================
# Sistema (com operações aninhadas)
# ============================================================================

class ProvisionarSistemaSerializer(serializers.Serializer):
    codigo = serializers.SlugField(max_length=80)
    nome = serializers.CharField(max_length=120)
    tipo = serializers.ChoiceField(choices=TipoSistema.choices, default=TipoSistema.GENERICO)
    protocolo = serializers.ChoiceField(choices=Protocolo.choices)
    base_url = serializers.URLField()
    ativo = serializers.BooleanField(default=True)

    adapter_customizado = serializers.CharField(
        required=False, allow_blank=True, default=''
    )

    tipo_auth = serializers.ChoiceField(choices=TipoAuth.choices, default=TipoAuth.NENHUMA)
    credenciais = serializers.JSONField(
        required=False, default=dict, write_only=True,
        help_text='Dict de credenciais. Cifrado ao salvar.'
    )
    auth_extra = serializers.JSONField(required=False, default=dict)

    timeout_segundos = serializers.IntegerField(min_value=1, max_value=600, default=30)
    verify_ssl = serializers.BooleanField(default=True)
    headers_padrao = serializers.JSONField(required=False, default=dict)

    webhook = WebhookConfigSerializer(required=False)

    def validate(self, data):
        # Se auth não é NENHUMA, exige credenciais
        if data.get('tipo_auth') != TipoAuth.NENHUMA and not data.get('credenciais'):
            raise serializers.ValidationError({
                'credenciais': f'Obrigatório quando tipo_auth != NENHUMA.'
            })
        # Se webhook habilitado, exige strategy registrada + segredo na criação
        wh = data.get('webhook') or {}
        if wh.get('habilitado') and not wh.get('segredo_atual'):
            raise serializers.ValidationError({
                'webhook.segredo_atual': 'Obrigatório quando webhook.habilitado=True.'
            })
        return data


class ProvisionarPayloadSerializer(serializers.Serializer):
    sistema = ProvisionarSistemaSerializer()
    operacoes = OperacaoIntegracaoSerializer(many=True, required=False, default=list)