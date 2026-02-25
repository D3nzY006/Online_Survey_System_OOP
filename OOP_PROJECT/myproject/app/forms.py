from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Survey, Question, Choice

class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with role selection"""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('staff', 'Staff/Admin'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    department = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department (optional)'}))
    course = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course (optional)'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'department', 'course']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

class SurveyForm(forms.ModelForm):
    """Form for creating surveys"""
    class Meta:
        model = Survey
        fields = ['title', 'description', 'start_date', 'end_date', 'target_audience', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Survey Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Survey Description'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'target_audience': forms.Select(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class QuestionForm(forms.ModelForm):
    """Form for adding questions to surveys"""
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'is_required', 'order']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Question text'}),
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'is_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class ChoiceForm(forms.ModelForm):
    """Form for adding choices to multiple choice questions"""
    class Meta:
        model = Choice
        fields = ['choice_text', 'order']
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choice text'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class SurveyResponseForm(forms.Form):
    """Dynamic form for survey responses"""
    
    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.survey = survey
        
        for question in survey.questions.all():
            if question.question_type == 'text':
                self.fields[f'question_{question.id}'] = forms.CharField(
                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                    required=question.is_required,
                    label=question.question_text
                )
            elif question.question_type == 'multiple_choice':
                choices = [(choice.id, choice.choice_text) for choice in question.choices.all()]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    choices=choices,
                    required=question.is_required,
                    label=question.question_text
                )
            elif question.question_type == 'rating':
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    choices=[(i, f'{i} - {["Very Poor", "Poor", "Average", "Good", "Excellent"][i-1]}') for i in range(1, 6)],
                    required=question.is_required,
                    label=question.question_text
                )
            elif question.question_type == 'yes_no':
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    choices=[('yes', 'Yes'), ('no', 'No')],
                    required=question.is_required,
                    label=question.question_text
                )