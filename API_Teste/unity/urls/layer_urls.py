from django.urls import path

from unity.viewsets.layer_view.create_layer_view import CreateLayerView
from unity.viewsets.layer_view.delete_layer_view import DeleteLayerView
from unity.viewsets.layer_view.get_layer_view import GetLayerView
from unity.viewsets.layer_view.list_layers_view import ListLayerView
from unity.viewsets.layer_view.update_layer_view import UpdateLayerView


urlpatterns = [
    path('layer/register/', CreateLayerView.as_view(), name='layer_create_route'),
    path('layer/list/', ListLayerView.as_view(), name='layer_list_route'),
    path('layer/update/<int:layer_id>/', UpdateLayerView.as_view(), name='layer_update_route'),
    path('layer/delete/<int:layer_id>/', DeleteLayerView.as_view(), name='layer_delete_route'),
    path('layer/<int:layer_id>/', GetLayerView.as_view(), name='layer_get_route'),
]