from django.urls import path

from users.viewsets.system_views.log_out_view import LogoutView
from users.viewsets.system_views.obtain_token_viewset import ObtainAuthToken
from users.viewsets.system_views.session_check_view import SessionCheckView


urlpatterns = [
    path('login/', ObtainAuthToken.as_view(), name='custom_obtain_auth_token'),
    path('logout/', LogoutView.as_view(), name='api_token_logout'),
    path('session-status/', SessionCheckView.as_view(), name='session-status'),
]