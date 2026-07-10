from django.urls import path

from unity.viewsets.game_object_rotation_view.create_game_object_rotation_view import CreateGameObjectRotationView
from unity.viewsets.game_object_rotation_view.delete_game_object_rotation_view import DeleteGameObjectRotationView
from unity.viewsets.game_object_rotation_view.get_game_object_rotation_view import GetGameObjectRotationView
from unity.viewsets.game_object_rotation_view.list_game_object_rotation_view import ListGameObjectRotationView
from unity.viewsets.game_object_rotation_view.update_game_object_rotation_view import UpdateGameObjectRotationView


urlpatterns = [
    path('game_object_rotation/register/', CreateGameObjectRotationView.as_view(), name='game_object_rotation_create_route'),
    path('game_object_rotation/list/', ListGameObjectRotationView.as_view(), name='game_object_rotation_list_route'),
    path('game_object_rotation/update/<int:game_object_rotation_id>/', UpdateGameObjectRotationView.as_view(), name='game_object_rotation_update_route'),
    path('game_object_rotation/delete/<int:game_object_rotation_id>/', DeleteGameObjectRotationView.as_view(), name='game_object_rotation_delete_route'),
    path('game_object_rotation/<int:game_object_rotation_id>/', GetGameObjectRotationView.as_view(), name='game_object_rotation_get_route'),
]