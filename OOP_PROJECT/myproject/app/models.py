from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    """Custom user model with role-based access control"""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('staff', 'Staff/Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    department = models.CharField(max_length=100, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
    
    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="customuser",
    )
    
    def __str__(self):
        return f"{self.username} ({self.role})"

class Survey(models.Model):
    """Survey model for creating and managing surveys"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_surveys')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    target_audience = models.CharField(max_length=50, default='all')  # 'students', 'instructors', 'all'
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    @property
    def response_count(self):
        return self.responses.count()
    
    @property
    def completion_rate(self):
        if self.target_audience == 'all':
            total_users = CustomUser.objects.count()
        elif self.target_audience == 'students':
            total_users = CustomUser.objects.filter(role='student').count()
        else:
            total_users = CustomUser.objects.filter(role='instructor').count()
        
        if total_users == 0:
            return 0
        return (self.response_count / total_users) * 100

class Question(models.Model):
    """Question model for survey questions"""
    QUESTION_TYPES = [
        ('text', 'Text Response'),
        ('multiple_choice', 'Multiple Choice'),
        ('rating', 'Rating Scale'),
        ('yes_no', 'Yes/No'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='text')
    is_required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.survey.title} - {self.question_text[:50]}..."

class Choice(models.Model):
    """Choice model for multiple choice questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.choice_text

class Response(models.Model):
    """Response model for survey responses"""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    respondent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='responses')
    submitted_at = models.DateTimeField(auto_now_add=True)
    completion_time = models.DurationField(null=True, blank=True)  # Time taken to complete survey
    
    def __str__(self):
        return f"{self.respondent.username} - {self.survey.title}"

class Answer(models.Model):
    """Answer model for individual question answers"""
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    rating_value = models.IntegerField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    def __str__(self):
        return f"{self.response} - {self.question.question_text[:30]}..."

class Notification(models.Model):
    """Notification model for smart notifications"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True, blank=True)
    target_users = models.ManyToManyField(CustomUser, related_name='notifications')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.priority.upper()}: {self.title}"

class AnalyticsReport(models.Model):
    """Analytics report model for generated reports"""
    REPORT_TYPES = [
        ('pdf', 'PDF Report'),
        ('excel', 'Excel Data'),
        ('csv', 'CSV Data'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=500)  # Path to generated file
    download_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.report_type} - {self.survey.title}"

class QRCode(models.Model):
    """QR Code model for survey access"""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='qr_codes')
    code_value = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    scan_count = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"QR for {self.survey.title}"

# Signal handlers for automatic notifications
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Response)
def create_completion_notification(sender, instance, created, **kwargs):
    """Create notification when survey completion rate is high"""
    if created:
        survey = instance.survey
        completion_rate = survey.completion_rate
        
        if completion_rate >= 90 and not Notification.objects.filter(
            survey=survey, 
            title__contains="High Response Rate"
        ).exists():
            Notification.objects.create(
                title="High Response Rate",
                message=f"Survey '{survey.title}' has reached {completion_rate:.1f}% completion rate. Consider closing the survey.",
                priority='high',
                survey=survey
            )

@receiver(post_save, sender=Answer)
def create_critical_feedback_notification(sender, instance, created, **kwargs):
    """Create notification for critical feedback"""
    if created and instance.rating_value and instance.rating_value <= 2:
        survey = instance.response.survey
        
        # Check if we already have a critical feedback notification for this survey today
        today = timezone.now().date()
        existing_notification = Notification.objects.filter(
            survey=survey,
            title__contains="Critical Feedback",
            created_at__date=today
        ).exists()
        
        if not existing_notification:
            Notification.objects.create(
                title="Critical Feedback Detected",
                message=f"Multiple low ratings detected in '{survey.title}'. Review recommended.",
                priority='critical',
                survey=survey
            )