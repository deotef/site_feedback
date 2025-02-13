from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('roles/', views.ShowRoles, name='role')
]