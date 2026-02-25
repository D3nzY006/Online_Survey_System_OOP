from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Count, Avg, Q
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.http import FileResponse
import json
import io
from datetime import datetime, timedelta

from .models import CustomUser, Survey, Question, Choice, Response, Answer, Notification, AnalyticsReport, QRCode
from .forms import SurveyForm, QuestionForm, ChoiceForm

# Create your views here.

def home(request):
    """Landing page with role-based entry points"""
    return render(request, 'home.html')

def log_in(request):
    """Login view with role-based redirection"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user role
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'instructor':
                return redirect('instructor_dashboard')
            elif user.role == 'staff':
                return redirect('analytics')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'log_in.html')

def log_out(request):
    """Logout view"""
    logout(request)
    return redirect('home')

@login_required
def student_dashboard(request):
    """Student dashboard - view available surveys"""
    # Get surveys that are active and target this student's audience
    current_time = timezone.now()
    surveys = Survey.objects.filter(
        Q(status='active') | Q(status='closed'),
        start_date__lte=current_time,
        end_date__gte=current_time
    ).order_by('-created_at')
    
    # Check which surveys the student has already completed
    completed_surveys = Response.objects.filter(
        respondent=request.user
    ).values_list('survey_id', flat=True)
    
    context = {
        'surveys': surveys,
        'completed_surveys': completed_surveys,
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def instructor_dashboard(request):
    """Instructor dashboard - manage surveys and view results"""
    if request.user.role != 'instructor':
        messages.error(request, 'Access denied. Instructor access only.')
        return redirect('home')
    
    # Get surveys created by this instructor
    surveys = Survey.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Get notifications for this instructor
    notifications = Notification.objects.filter(
        target_users=request.user
    ).order_by('-created_at')[:5]
    
    # Calculate stats
    total_responses = Response.objects.filter(survey__in=surveys).count()
    active_surveys = surveys.filter(status='active').count()
    
    context = {
        'surveys': surveys,
        'notifications': notifications,
        'total_responses': total_responses,
        'active_surveys': active_surveys,
    }
    return render(request, 'instructor_dashboard.html', context)

@login_required
def staff_dashboard(request):
    """Staff dashboard - view all analytics and manage system"""
    if request.user.role != 'staff':
        messages.error(request, 'Access denied. Staff access only.')
        return redirect('home')
    
    # Get all surveys
    surveys = Survey.objects.all().order_by('-created_at')
    
    # Get all notifications
    notifications = Notification.objects.all().order_by('-created_at')[:10]
    
    # Calculate system-wide stats
    total_responses = Response.objects.count()
    total_surveys = Survey.objects.count()
    active_surveys = Survey.objects.filter(status='active').count()
    total_users = CustomUser.objects.count()
    last_update = timezone.now()
    
    context = {
        'surveys': surveys,
        'notifications': notifications,
        'total_responses': total_responses,
        'total_surveys': total_surveys,
        'active_surveys': active_surveys,
        'total_users': total_users,
        'last_update': last_update,
    }
    return render(request, 'staff_dashboard.html', context)

@login_required
def analytics(request):
    """Analytics dashboard with real-time charts"""
    if request.user.role not in ['instructor', 'staff']:
        messages.error(request, 'Access denied. Analytics access requires instructor or staff role.')
        return redirect('home')
    
    # Get surveys based on user role
    if request.user.role == 'staff':
        surveys = Survey.objects.all()
    else:
        surveys = Survey.objects.filter(created_by=request.user)
    
    # Calculate analytics data
    total_responses = Response.objects.filter(survey__in=surveys).count()
    completion_rates = []
    response_distribution = []
    
    for survey in surveys[:3]:  # Top 3 surveys
        completion_rate = survey.completion_rate
        completion_rates.append({
            'title': survey.title,
            'rate': completion_rate,
            'responses': survey.response_count
        })
        
        response_distribution.append({
            'label': survey.title,
            'value': survey.response_count
        })
    
    # Daily responses for last 7 days
    last_7_days = [timezone.now().date() - timedelta(days=i) for i in range(6, -1, -1)]
    daily_data = []
    
    for day in last_7_days:
        count = Response.objects.filter(
            survey__in=surveys,
            submitted_at__date=day
        ).count()
        daily_data.append(count)
    
    context = {
        'total_responses': total_responses,
        'completion_rates': completion_rates,
        'response_distribution': response_distribution,
        'daily_data': daily_data,
        'last_7_days': [day.strftime('%a') for day in last_7_days],
    }
    return render(request, 'analytics.html', context)

@login_required
def survey_detail(request, survey_id):
    """Survey detail page - view survey and submit responses"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    # Check if survey is active
    current_time = timezone.now()
    if survey.status != 'active' or current_time < survey.start_date or current_time > survey.end_date:
        messages.error(request, 'This survey is not currently available.')
        return redirect('home')
    
    # Check if user has already completed this survey
    if Response.objects.filter(survey=survey, respondent=request.user).exists():
        messages.info(request, 'You have already completed this survey.')
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        # Process survey submission
        start_time = request.session.get('survey_start_time')
        completion_time = None
        
        if start_time:
            start_time = datetime.fromisoformat(start_time)
            completion_time = timezone.now() - start_time
        
        # Create response
        response = Response.objects.create(
            survey=survey,
            respondent=request.user,
            completion_time=completion_time
        )
        
        # Process answers
        for question in survey.questions.all():
            question_key = f'question_{question.id}'
            
            if question.question_type == 'multiple_choice':
                choice_id = request.POST.get(question_key)
                if choice_id:
                    choice = get_object_or_404(Choice, id=choice_id, question=question)
                    Answer.objects.create(
                        response=response,
                        question=question,
                        selected_choice=choice
                    )
            elif question.question_type == 'rating':
                rating = request.POST.get(question_key)
                if rating:
                    Answer.objects.create(
                        response=response,
                        question=question,
                        rating_value=int(rating)
                    )
            else:
                answer_text = request.POST.get(question_key, '')
                if answer_text:
                    Answer.objects.create(
                        response=response,
                        question=question,
                        answer_text=answer_text
                    )
        
        messages.success(request, 'Thank you for completing the survey!')
        return redirect('student_dashboard')
    
    else:
        # Set survey start time
        request.session['survey_start_time'] = timezone.now().isoformat()
    
    context = {
        'survey': survey,
    }
    return render(request, 'survey_detail.html', context)

