# backend/settings.py
"""
Settings do backend.

Organização:
  A. Caminhos e ambiente
  B. Segurança
  C. Aplicações
  D. Middleware
  E. URLs e WSGI
  F. Templates
  G. Banco de dados
  H. Senhas e autenticação
  I. Internacionalização
  J. Estáticos e mídia
  K. Django REST Framework / Swagger / CORS
  L. Cache
  M. Celery (broker, filas, retry, beat)
  N. Integração — núcleo (crypto, circuit breaker, http)
  O. Integração — webhooks
  P. Logging
  Q. Sentry (opcional)
  R. Bootstrap / validações
"""

from pathlib import Path
import os

from django.core.exceptions import ImproperlyConfigured


# ============================================================================
# A. CAMINHOS E AMBIENTE
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# 'development' | 'staging' | 'production'
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'development')


def env_bool(nome: str, default: bool = False) -> bool:
    val = os.environ.get(nome)
    if val is None:
        return default
    return val.strip().lower() in ('1', 'true', 'yes', 'on')


def env_int(nome: str, default: int) -> int:
    try:
        return int(os.environ.get(nome, default))
    except (TypeError, ValueError):
        return default


# ============================================================================
# B. SEGURANÇA
# ============================================================================

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-w&psgt&t6su+s9q6a^2e07m-ow99_fp6s@@lat#w(e(srs57q#',
)

DEBUG = env_bool('DJANGO_DEBUG', default=True)

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.CustomUser'

# Ajustes endurecidos em produção (ver bloco R no final)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'


# ============================================================================
# C. APLICAÇÕES
# ============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceiros
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_yasg',
    'django_celery_beat',      # Periodic tasks (reprocessar DLQ)
    'django_celery_results',   # Resultados do Celery no banco (opcional)

    # Apps do projeto
    'users',
    'machines',
    'unity',
    'db_connector',
    'integracao',
]


# ============================================================================
# D. MIDDLEWARE
# ============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================================
# E. URLs E WSGI
# ============================================================================

ROOT_URLCONF = 'backend.urls'
WSGI_APPLICATION = 'backend.wsgi.application'
# ASGI_APPLICATION = 'backend.asgi.application'   # descomente se usar ASGI


# ============================================================================
# F. TEMPLATES
# ============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ============================================================================
# G. BANCO DE DADOS (MySQL — mantido)
# ============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'CONN_MAX_AGE': env_int('DB_CONN_MAX_AGE', 60),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'connect_timeout': 10,
        },
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================================
# H. SENHAS E AUTENTICAÇÃO
# ============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ============================================================================
# I. INTERNACIONALIZAÇÃO
# ============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ============================================================================
# J. ESTÁTICOS E MÍDIA
# ============================================================================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ============================================================================
# K. DJANGO REST FRAMEWORK / SWAGGER / CORS
# ============================================================================

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,

    # Throttling por escopo — protege endpoints da integração.
    # As views de integração declaram `throttle_scope` correspondente.
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'integracao_executar': '600/min',
        'integracao_dry_run': '120/min',
        'webhooks': '2000/min',
    },

    # Views de webhook sobrescrevem authentication_classes=[] e usam
    # RawBodyParser local. Esta flag evita AnonymousUser em runtime.
    'UNAUTHENTICATED_USER': None,
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Formato: Token seu_token_aqui",
        },
    },
}


# ============================================================================
# L. CACHE
# ============================================================================

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('CACHE_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/1'),
    },
    # Cache dedicado para idempotência de webhooks (isolado do cache geral)
    'webhooks': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get(
            'CACHE_WEBHOOK_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/2'
        ),
        'TIMEOUT': env_int('WEBHOOK_IDEMPOTENCIA_TTL_SEGUNDOS', 60 * 60 * 24 * 7),
    },
}


# ============================================================================
# M. CELERY (broker, filas, retry, beat)
# ============================================================================

# Broker/result — mantido o padrão que você já usa
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', f'redis://{REDIS_HOST}:{REDIS_PORT}/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'django-db')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# ── Confiabilidade ─────────────────────────────────────────────────────────
# ack tardio: a task só é marcada como concluída após processar.
# Se o worker morrer no meio, a task volta para a fila.
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_TRACK_STARTED = True

