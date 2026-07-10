from django.urls import path

from unity.viewsets.game_object_view.create_game_object_view import CreateGameObjectView
from unity.viewsets.game_object_view.delete_game_object_view import DeleteGameObjectView
from unity.viewsets.game_object_view.get_game_object_view import GetGameObjectView
from unity.viewsets.game_object_view.list_game_objects_view import ListGameObjectView
from unity.viewsets.game_object_view.update_game_object_view import UpdateGameObjectView


urlpatterns = [
    path('game_object/register/', CreateGameObjectView.as_view(), name='game_object_create_route'),
    path('game_object/list/', ListGameObjectView.as_view(), name='game_object_list_route'),
    path('game_object/update/<int:game_object_id>/', UpdateGameObjectView.as_view(), name='game_object_update_route'),
    path('game_object/delete/<int:game_object_id>/', DeleteGameObjectView.as_view(), name='game_object_delete_route'),
    path('game_object/<int:game_object_id>/', GetGameObjectView.as_view(), name='game_object_get_route'),
]