@login_required
def create_survey(request):
    """Create new survey (instructors only)"""
    if request.user.role != 'instructor':
        messages.error(request, 'Access denied. Survey creation requires instructor role.')
        return redirect('home')
    
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.created_by = request.user
            survey.save()
            messages.success(request, 'Survey created successfully!')
            return redirect('instructor_dashboard')
    else:
        form = SurveyForm()
    
    context = {
        'form': form,
    }
    return render(request, 'create_survey.html', context)

@login_required
def add_question(request, survey_id):
    """Add question to survey"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    if request.user.role != 'instructor' or survey.created_by != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            messages.success(request, 'Question added successfully!')
            return redirect('instructor_dashboard')
    else:
        form = QuestionForm()
    
    context = {
        'form': form,
        'survey': survey,
    }
    return render(request, 'add_question.html', context)

@login_required
def add_choice(request, question_id):
    """Add choice to multiple choice question"""
    question = get_object_or_404(Question, id=question_id)
    
    if request.user.role != 'instructor' or question.survey.created_by != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            messages.success(request, 'Choice added successfully!')
            return redirect('instructor_dashboard')
    else:
        form = ChoiceForm()
    
    context = {
        'form': form,
        'question': question,
    }
    return render(request, 'add_choice.html', context)

@login_required
def survey_results(request, survey_id):
    """View survey results and analytics"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    if request.user.role == 'student':
        messages.error(request, 'Access denied. Students cannot view survey results.')
        return redirect('home')
    
    if request.user.role == 'instructor' and survey.created_by != request.user:
        messages.error(request, 'Access denied. You can only view results for surveys you created.')
        return redirect('home')
    
    # Calculate results
    responses = survey.responses.all()
    total_responses = responses.count()
    
    results = []
    for question in survey.questions.all():
        question_data = {
            'question': question,
            'responses': [],
            'stats': {}
        }
        
        if question.question_type == 'multiple_choice':
            choices = question.choices.all()
            for choice in choices:
                count = Answer.objects.filter(
                    question=question,
                    selected_choice=choice
                ).count()
                percentage = (count / total_responses * 100) if total_responses > 0 else 0
                question_data['responses'].append({
                    'choice': choice.choice_text,
                    'count': count,
                    'percentage': percentage
                })
        
        elif question.question_type == 'rating':
            avg_rating = Answer.objects.filter(question=question).aggregate(avg=Avg('rating_value'))['avg']
            question_data['stats']['average_rating'] = avg_rating
            
            # Rating distribution
            rating_counts = []
            for rating in range(1, 6):
                count = Answer.objects.filter(question=question, rating_value=rating).count()
                percentage = (count / total_responses * 100) if total_responses > 0 else 0
                rating_counts.append({
                    'rating': rating,
                    'count': count,
                    'percentage': percentage
                })
            question_data['responses'] = rating_counts
        
        else:
            # Text responses
            text_answers = Answer.objects.filter(question=question, answer_text__isnull=False)
            question_data['responses'] = text_answers
        
        results.append(question_data)
    
    context = {
        'survey': survey,
        'total_responses': total_responses,
        'results': results,
    }
    return render(request, 'survey_results.html', context)