# ── Limites de tempo (soft < hard) ─────────────────────────────────────────
# Soft limit dispara SoftTimeLimitExceeded; hard mata o worker à força.
# Precisa ser > timeout do adapter + auth + mapper.
CELERY_TASK_TIME_LIMIT = env_int('CELERY_TASK_TIME_LIMIT', 300)          # 5 min
CELERY_TASK_SOFT_TIME_LIMIT = env_int('CELERY_TASK_SOFT_TIME_LIMIT', 240)  # 4 min

# ── Resultados ─────────────────────────────────────────────────────────────
CELERY_RESULT_EXPIRES = env_int('CELERY_RESULT_EXPIRES', 60 * 60 * 24 * 3)  # 3 dias
CELERY_RESULT_EXTENDED = True

# ── Filas dedicadas por prioridade ─────────────────────────────────────────
# Roteamento é feito por `_resolver_fila()` em integracao/tasks.py,
# baseado em OperacaoIntegracao.prioridade (0–10).
from kombu import Queue, Exchange  # noqa: E402

CELERY_TASK_QUEUES = (
    Queue('integracao_alta', Exchange('integracao'), routing_key='integracao.alta'),
    Queue('integracao_normal', Exchange('integracao'), routing_key='integracao.normal'),
    Queue('integracao_baixa', Exchange('integracao'), routing_key='integracao.baixa'),
    Queue('integracao_dlq', Exchange('integracao'), routing_key='integracao.dlq'),
    Queue('celery', Exchange('celery'), routing_key='celery'),
)
CELERY_TASK_DEFAULT_QUEUE = 'integracao_normal'
CELERY_TASK_DEFAULT_EXCHANGE = 'integracao'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'integracao.normal'

# Roteamento por nome de task (fallback do resolver dinâmico)
CELERY_TASK_ROUTES = {
    'integracao.executar': {'queue': 'integracao_normal'},
    'integracao.processar_webhook': {'queue': 'integracao_normal'},
    'integracao.reprocessar_dlq': {'queue': 'integracao_normal'},
    'integracao.reprocessar_dlq_em_lote': {'queue': 'integracao_dlq'},
}

# ── Beat ───────────────────────────────────────────────────────────────────
CELERY_BEAT_SCHEDULE = {
    'reprocessar-dlq-em-lote': {
        'task': 'integracao.reprocessar_dlq_em_lote',
        'schedule': 60 * 15,  # a cada 15 min
        'kwargs': {'limite': 50},
    },
}


# ============================================================================
# N. INTEGRAÇÃO — NÚCLEO
# ============================================================================

# Chave Fernet que cifra credenciais em banco (credenciais_cifradas e
# webhook_hmac_*_cifrado). Gerar com:
#   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
#
# ⚠️ Se perdê-la, TODAS as credenciais cadastradas tornam-se irrecuperáveis.
INTEGRACAO_SECRET_KEY = os.environ.get('INTEGRACAO_SECRET_KEY')

# ── Retry exponencial (task genérica) ──────────────────────────────────────
INTEGRACAO_RETRY_MAX_TENTATIVAS = env_int('INTEGRACAO_RETRY_MAX_TENTATIVAS', 5)
INTEGRACAO_RETRY_BACKOFF_BASE = env_int('INTEGRACAO_RETRY_BACKOFF_BASE', 2)
INTEGRACAO_RETRY_BACKOFF_MAX = env_int('INTEGRACAO_RETRY_BACKOFF_MAX', 600)
INTEGRACAO_RETRY_JITTER_MAX = env_int('INTEGRACAO_RETRY_JITTER_MAX', 2)

# ── Circuit breaker (por SistemaExterno) ───────────────────────────────────
INTEGRACAO_CIRCUIT_LIMITE_FALHAS = env_int('INTEGRACAO_CIRCUIT_LIMITE_FALHAS', 5)
INTEGRACAO_CIRCUIT_TEMPO_BLOQUEIO_MINUTOS = env_int(
    'INTEGRACAO_CIRCUIT_TEMPO_BLOQUEIO_MINUTOS', 5
)

# ── HTTP client (defaults; podem ser sobrescritos por SistemaExterno) ──────
INTEGRACAO_HTTP_DEFAULT_TIMEOUT = env_int('INTEGRACAO_HTTP_DEFAULT_TIMEOUT', 30)
INTEGRACAO_HTTP_DEFAULT_VERIFY_SSL = env_bool('INTEGRACAO_HTTP_DEFAULT_VERIFY_SSL', True)
INTEGRACAO_HTTP_RETRY_TOTAL = env_int('INTEGRACAO_HTTP_RETRY_TOTAL', 3)
INTEGRACAO_HTTP_RETRY_BACKOFF = float(os.environ.get('INTEGRACAO_HTTP_RETRY_BACKOFF', '0.5'))
INTEGRACAO_HTTP_RETRY_STATUS = [429, 500, 502, 503, 504]
INTEGRACAO_HTTP_USER_AGENT = os.environ.get(
    'INTEGRACAO_HTTP_USER_AGENT', 'IntegracaoUniversal/1.0'
)


