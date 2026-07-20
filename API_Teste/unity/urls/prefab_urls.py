from django.urls import path

from unity.viewsets.prefab_view.create_prefab_view import CreatePrefabView
from unity.viewsets.prefab_view.delete_prefab_view import DeletePrefabView
from unity.viewsets.prefab_view.get_prefab_view import GetPrefabView
from unity.viewsets.prefab_view.list_prefab_view import ListPrefabView
from unity.viewsets.prefab_view.update_prefab_view import UpdatePrefabView


urlpatterns = [
    path('prefab/register/', CreatePrefabView.as_view(), name='prefab_create_route'),
    path('prefab/list/', ListPrefabView.as_view(), name='prefab_list_route'),
    path('prefab/update/<int:layer_id>/', UpdatePrefabView.as_view(), name='prefab_update_route'),
    path('prefab/delete/<int:layer_id>/', DeletePrefabView.as_view(), name='prefab_delete_route'),
    path('prefab/<int:layer_id>/', GetPrefabView.as_view(), name='prefab_get_route'),
]