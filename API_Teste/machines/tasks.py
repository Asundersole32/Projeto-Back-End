from celery import shared_task
from datetime import datetime, timedelta
from django.core.cache import cache
from machines.services.data_generetor_service import SeededDataGenerator
import uuid

CACHE_KEY = 'minha_tarefa_token'

@shared_task
def seeded_data_generator_task(aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id, token):
    print(f"[TASK] Iniciando com token: {token}")
    
    current_token = cache.get(CACHE_KEY)
    if current_token != token:
        print(f"[TASK] Token inválido ({token} != {current_token}). Encerrando.")
        return
    
    seeded_data_generator = SeededDataGenerator(
        aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id
    )
    seeded_data_generator.execute()
    
    # Reagenda para 60 segundos depois
    seeded_data_generator_task.apply_async(
        args=(aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id, token),
        eta=datetime.now() + timedelta(seconds=60)
    )

def generator_starter(aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id):
    try:
        novo_token = str(uuid.uuid4())
        print(f"[STARTER] Novo token gerado: {novo_token}")
        cache.set(CACHE_KEY, novo_token)
        
        # Dispara a tarefa imediatamente
        seeded_data_generator_task.delay(
            aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id, novo_token
        )
        
        return {'msg': 'task iniciada'}
    except Exception as error:
        return {'msg': 'falha ao iniciar a task', 'error': str(error)}