@login_required
def export_report(request, survey_id, report_type):
    """Export survey report"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    if request.user.role == 'student':
        messages.error(request, 'Access denied. Students cannot export reports.')
        return redirect('home')
    
    if request.user.role == 'instructor' and survey.created_by != request.user:
        messages.error(request, 'Access denied. You can only export reports for surveys you created.')
        return redirect('home')
    
    # Create analytics report record
    report = AnalyticsReport.objects.create(
        survey=survey,
        report_type=report_type,
        generated_by=request.user,
        file_path=f"/reports/{survey.id}_{report_type}_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
    )
    
    # In a real implementation, you would generate the actual file here
    # For now, we'll simulate the export
    
    messages.success(request, f'{report_type.upper()} report generated successfully!')
    return redirect('survey_results', survey_id=survey_id)

@login_required
def notifications(request):
    """View user notifications"""
    notifications = Notification.objects.filter(
        target_users=request.user
    ).order_by('-created_at')
    
    # Mark notifications as read
    notifications.filter(is_read=False).update(is_read=True)
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'notifications.html', context)

@login_required
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    notification = get_object_or_404(Notification, id=notification_id)
    
    if request.user in notification.target_users.all():
        notification.is_read = True
        notification.save()
    
    return redirect('notifications')

# API endpoints for real-time analytics
@login_required
def api_analytics_data(request):
    """API endpoint for real-time analytics data"""
    if request.user.role not in ['instructor', 'staff']:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    period = request.GET.get('period', 'today')
    
    # Get surveys based on user role
    if request.user.role == 'staff':
        surveys = Survey.objects.all()
    else:
        surveys = Survey.objects.filter(created_by=request.user)
    
    # Calculate data based on period
    if period == 'today':
        start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
    elif period == 'week':
        start_date = timezone.now() - timedelta(days=7)
        end_date = timezone.now()
    else:  # month
        start_date = timezone.now() - timedelta(days=30)
        end_date = timezone.now()
    
    # Response distribution
    response_data = []
    for survey in surveys[:5]:  # Top 5 surveys
        count = Response.objects.filter(
            survey=survey,
            submitted_at__range=[start_date, end_date]
        ).count()
        response_data.append({
            'label': survey.title,
            'value': count
        })
    
    # Daily responses
    daily_data = []
    dates = []
    
    if period == 'today':
        for hour in range(24):
            start = start_date + timedelta(hours=hour)
            end = start + timedelta(hours=1)
            count = Response.objects.filter(
                survey__in=surveys,
                submitted_at__range=[start, end]
            ).count()
            daily_data.append(count)
            dates.append(f"{hour}:00")
    else:
        # For week/month, group by day
        current = start_date
        while current <= end_date:
            next_day = current + timedelta(days=1)
            count = Response.objects.filter(
                survey__in=surveys,
                submitted_at__range=[current, next_day]
            ).count()
            daily_data.append(count)
            dates.append(current.strftime('%m/%d'))
            current = next_day
    
    data = {
        'total_responses': Response.objects.filter(
            survey__in=surveys,
            submitted_at__range=[start_date, end_date]
        ).count(),
        'response_distribution': response_data,
        'daily_data': daily_data,
        'dates': dates,
    }
    
    return JsonResponse(data)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Count, Avg, Q
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.http import FileResponse
import json
import io
from datetime import datetime, timedelta

from .models import CustomUser, Survey, Question, Choice, Response, Answer, Notification, AnalyticsReport, QRCode
from .forms import SurveyForm, QuestionForm, ChoiceForm

# Create your views here.

def home(request):
    """Landing page with role-based entry points"""
    return render(request, 'home.html')

def log_in(request):
    """Login view with role-based redirection"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user role
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'instructor':
                return redirect('instructor_dashboard')
            elif user.role == 'staff':
                return redirect('analytics')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'log_in.html')

