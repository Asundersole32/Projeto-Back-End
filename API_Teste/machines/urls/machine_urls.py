from django.urls import path

from machines.viewsets.machine_views.machine_create_view import CreateMachineView
from machines.viewsets.machine_views.machine_delete_view import DeleteMachineView
from machines.viewsets.machine_views.machine_get_views import GetMachineView
from machines.viewsets.machine_views.machine_list_view import MachineListView
from machines.viewsets.machine_views.machine_update_view import UpdateMachineView


urlpatterns = [
    path('machine/register/', CreateMachineView.as_view(), name='create_machine_route'),
    path('machine/list/', MachineListView.as_view(), name='list_machines_route'),
    path('machine/update/<int:machine_id>/', UpdateMachineView.as_view(), name='update_machine_route'),
    path('machine/delete/<int:machine_id>/', DeleteMachineView.as_view(), name='delete_machine_route'),
    path('machine/<int:machine_id>/', GetMachineView.as_view(), name='get_machine_route'),
]
