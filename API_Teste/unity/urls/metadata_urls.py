from django.urls import path

from unity.viewsets.metadata_view.create_metadata_view import CreateMetadataView
from unity.viewsets.metadata_view.delete_metadata_view import DeleteMetadataView
from unity.viewsets.metadata_view.get_metadata_view import GetMetadataView
from unity.viewsets.metadata_view.list_metadata_view import ListMetadataView
from unity.viewsets.metadata_view.update_metadata_view import UpdateMetadataView


urlpatterns = [
    path('metadata/register/', CreateMetadataView.as_view(), name='metadata_create_route'),
    path('metadata/list/', ListMetadataView.as_view(), name='metadata_list_route'),
    path('metadata/update/<int:layer_id>/', UpdateMetadataView.as_view(), name='metadata_update_route'),
    path('metadata/delete/<int:layer_id>/', DeleteMetadataView.as_view(), name='metadata_delete_route'),
    path('metadata/<int:layer_id>/', GetMetadataView.as_view(), name='metadata_get_route'),
]