def log_out(request):
    """Logout view"""
    logout(request)
    return redirect('home')

@login_required
def student_dashboard(request):
    """Student dashboard - view available surveys"""
    # Get surveys that are active and target this student's audience
    current_time = timezone.now()
    surveys = Survey.objects.filter(
        Q(status='active') | Q(status='closed'),
        start_date__lte=current_time,
        end_date__gte=current_time
    ).order_by('-created_at')
    
    # Check which surveys the student has already completed
    completed_surveys = Response.objects.filter(
        respondent=request.user
    ).values_list('survey_id', flat=True)
    
    context = {
        'surveys': surveys,
        'completed_surveys': completed_surveys,
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def instructor_dashboard(request):
    """Instructor dashboard - manage surveys and view results"""
    if request.user.role != 'instructor':
        messages.error(request, 'Access denied. Instructor access only.')
        return redirect('home')
    
    # Get surveys created by this instructor
    surveys = Survey.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Get notifications for this instructor
    notifications = Notification.objects.filter(
        target_users=request.user
    ).order_by('-created_at')[:5]
    
    context = {
        'surveys': surveys,
        'notifications': notifications,
    }
    return render(request, 'instructor_dashboard.html', context)

@login_required
def staff_dashboard(request):
    """Staff dashboard - view all analytics and manage system"""
    if request.user.role != 'staff':
        messages.error(request, 'Access denied. Staff access only.')
        return redirect('home')
    
    # Get all surveys
    surveys = Survey.objects.all().order_by('-created_at')
    
    # Get all notifications
    notifications = Notification.objects.all().order_by('-created_at')[:10]
    
    # Calculate system-wide stats
    total_responses = Response.objects.count()
    total_surveys = Survey.objects.count()
    active_surveys = Survey.objects.filter(status='active').count()
    
    context = {
        'surveys': surveys,
        'notifications': notifications,
        'total_responses': total_responses,
        'total_surveys': total_surveys,
        'active_surveys': active_surveys,
    }
    return render(request, 'staff_dashboard.html', context)

@login_required
def analytics(request):
    """Analytics dashboard with real-time charts"""
    if request.user.role not in ['instructor', 'staff']:
        messages.error(request, 'Access denied. Analytics access requires instructor or staff role.')
        return redirect('home')
    
    # Get surveys based on user role
    if request.user.role == 'staff':
        surveys = Survey.objects.all()
    else:
        surveys = Survey.objects.filter(created_by=request.user)
    
    # Calculate analytics data
    total_responses = Response.objects.filter(survey__in=surveys).count()
    completion_rates = []
    response_distribution = []
    
    for survey in surveys[:3]:  # Top 3 surveys
        completion_rate = survey.completion_rate
        completion_rates.append({
            'title': survey.title,
            'rate': completion_rate,
            'responses': survey.response_count
        })
        
        response_distribution.append({
            'label': survey.title,
            'value': survey.response_count
        })
    
    # Daily responses for last 7 days
    last_7_days = [timezone.now().date() - timedelta(days=i) for i in range(6, -1, -1)]
    daily_data = []
    
    for day in last_7_days:
        count = Response.objects.filter(
            survey__in=surveys,
            submitted_at__date=day
        ).count()
        daily_data.append(count)
    
    context = {
        'total_responses': total_responses,
        'completion_rates': completion_rates,
        'response_distribution': response_distribution,
        'daily_data': daily_data,
        'last_7_days': [day.strftime('%a') for day in last_7_days],
    }
    return render(request, 'analytics.html', context)

@login_required
def survey_detail(request, survey_id):
    """Survey detail page - view survey and submit responses"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    # Check if survey is active
    current_time = timezone.now()
    if survey.status != 'active' or current_time < survey.start_date or current_time > survey.end_date:
        messages.error(request, 'This survey is not currently available.')
        return redirect('home')
    
    # Check if user has already completed this survey
    if Response.objects.filter(survey=survey, respondent=request.user).exists():
        messages.info(request, 'You have already completed this survey.')
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        # Process survey submission
        start_time = request.session.get('survey_start_time')
        completion_time = None
        
        if start_time:
            start_time = datetime.fromisoformat(start_time)
            completion_time = timezone.now() - start_time
        
        # Create response
        response = Response.objects.create(
            survey=survey,
            respondent=request.user,
            completion_time=completion_time
        )
        
        # Process answers
        for question in survey.questions.all():
            question_key = f'question_{question.id}'
            
            if question.question_type == 'multiple_choice':
                choice_id = request.POST.get(question_key)
                if choice_id:
                    choice = get_object_or_404(Choice, id=choice_id, question=question)
                    Answer.objects.create(
                        response=response,
                        question=question,
                        selected_choice=choice
                    )
            elif question.question_type == 'rating':
                rating = request.POST.get(question_key)
                if rating:
                    Answer.objects.create(
                        response=response,
                        question=question,
                        rating_value=int(rating)
                    )
            else:
                answer_text = request.POST.get(question_key, '')
                if answer_text:
                    Answer.objects.create(
                        response=response,
                        question=question,
                        answer_text=answer_text
                    )
        
        messages.success(request, 'Thank you for completing the survey!')
        return redirect('student_dashboard')
    
    else:
        # Set survey start time
        request.session['survey_start_time'] = timezone.now().isoformat()
    
    context = {
        'survey': survey,
    }
    return render(request, 'survey_detail.html', context)

@login_required
def create_survey(request):
    """Create new survey (instructors only)"""
    if request.user.role != 'instructor':
        messages.error(request, 'Access denied. Survey creation requires instructor role.')
        return redirect('home')
    
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.created_by = request.user
            survey.save()
            messages.success(request, 'Survey created successfully!')
            return redirect('instructor_dashboard')
    else:
        form = SurveyForm()
    
    context = {
        'form': form,
    }
    return render(request, 'create_survey.html', context)

@login_required
def add_question(request, survey_id):
    """Add question to survey"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    if request.user.role != 'instructor' or survey.created_by != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            messages.success(request, 'Question added successfully!')
            return redirect('instructor_dashboard')
    else:
        form = QuestionForm()
    
    context = {
        'form': form,
        'survey': survey,
    }
    return render(request, 'add_question.html', context)

@login_required
def add_choice(request, question_id):
    """Add choice to multiple choice question"""
    question = get_object_or_404(Question, id=question_id)
    
    if request.user.role != 'instructor' or question.survey.created_by != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            messages.success(request, 'Choice added successfully!')
            return redirect('instructor_dashboard')
    else:
        form = ChoiceForm()
    
    context = {
        'form': form,
        'question': question,
    }
    return render(request, 'add_choice.html', context)

@login_required
def survey_results(request, survey_id):
    """View survey results and analytics"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    if request.user.role == 'student':
        messages.error(request, 'Access denied. Students cannot view survey results.')
        return redirect('home')
    
    if request.user.role == 'instructor' and survey.created_by != request.user:
        messages.error(request, 'Access denied. You can only view results for surveys you created.')
        return redirect('home')
    
    # Calculate results
    responses = survey.responses.all()
    total_responses = responses.count()
    
    results = []
    for question in survey.questions.all():
        question_data = {
            'question': question,
            'responses': [],
            'stats': {}
        }
        
        if question.question_type == 'multiple_choice':
            choices = question.choices.all()
            for choice in choices:
                count = Answer.objects.filter(
                    question=question,
                    selected_choice=choice
                ).count()
                percentage = (count / total_responses * 100) if total_responses > 0 else 0
                question_data['responses'].append({
                    'choice': choice.choice_text,
                    'count': count,
                    'percentage': percentage
                })
        
        elif question.question_type == 'rating':
            avg_rating = Answer.objects.filter(question=question).aggregate(avg=Avg('rating_value'))['avg']
            question_data['stats']['average_rating'] = avg_rating
            
            # Rating distribution
            rating_counts = []
            for rating in range(1, 6):
                count = Answer.objects.filter(question=question, rating_value=rating).count()
                percentage = (count / total_responses * 100) if total_responses > 0 else 0
                rating_counts.append({
                    'rating': rating,
                    'count': count,
                    'percentage': percentage
                })
            question_data['responses'] = rating_counts
        
        else:
            # Text responses
            text_answers = Answer.objects.filter(question=question, answer_text__isnull=False)
            question_data['responses'] = text_answers
        
        results.append(question_data)
    
    context = {
        'survey': survey,
        'total_responses': total_responses,
        'results': results,
    }
    return render(request, 'survey_results.html', context)

@login_required
def export_report(request, survey_id, report_type):
    """Export survey report"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    if request.user.role == 'student':
        messages.error(request, 'Access denied. Students cannot export reports.')
        return redirect('home')
    
    if request.user.role == 'instructor' and survey.created_by != request.user:
        messages.error(request, 'Access denied. You can only export reports for surveys you created.')
        return redirect('home')
    
    # Create analytics report record
    report = AnalyticsReport.objects.create(
        survey=survey,
        report_type=report_type,
        generated_by=request.user,
        file_path=f"/reports/{survey.id}_{report_type}_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
    )
    
    # In a real implementation, you would generate the actual file here
    # For now, we'll simulate the export
    
    messages.success(request, f'{report_type.upper()} report generated successfully!')
    return redirect('survey_results', survey_id=survey_id)

@login_required
def notifications(request):
    """View user notifications"""
    notifications = Notification.objects.filter(
        target_users=request.user
    ).order_by('-created_at')
    
    # Mark notifications as read
    notifications.filter(is_read=False).update(is_read=True)
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'notifications.html', context)

