from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('login/', views.log_in, name='log_in'),
    path('register/', views.register, name='register'),
    path('logout/', views.log_out, name='log_out'),
    
    # Dashboards
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('instructor-dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
    
    # Surveys
    path('survey/<int:survey_id>/', views.survey_detail, name='survey_detail'),
    path('create-survey/', views.create_survey, name='create_survey'),
    path('survey/<int:survey_id>/add-question/', views.add_question, name='add_question'),
    path('question/<int:question_id>/add-choice/', views.add_choice, name='add_choice'),
    path('survey/<int:survey_id>/results/', views.survey_results, name='survey_results'),
    path('survey/<int:survey_id>/export/<str:report_type>/', views.export_report, name='export_report'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notification/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # API
    path('api/analytics/', views.api_analytics_data, name='api_analytics_data'),
]
