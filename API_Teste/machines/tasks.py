from celery import shared_task, current_app
from datetime import datetime, timedelta
from django.core.cache import cache
from machines.services.data_generetor_service import SeededDataGenerator
from celery.result import AsyncResult
import uuid


CACHE_KEY = 'minha_tarefa_token'

@shared_task(bind=True)
def seeded_data_generator_task(self, aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id, token):
    
    current_token = cache.get(CACHE_KEY)
    if current_token != token:
        return
    
    # Valida parâmetros
    if None in [aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id]:
        return
    
    try:
        seeded_data_generator = SeededDataGenerator(
            aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id
        )
        seeded_data_generator.execute()
    except Exception as e:
        return  # Não reagenda em caso de erro
    
    # Reagenda para 60 segundos depois (sem task_id fixo)
    seeded_data_generator_task.apply_async(
        args=(aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id, token),
        eta=datetime.now() + timedelta(seconds=20)
    )

def generator_starter(aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id):
    try:
        if None in [aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id]:
            return {'error': 'Todos os IDs são obrigatórios'}
        
        novo_token = str(uuid.uuid4())
        cache.set(CACHE_KEY, novo_token)
        
        # Envia a tarefa sem task_id fixo (cada execução terá um ID único)
        result = seeded_data_generator_task.delay(
            aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id, novo_token
        )
        
        return {
            'msg': 'task iniciada',
            'task_id': result.id,
            'token': novo_token
        }
    except Exception as error:
        return {'error': str(error)}

def check_task_status(task_id=None):
    result = AsyncResult(task_id)
    return {
        'task_id': task_id,
        'status': result.status,
        'result': result.result if result.ready() else None,
        'traceback': result.traceback if result.failed() else None
    }