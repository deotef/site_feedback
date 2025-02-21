from django.urls import path
from . import api
from . import views


urlpatterns = [
    path('roles/', views.ShowRoles, name='role'),
    path('profile/<int:user_id>/', views.ShowProfile, name='profile'),
    path('registration/', views.CustomUserRegistration, name='registration'),
    path('login/', views.CustomUserLogin, name='login'),
]