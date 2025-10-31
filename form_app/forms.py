from django import forms
from .models import IntervieweeForm, Feedback

class IntervieweeFormForm(forms.ModelForm):
    class Meta:
        model = IntervieweeForm
        fields = ['name', 'qualification', 'address', 'designation', 'skills', 'mobile_no', 'email', 'resume', 'reference']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }

