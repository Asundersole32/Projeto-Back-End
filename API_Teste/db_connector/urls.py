from django.urls import path
from .views import (
    ConnectView, TablesListView, TableInfoView,
    TableDataView, TableRowDetailView
)

urlpatterns = [
    path('connect/', ConnectView.as_view(), name='connect'),
    path('tables/', TablesListView.as_view(), name='tables'),
    path('tables/<str:table_name>/', TableInfoView.as_view(), name='table_info'),
    path('tables/<str:table_name>/rows/', TableDataView.as_view(), name='table_data'),
    path('tables/<str:table_name>/rows/<str:pk>/', TableRowDetailView.as_view(), name='table_row_detail'),
]