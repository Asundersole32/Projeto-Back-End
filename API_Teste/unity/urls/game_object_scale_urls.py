from django.urls import path

from unity.viewsets.game_object_scale_view.create_game_object_scale_view import CreateGameObjectScaleView
from unity.viewsets.game_object_scale_view.list_game_object_scale_view import ListGameObjectScaleView
from unity.viewsets.game_object_scale_view.delete_game_object_scale_view import DeleteGameObjectScaleView
from unity.viewsets.game_object_scale_view.get_game_object_scale_view import GetGameObjectScaleView
from unity.viewsets.game_object_scale_view.update_game_object_scale_view import UpdateGameObjectScaleView


urlpatterns = [
    path('game_object_scale/register/', CreateGameObjectScaleView.as_view(), name='game_object_scale_create_route'),
    path('game_object_scale/list/', ListGameObjectScaleView.as_view(), name='game_object_scale_list_route'),
    path('game_object_scale/update/<int:game_object_scale_id>/', UpdateGameObjectScaleView.as_view(), name='game_object_scale_update_route'),
    path('game_object_scale/delete/<int:game_object_scale_id>/', DeleteGameObjectScaleView.as_view(), name='game_object_scale_delete_route'),
    path('game_object_scale/<int:game_object_scale_id>/', GetGameObjectScaleView.as_view(), name='game_object_scale_get_route'),
]