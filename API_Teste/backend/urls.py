from django.contrib import admin 
from django.urls import path, include 
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API TESTE",
        default_version='v1',
        description="API de geração de dados de teste e estudo de back-end",
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/v1/', include('users.urls.user_urls')),
    path('api/v1/', include('users.urls.system_urls')),
    path('api/v1/', include('machines.urls.seeded_data_urls')),
    path('api/v1/', include('machines.urls.machine_urls')),
    path('api/v1/', include('machines.urls.line_urls')),
    path('api/v1/', include('unity.urls.game_object_position_urls')),
    path('api/v1/', include('unity.urls.game_object_rotation_urls')),
    path('api/v1/', include('unity.urls.game_object_scale_urls')),
    path('api/v1/', include('unity.urls.game_object_transform_urls')),
    path('api/v1/', include('unity.urls.game_object_urls')),
    path('api/v1/', include('unity.urls.layer_urls')),
    path('api/v1/', include('unity.urls.metadata_urls')),
    path('api/v1/', include('unity.urls.tag_urls')),
]