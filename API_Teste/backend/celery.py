# backend/celery.py
"""
Configuração do Celery para o backend.

IMPORTANTE — ordem de inicialização:
  `backend/__init__.py` importa este módulo no boot do Django, ANTES de
  `django.setup()` terminar. Portanto NADA aqui pode importar `models.py`
  direta ou indiretamente. A descoberta de tasks é feita por
  `autodiscover_tasks()`, que roda no momento correto (pós-setup).
"""

import os
import logging

from celery import Celery
from celery.signals import worker_ready, task_failure, task_revoked


# ============================================================================
# Configuração básica
# ============================================================================

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Lê as configurações do Django que começam com 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente as tasks em todos os apps instalados.
# Passamos explicitamente 'integracao' além do autodiscover genérico para
# garantir que a app seja varrida mesmo que o autodiscover do Django falhe.
app.autodiscover_tasks(['integracao'])


# ============================================================================
# Ajustes de confiabilidade / compatibilidade
# ============================================================================

app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_retry = True
app.conf.broker_connection_max_retries = 10
app.conf.task_ignore_result = False


# ============================================================================
# Sinais — observabilidade
# ============================================================================

logger = logging.getLogger('celery')


@worker_ready.connect
def _on_worker_ready(sender=None, **kwargs):
    """Loga no boot: confirma filas escutadas e o backend de resultado."""
    filas = getattr(sender, 'app', app).conf.task_queues or ()
    nomes = [q.name if hasattr(q, 'name') else str(q) for q in filas]

    logger.info(
        'Celery worker pronto. hostname=%s filas=%s result_backend=%s',
        getattr(sender, 'hostname', '?'),
        nomes or ['(default)'],
        app.conf.result_backend,
    )


@task_failure.connect
def _on_task_failure(sender=None, task_id=None, exception=None,
                     args=None, kwargs=None, traceback=None, einfo=None, **kw):
    """Loga falhas de task — complementar ao log interno de integracao.tasks."""
    logger.error(
        'Celery task falhou: nome=%s id=%s erro=%s args=%s kwargs=%s',
        getattr(sender, 'name', '?'),
        task_id,
        exception,
        args,
        kwargs,
        exc_info=True,
    )


@task_revoked.connect
def _on_task_revoked(sender=None, request=None, terminated=None,
                     signum=None, expired=None, **kw):
    """Task cancelada/revogada — normalmente por shutdown do worker."""
    logger.warning(
        'Celery task revogada: id=%s terminated=%s expired=%s',
        getattr(request, 'id', '?'),
        terminated,
        expired,
    )


# ============================================================================
# Task de debug — smoke test
# ============================================================================

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Uso: `celery -A backend call backend.celery.debug_task`"""
    print(f'Request: {self.request!r}')