@login_required
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    notification = get_object_or_404(Notification, id=notification_id)
    
    if request.user in notification.target_users.all():
        notification.is_read = True
        notification.save()
    
    return redirect('notifications')

# API endpoints for real-time analytics
@login_required
def api_analytics_data(request):
    """API endpoint for real-time analytics data"""
    if request.user.role not in ['instructor', 'staff']:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    period = request.GET.get('period', 'today')
    
    # Get surveys based on user role
    if request.user.role == 'staff':
        surveys = Survey.objects.all()
    else:
        surveys = Survey.objects.filter(created_by=request.user)
    
    # Calculate data based on period
    if period == 'today':
        start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
    elif period == 'week':
        start_date = timezone.now() - timedelta(days=7)
        end_date = timezone.now()
    else:  # month
        start_date = timezone.now() - timedelta(days=30)
        end_date = timezone.now()
    
    # Response distribution
    response_data = []
    for survey in surveys[:5]:  # Top 5 surveys
        count = Response.objects.filter(
            survey=survey,
            submitted_at__range=[start_date, end_date]
        ).count()
        response_data.append({
            'label': survey.title,
            'value': count
        })
    
    # Daily responses
    daily_data = []
    dates = []
    
    if period == 'today':
        for hour in range(24):
            start = start_date + timedelta(hours=hour)
            end = start + timedelta(hours=1)
            count = Response.objects.filter(
                survey__in=surveys,
                submitted_at__range=[start, end]
            ).count()
            daily_data.append(count)
            dates.append(f"{hour}:00")
    else:
        # For week/month, group by day
        current = start_date
        while current <= end_date:
            next_day = current + timedelta(days=1)
            count = Response.objects.filter(
                survey__in=surveys,
                submitted_at__range=[current, next_day]
            ).count()
            daily_data.append(count)
            dates.append(current.strftime('%m/%d'))
            current = next_day
    
    data = {
        'total_responses': Response.objects.filter(
            survey__in=surveys,
            submitted_at__range=[start_date, end_date]
        ).count(),
        'response_distribution': response_data,
        'daily_data': daily_data,
        'dates': dates,
    }
    
    return JsonResponse(data)



def register(request):
    """Register view for new users"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'student')
        
        if not all([first_name, last_name, email, password]):
            messages.error(request, 'Please fill in all required fields')
            return render(request, 'register.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'register.html')
        
        username = email
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('log_in')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'register.html')
    
    return render(request, 'register.html')


   


    
    
