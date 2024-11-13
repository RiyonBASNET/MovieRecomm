from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    # Rating range input (using NumberInput widget)
    rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
        required=True,
        label="Rating (1-5)"
    )
    
    # Review text area (using Textarea widget)
    review_text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your review here...'}),
        required=True,
        label="Review"
    )
    class Meta:
        model = Review
        fields = [ 'rating','review_text']
