from django.urls import path

from machines.viewsets.machine_data_views.controle_seeded_data_generator_view import SeededDataGeneratorControllerView
from machines.viewsets.machine_data_views.task_check_view import TaskStatusView


urlpatterns = [
    path('seeded_data/controller/<int:aoi_id>/<int:automated_stencil_printer_id>/<int:pick_and_place_id>/<int:reflow_oven_id>/<int:spi_id>/', 
         SeededDataGeneratorControllerView.as_view(), name='seeded_data_generator_start_controller'),
    path('seeded_data/task/', TaskStatusView.as_view(), name='seeded_data_task_check_view'),
]