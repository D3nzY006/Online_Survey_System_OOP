from django.urls import path
from .views import survey_list, take_survey, multiple_surveys, survey_instructions, thank_you

urlpatterns = [
    path('', survey_list, name='survey_list'),
    path('multiple/', multiple_surveys, name='multiple_surveys'),
    path('instructions/<int:survey_id>/', survey_instructions, name='survey_instructions'),
    path('take/<int:survey_id>/', take_survey, name='take_survey'),
    path('thank-you/', thank_you, name='thank_you'),
]
