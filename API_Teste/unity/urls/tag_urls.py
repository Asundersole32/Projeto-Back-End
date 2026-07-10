from django.urls import path

from unity.viewsets.tag_view.create_tag_view import CreateTagView
from unity.viewsets.tag_view.delete_tag_view import DeleteTagView
from unity.viewsets.tag_view.get_tag_view import GetTagView
from unity.viewsets.tag_view.list_tag_view import ListTagView
from unity.viewsets.tag_view.update_tag_view import UpdateTagView

urlpatterns = [
    path('tag/register/', CreateTagView.as_view(), name='tag_create_route'),
    path('tag/list/', ListTagView.as_view(), name='tag_list_route'),
    path('tag/update/<int:layer_id>/', UpdateTagView.as_view(), name='tag_update_route'),
    path('tag/delete/<int:layer_id>/', DeleteTagView.as_view(), name='tag_delete_route'),
    path('tag/<int:layer_id>/', GetTagView.as_view(), name='tag_get_route'),
]