from .models import Answer
from django import forms
from .models import Upvote

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }