from django.urls import path
from .views import survey_list, take_survey

urlpatterns = [
    path('', survey_list, name='survey_list'),
    path('take/<int:survey_id>/', take_survey, name='take_survey'),
]