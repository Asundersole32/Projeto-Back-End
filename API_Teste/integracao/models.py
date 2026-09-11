from django.db import models
from django.utils import timezone


# ============================================================================
# EXISTENTES (mantidos da versão anterior) — coloco aqui para referência
# ============================================================================

class TipoSistema(models.TextChoices):
    ERP = 'ERP', 'ERP'
    MES = 'MES', 'MES'
    CRM = 'CRM', 'CRM'
    WMS = 'WMS', 'WMS'
    GENERICO = 'GENERICO', 'Genérico'


class Protocolo(models.TextChoices):
    REST = 'REST', 'REST / JSON'
    SOAP = 'SOAP', 'SOAP / WSDL'
    XMLRPC = 'XMLRPC', 'XML-RPC'
    ODATA = 'ODATA', 'OData'
    GRAPHQL = 'GRAPHQL', 'GraphQL'


class TipoAuth(models.TextChoices):
    NENHUMA = 'NONE', 'Sem autenticação'
    BEARER = 'BEARER', 'Bearer Token (estático)'
    API_KEY = 'API_KEY', 'API Key (header/query)'
    BASIC = 'BASIC', 'Basic Auth'
    OAUTH2_CC = 'OAUTH2_CC', 'OAuth2 Client Credentials'
    CUSTOM = 'CUSTOM', 'Strategy customizada'


class Direcao(models.TextChoices):
    REQUEST = 'REQUEST', 'Requisição (nós → eles)'
    RESPONSE = 'RESPONSE', 'Resposta (eles → nós)'
    WEBHOOK = 'WEBHOOK', 'Webhook (entrada)'


class SistemaExterno(models.Model):
    """Qualquer ERP/MES/WMS registrado no motor."""

    codigo = models.SlugField(unique=True)
    nome = models.CharField(max_length=120)
    tipo = models.CharField(max_length=20, choices=TipoSistema.choices, default=TipoSistema.GENERICO)
    protocolo = models.CharField(max_length=20, choices=Protocolo.choices)
    base_url = models.URLField()
    ativo = models.BooleanField(default=True)

    adapter_customizado = models.CharField(max_length=120, blank=True)

    tipo_auth = models.CharField(max_length=20, choices=TipoAuth.choices, default=TipoAuth.NENHUMA)
    credenciais_cifradas = models.BinaryField(null=True, blank=True)
    auth_extra = models.JSONField(default=dict, blank=True)

    timeout_segundos = models.PositiveIntegerField(default=30)
    headers_padrao = models.JSONField(default=dict, blank=True)
    verify_ssl = models.BooleanField(default=True)

    falhas_consecutivas = models.PositiveIntegerField(default=0)
    bloqueado_ate = models.DateTimeField(null=True, blank=True)

    # ========================================================================
    # NOVOS CAMPOS — Webhook / HMAC (módulo d)
    # ========================================================================

    webhook_habilitado = models.BooleanField(default=False)

    # Segredos HMAC ficam cifrados. Guardamos DOIS para permitir rotação sem downtime.
    webhook_hmac_atual_cifrado = models.BinaryField(null=True, blank=True)
    webhook_hmac_anterior_cifrado = models.BinaryField(null=True, blank=True)

    # Strategy de validação — resolvida via registry (ver auth_webhook/)
    webhook_auth_strategy = models.CharField(
        max_length=60, blank=True, default='HMAC_SHA256',
        help_text='Chave da strategy no registry. Ex: HMAC_SHA256, GITHUB, STRIPE, HMAC_SHA1'
    )
    # Parâmetros extras da strategy (nome do header, formato do timestamp etc.)
    webhook_auth_params = models.JSONField(default=dict, blank=True)

    # Tolerância de timestamp em segundos (anti-replay)
    webhook_tolerancia_segundos = models.PositiveIntegerField(default=300)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sistema Externo'
        verbose_name_plural = 'Sistemas Externos'

    def __str__(self):
        return f'{self.codigo} ({self.tipo})'

    @property
    def esta_bloqueado(self):
        return self.bloqueado_ate and self.bloqueado_ate > timezone.now()


class OperacaoIntegracao(models.Model):
    sistema = models.ForeignKey(SistemaExterno, on_delete=models.CASCADE, related_name='operacoes')
    codigo = models.SlugField()
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)

    metodo_http = models.CharField(max_length=10, default='POST')
    caminho = models.CharField(max_length=255)
    content_type = models.CharField(max_length=80, default='application/json')

    adapter_params = models.JSONField(default=dict, blank=True)

    schema_entrada = models.JSONField(null=True, blank=True)
    schema_saida = models.JSONField(null=True, blank=True)

    ativo = models.BooleanField(default=True)

    # Prioridade para roteamento de fila Celery: 0=baixa, 5=normal, 10=alta
    prioridade = models.PositiveSmallIntegerField(default=5)

    class Meta:
        unique_together = [('sistema', 'codigo')]

    def __str__(self):
        return f'{self.sistema.codigo}.{self.codigo}'


