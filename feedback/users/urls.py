from django.urls import path, include
from . import api
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('roles/', views.ShowRoles, name='role'),
    path('profile/<int:user_id>/', views.ShowProfile, name='profile'),
    path('registration/', views.CustomUserRegistration, name='registr'),
    path('login/', views.CustomUserLogin, name='loginform'),
    path('logout/', views.logout_user, name='user_logout'),
    path('survey/', include('survey.urls')),
]