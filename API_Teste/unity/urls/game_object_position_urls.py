from django.urls import path

from unity.viewsets.game_object_position_view.create_game_object_position_view import CreateGameObjectPositionView
from unity.viewsets.game_object_position_view.delete_game_object_position_view import DeleteGameObjectPositionView
from unity.viewsets.game_object_position_view.get_game_object_position_view import GetGameObjectPositionView
from unity.viewsets.game_object_position_view.list_game_object_position_view import ListGameObjectsPositionView
from unity.viewsets.game_object_position_view.update_game_object_position_view import UpdateGameObjectPositionView


urlpatterns = [
    path('game_object_position/register/', CreateGameObjectPositionView.as_view(), name='game_object_position_create_route'),
    path('game_object_position/list/', ListGameObjectsPositionView.as_view(), name='game_object_position_list_route'),
    path('game_object_position/update/<int:game_object_position_id>/', UpdateGameObjectPositionView.as_view(), name='game_object_position_update_route'),
    path('game_object_position/delete/<int:game_object_position_id>/', DeleteGameObjectPositionView.as_view(), name='game_object_position_delete_route'),
    path('game_object_position/<int:game_object_position_id>/', GetGameObjectPositionView.as_view(), name='game_object_position_get_route'),
]