from django import forms
from django.contrib.auth import get_user_model

from hive_activities.activities.models import Activity

User=get_user_model()


class IndividualActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 1}),
        }


class LoggedInUserActivityForm(IndividualActivityForm):

    class Meta:
        model = Activity
        fields = ['project', 'title', 'description', 'assigned_to', 'status', 'priority', 'due_date']

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class UpdateActivityForm(IndividualActivityForm):
    class Meta:
        model = Activity
        fields = ['project', 'title', 'description', 'priority', 'due_date']

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }