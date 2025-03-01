from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Surveys API",
        default_version='v1',
        description="API для управления опросами",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

admin.site.site_header = "Панель администрирования"
#admin.site.index_title = "index_title"

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),

    path("__debug__/", include("debug_toolbar.urls")),

    path('api/', include('users.api_urls')),
    path('apis/', include('survey.api_urls')),

    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
