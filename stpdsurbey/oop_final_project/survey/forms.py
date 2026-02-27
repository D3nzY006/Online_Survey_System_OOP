from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],  # 1 to 5 stars
        widget=forms.RadioSelect,
        label="Rate (1-5 stars)"
    )

    class Meta:
        model = Rating
        fields = ['rating']