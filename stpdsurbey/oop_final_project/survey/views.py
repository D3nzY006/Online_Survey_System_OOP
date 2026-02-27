from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Survey, Question, Rating
from .forms import RatingForm

@login_required
def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, 'survey_list.html', {'surveys': surveys})

@login_required
def take_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.all()

    if request.method == 'POST':
        for question in questions:
            form = RatingForm(request.POST, prefix=str(question.id))
            if form.is_valid():
                rating_value = form.cleaned_data['rating']
                Rating.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'rating': rating_value}
                )
        return redirect('survey_list')
    else:
        forms = {question.id: RatingForm(prefix=str(question.id)) for question in questions}
        return render(request, 'take_survey.html', {'survey': survey, 'questions': questions, 'forms': forms})
