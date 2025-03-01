from django.urls import path
from . import api


urlpatterns = [
    path('users/', api.CustomUserAPIList.as_view(), name='users'),
    path('post_user/', api.CustomUserAPIPost.as_view(), name='post_user'),
    path('user/me', api.CustomUserAPIUpdate.as_view(), name='update'),
    path('delete_user/<int:pk>/', api.CustomUserAPIDestroy.as_view(), name='delete_user'),
]