from django.urls import path

from machines.viewsets.line_views.line_create_view import CreateLineView
from machines.viewsets.line_views.line_delete_view import DeleteLineView
from machines.viewsets.line_views.line_get_view import GetLineView
from machines.viewsets.line_views.line_list_view import ListLineView
from machines.viewsets.line_views.line_update_view import UpdateLineView


urlpatterns = [
    path('line/register/', CreateLineView.as_view(), name='create_line_view'),
    path('line/list/', ListLineView.as_view(), name='list_lines_view'),
    path('line/update/<int:line_id>/', UpdateLineView.as_view(), name='update_line_route'),
    path('line/delete/<int:line_id>/', DeleteLineView.as_view(), name='delete_line_route'),
    path('line/<int:line_id>/', GetLineView.as_view(), name='get_line_route'),
]
