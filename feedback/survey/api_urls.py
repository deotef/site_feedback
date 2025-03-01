from django.urls import path
from .api_views import *


urlpatterns = [
    path('add-surveys/', SurveyCreateView.as_view(), name='survey-create'),
    path('surveys/<int:pk>/', SurveyDetailAndSubmitAPIView.as_view(), name='survey-detail-and-submit'),
    path('surveys/answers/',SurveyListWithAnswersAPIView.as_view(), name='survey-detail-with-answers'),
#    path('surveys/answers/<int:pk>', SurveyDetailWithAnswersAPIView.as_view(), name='survey-detail-with-answers'),
    path('surveys/', UserSurveysListAPIView.as_view(), name='user-surveys-list'),
]