class MapeamentoCampo(models.Model):
    operacao = models.ForeignKey(OperacaoIntegracao, on_delete=models.CASCADE, related_name='mapeamentos')
    direcao = models.CharField(max_length=10, choices=Direcao.choices)

    origem_path = models.CharField(max_length=255)
    destino_path = models.CharField(max_length=255)

    transformacoes = models.JSONField(default=list)

    valor_padrao = models.JSONField(null=True, blank=True)
    obrigatorio = models.BooleanField(default=False)

    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['operacao', 'direcao', 'ordem']


class RegistroIntegracao(models.Model):
    sistema = models.ForeignKey(SistemaExterno, on_delete=models.SET_NULL, null=True)
    operacao_codigo = models.CharField(max_length=120)
    direcao = models.CharField(max_length=10, choices=Direcao.choices)

    payload_original = models.JSONField(null=True, blank=True)
    payload_mapeado = models.JSONField(null=True, blank=True)
    resposta_bruta = models.JSONField(null=True, blank=True)
    resposta_mapeada = models.JSONField(null=True, blank=True)

    sucesso = models.BooleanField(default=False)
    status_code = models.IntegerField(null=True, blank=True)
    erro = models.TextField(blank=True)
    duracao_ms = models.IntegerField(default=0)

    correlation_id = models.UUIDField(null=True, blank=True, db_index=True)

    # ========================================================================
    # NOVO — distinguir dry-run de execução real (módulo b)
    # ========================================================================
    dry_run = models.BooleanField(default=False, db_index=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        indexes = [models.Index(fields=['sistema', 'operacao_codigo', 'criado_em'])]


class WebhookRecebido(models.Model):
    sistema = models.ForeignKey(SistemaExterno, on_delete=models.SET_NULL, null=True)
    evento = models.CharField(max_length=120)

    headers = models.JSONField(default=dict)
    corpo = models.JSONField(null=True, blank=True)

    # ========================================================================
    # NOVOS CAMPOS — HMAC / idempotência / processamento assíncrono (módulo d)
    # ========================================================================

    assinatura_recebida = models.CharField(max_length=255, blank=True)
    assinatura_valida = models.BooleanField(null=True, blank=True)

    delivery_id = models.CharField(
        max_length=200, blank=True, db_index=True,
        help_text='ID único do emissor para idempotência (X-Delivery-ID, X-Event-ID, etc.)'
    )
    ip_origem = models.GenericIPAddressField(null=True, blank=True)

    # Processamento
    processado = models.BooleanField(default=False, db_index=True)
    processando = models.BooleanField(default=False)
    tentativas_processamento = models.PositiveIntegerField(default=0)
    erro = models.TextField(blank=True)

    # Correlation para amarrar aos registros de saída disparados pelo handler
    correlation_id = models.UUIDField(null=True, blank=True, db_index=True)

    recebido_em = models.DateTimeField(auto_now_add=True, db_index=True)
    processado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-recebido_em']
        indexes = [
            models.Index(fields=['sistema', 'evento', 'recebido_em']),
            models.Index(fields=['delivery_id']),
        ]


# ============================================================================
# NOVO — Dead Letter Queue (módulo c)
# ============================================================================

class StatusDLQ(models.TextChoices):
    PENDENTE = 'PENDENTE', 'Pendente de reprocessamento'
    REPROCESSANDO = 'REPROCESSANDO', 'Reprocessando'
    RESOLVIDO = 'RESOLVIDO', 'Resolvido'
    DESCARTADO = 'DESCARTADO', 'Descartado'


class DeadLetterQueue(models.Model):
    """
    Registra execuções que esgotaram todas as tentativas de retry.
    Fica esperando inspeção manual ou reprocessamento programado.
    """

    # Origem: 'INTEGRACAO' (outbound) ou 'WEBHOOK' (inbound)
    ORIGEM_CHOICES = [
        ('INTEGRACAO', 'Integração (saída)'),
        ('WEBHOOK', 'Webhook (entrada)'),
    ]

    origem = models.CharField(max_length=20, choices=ORIGEM_CHOICES)

    sistema = models.ForeignKey(SistemaExterno, on_delete=models.SET_NULL, null=True)
    operacao_codigo = models.CharField(max_length=120, blank=True)

    # Referência ao registro original (para rastrear o que aconteceu)
    registro_integracao = models.ForeignKey(
        RegistroIntegracao, on_delete=models.SET_NULL, null=True, blank=True
    )
    webhook_recebido = models.ForeignKey(
        WebhookRecebido, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Payload original para reprocessar
    payload = models.JSONField(null=True, blank=True)

    # Última exceção capturada
    ultima_excecao = models.TextField(blank=True)
    ultima_excecao_tipo = models.CharField(max_length=120, blank=True)
    total_tentativas = models.PositiveIntegerField(default=0)

    correlation_id = models.UUIDField(null=True, blank=True, db_index=True)

    status = models.CharField(max_length=20, choices=StatusDLQ.choices, default=StatusDLQ.PENDENTE)
    observacoes = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['status', 'criado_em']),
            models.Index(fields=['origem', 'sistema']),
        ]

    def __str__(self):
        return f'DLQ #{self.id} [{self.origem}] {self.operacao_codigo or "-"} ({self.status})'