from django.urls import path

from survey import views

urlpatterns = [
    path('add_survey/', views.add_survey, name='add'),
    path('list/', views.list_surveys, name='list'),
]
