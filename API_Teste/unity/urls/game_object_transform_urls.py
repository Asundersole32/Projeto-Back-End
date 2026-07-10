from django.urls import path

from unity.viewsets.game_object_transform_view.create_game_object_transform_view import CreateGameObjectTransformView
from unity.viewsets.game_object_transform_view.delete_game_object_transform_view import DeleteGameObjectTransformView
from unity.viewsets.game_object_transform_view.get_game_object_transform_view import GetGameObjectTransformView
from unity.viewsets.game_object_transform_view.list_game_object_transform_view import ListGameObjectTransformView
from unity.viewsets.game_object_transform_view.update_game_object_transform_view import UpdateGameObjectTransformView


urlpatterns = [
    path('game_object_transform/register/', CreateGameObjectTransformView.as_view(), name='game_object_transform_create_route'),
    path('game_object_transform/list/', ListGameObjectTransformView.as_view(), name='game_object_transform_list_route'),
    path('game_object_transform/update/<int:game_object_transform_id>/', UpdateGameObjectTransformView.as_view(), name='game_object_transform_update_route'),
    path('game_object_transform/delete/<int:game_object_transform_id>/', DeleteGameObjectTransformView.as_view(), name='game_object_transform_delete_route'),
    path('game_object_transform/<int:game_object_transform_id>/', GetGameObjectTransformView.as_view(), name='game_object_transform_get_route'),
]