from django import forms
from django.contrib.auth import get_user_model
from hive_activities.activities.models import Activity

User = get_user_model()


class IndividualActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'status', 'priority', 'due_date']

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 1}),
        }


class LoggedInUserActivityForm(IndividualActivityForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].empty_label = None
        self.fields['project'].empty_label = None

    class Meta:
        model = Activity
        fields = ['project', 'title', 'description', 'assigned_to', 'status', 'priority', 'due_date']

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }



