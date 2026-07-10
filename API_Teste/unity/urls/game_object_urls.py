from django.urls import path

from unity.viewsets.game_object_view.create_game_object_view import CreateGameObjectView
from unity.viewsets.game_object_view.delete_game_object_view import DeleteGameObjectView
from unity.viewsets.game_object_view.get_game_object_view import GetGameObjectView
from unity.viewsets.game_object_view.list_game_objects_view import ListGameObjectView
from unity.viewsets.game_object_view.update_game_object_view import UpdateGameObjectView
from unity.viewsets.game_object_view.get_complete_game_object_view import GetCompleteGameObjectView
from unity.viewsets.game_object_view.list_complete_game_object_view import ListCompleteGameObjectsView


urlpatterns = [
    path('game_object/register/', CreateGameObjectView.as_view(), name='game_object_create_route'),
    path('game_object/list/', ListGameObjectView.as_view(), name='game_object_list_route'),
    path('game_object/list/complete/', ListCompleteGameObjectsView.as_view(), name='list_complete_game_object_route'),
    path('game_object/update/<str:game_object_id>/', UpdateGameObjectView.as_view(), name='game_object_update_route'),
    path('game_object/delete/<str:game_object_id>/', DeleteGameObjectView.as_view(), name='game_object_delete_route'),
    path('game_object/complete/<str:game_object_id>/', GetCompleteGameObjectView.as_view(), name='get_complete_game_object_view'),
    path('game_object/<str:game_object_id>/', GetGameObjectView.as_view(), name='game_object_get_route'),
]