# ============================================================================
# O. INTEGRAÇÃO — WEBHOOKS
# ============================================================================

# Mapa (sistema.evento) → caminho do handler Python.
# Suporta coringas: '*.evento' (qualquer sistema) e 'sistema.*' (qualquer evento).
WEBHOOK_HANDLERS = {
    # Exemplos:
    # 'opcenter.apontamento_concluido': 'meu_app.webhook_handlers.apontamento_concluido',
    # 'sap.nota_fiscal_emitida':        'meu_app.webhook_handlers.nf_emitida',
    # '*.ping':                         'meu_app.webhook_handlers.ping',
}

# Só use True em dev, para testar com curl sem montar HMAC.
# Em staging/produção, sempre False.
WEBHOOK_ALLOW_UNSIGNED = env_bool('WEBHOOK_ALLOW_UNSIGNED', False)

# TTL do delivery_id na chave de idempotência (usado também pelo cache 'webhooks')
WEBHOOK_IDEMPOTENCIA_TTL_SEGUNDOS = env_int(
    'WEBHOOK_IDEMPOTENCIA_TTL_SEGUNDOS', 60 * 60 * 24 * 7
)


# ============================================================================
# P. LOGGING
# ============================================================================

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# Garante que o diretório de logs exista
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'integracao': {
            'format': '[{asctime}] {levelname} {name} '
                      'sistema={sistema} operacao={operacao} '
                      'correlation_id={correlation_id} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'integracao_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'integracao',
        },
        'file_integracao': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'integracao.log'),
            'maxBytes': 20 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'file_dlq': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'dlq.log'),
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'integracao': {
            'handlers': ['integracao_console', 'file_integracao'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'integracao.engine': {
            'handlers': ['integracao_console', 'file_integracao'],
            'level': 'DEBUG' if DEBUG else LOG_LEVEL,
            'propagate': False,
        },
        'integracao.tasks': {
            'handlers': ['integracao_console', 'file_integracao', 'file_dlq'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'integracao.webhooks': {
            'handlers': ['integracao_console', 'file_integracao'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}


# ============================================================================
# Q. SENTRY (OPCIONAL)
# ============================================================================

SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
if SENTRY_DSN:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.celery import CeleryIntegration
        from sentry_sdk.integrations.redis import RedisIntegration

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()],
            environment=ENVIRONMENT,
            traces_sample_rate=float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', '0.1')),
            profiles_sample_rate=float(os.environ.get('SENTRY_PROFILES_SAMPLE_RATE', '0.1')),
            send_default_pii=False,
        )
    except ImportError:
        # sentry-sdk não instalado — apenas ignora
        pass


# ============================================================================
# R. BOOTSTRAP / VALIDAÇÕES
# ============================================================================

# INTEGRACAO_SECRET_KEY é obrigatória — sem ela o motor não decifra credenciais.
if not INTEGRACAO_SECRET_KEY:
    raise ImproperlyConfigured(
        'Defina INTEGRACAO_SECRET_KEY no ambiente. Gere com:\n'
        '  python -c "from cryptography.fernet import Fernet; '
        'print(Fernet.generate_key().decode())"'
    )

# Endurecimento em produção
if ENVIRONMENT == 'production':
    if DEBUG:
        raise ImproperlyConfigured('DEBUG=True não é permitido em produção.')

    if SECRET_KEY.startswith('django-insecure'):
        raise ImproperlyConfigured(
            'DJANGO_SECRET_KEY padrão não é permitido em produção. '
            'Defina uma chave forte em variável de ambiente.'
        )

    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True

    if WEBHOOK_ALLOW_UNSIGNED:
        raise ImproperlyConfigured(
            'WEBHOOK_ALLOW_UNSIGNED=True não é permitido em produção.'
        )

    # Em produção, remove BrowsableAPI implicitamente (só se você usar o renderer padrão)
    # REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ['rest_framework.renderers.JSONRenderer']