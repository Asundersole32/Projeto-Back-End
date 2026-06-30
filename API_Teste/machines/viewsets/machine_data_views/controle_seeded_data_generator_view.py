from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from celery import current_app

from machines.tasks import generator_starter

import uuid


class SeededDataGeneratorControllerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id):
        try:
            task_exc = generator_starter(aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id)
            return Response({'msg': 'Geração de dados ativada',
                            'parametros': {
                                'aoi_id': aoi_id,
                                'automated_stencil_printer_id': automated_stencil_printer_id,
                                'pick_and_place_id': pick_and_place_id,
                                'reflow_oven_id': reflow_oven_id,
                                'spi_id': spi_id
                            },
                            'task_exec_msg': task_exc}, status=status.HTTP_200_OK)
        
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)

