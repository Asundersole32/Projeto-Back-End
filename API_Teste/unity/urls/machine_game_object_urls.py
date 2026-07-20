from django.urls import path

from unity.viewsets.machine_game_object_view.create_machine_game_object_view import CreateMachineGameObjectView
from unity.viewsets.machine_game_object_view.delete_machine_game_object_view import DeleteMachineGameObjectView
from unity.viewsets.machine_game_object_view.get_machine_game_object_view import GetMachineGameObjectView
from unity.viewsets.machine_game_object_view.list_machine_game_object_view import ListMachineGameObjectView
from unity.viewsets.machine_game_object_view.update_machine_game_object_view import UpdateMachineGameObjectView


urlpatterns = [
    path('machine_game_object/register/', CreateMachineGameObjectView.as_view(), name='machine_game_object_create_route'),
    path('machine_game_object/list/', ListMachineGameObjectView.as_view(), name='machine_game_object_list_route'),
    path('machine_game_object/update/<int:machine_game_object_id>/', UpdateMachineGameObjectView.as_view(), name='machine_game_object_update_route'),
    path('machine_game_object/delete/<int:machine_game_object_id>/', DeleteMachineGameObjectView.as_view(), name='machine_game_object_delete_route'),
    path('machine_game_object/<int:machine_game_object_id>/', GetMachineGameObjectView.as_view(), name='machine_game_object_get_route'),
]