# backend/celery.py
import os
from celery import Celery

# Define o módulo de configurações do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Lê as configurações do Django que começam com 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente as tarefas em todos os apps instalados
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')