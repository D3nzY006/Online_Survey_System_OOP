from django.contrib import admin
from .models import Survey, Question, Rating

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 10  # Allows adding 10 questions at once

class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question)
admin.site.register(Rating)