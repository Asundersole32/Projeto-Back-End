# integracao/webhooks/idempotencia.py
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

TTL_SEGUNDOS = 60 * 60 * 24 * 7  # 7 dias


def ja_processado(sistema_codigo: str, delivery_id: str) -> bool:
    if not delivery_id:
        return False
    chave = f'webhook:{sistema_codigo}:{delivery_id}'
    # cache.add é atômico: retorna False se já existia
    return not cache.add(chave, '1', timeout=TTL_SEGUNDOS)


def marcar_processado(sistema_codigo: str, delivery_id: str):
    if not delivery_id:
        return
    cache.set(f'webhook:{sistema_codigo}:{delivery_id}', '1', timeout=TTL_SEGUNDOS)