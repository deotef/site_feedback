from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Панель администрирования"
#admin.site.index_title = "index_title"

urlpatterns = [
    path('admin/', admin.site.urls),

    #path('survey/', include('survey.urls')),
    path('user/', include('users.urls')),
    path('api/', include('users.api_urls')),
    path("__debug__/", include("debug_toolbar.urls")),

]
