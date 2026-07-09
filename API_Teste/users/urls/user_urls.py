from django.urls import path

from users.viewsets.user_views.create_use_view import CreateUserView
from users.viewsets.user_views.delete_user_view import DeleteUserView
from users.viewsets.user_views.get_user_view import GetUserView
from users.viewsets.user_views.list_user_view import UserListView
from users.viewsets.user_views.update_user_view import UpdateUserView


urlpatterns = [
    path('user/register/', CreateUserView.as_view(), name='create_user_route'),
    path('user/list/', UserListView.as_view(), name='list_users_route'),
    path('user/update/<str:uid>/', UpdateUserView.as_view(), name='update_user_route'),
    path('user/delete/<str:uid>/', DeleteUserView.as_view(), name='delete_user_route'),
    path('user/<str:uid>/', GetUserView.as_view(), name='get_user_route'),
]