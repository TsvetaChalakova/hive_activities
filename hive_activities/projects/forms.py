from django import forms

from hive_activities.projects.models import Project, ProjectMembership, User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'manager', 'priority', 'start_date', 'due_date']
        widgets = {
            'manager': forms.HiddenInput(),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control'
            })
        }
        labels = {
            'title': 'Project Title',
            'priority': 'Project Priority',
            'description': 'Project Description'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['manager'].initial = user

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')

        if start_date and due_date and start_date > due_date:
            raise forms.ValidationError("Start date cannot be after due date.")
        return cleaned_data


class ProjectMembershipForm(forms.ModelForm):
    class Meta:
        model = ProjectMembership
        fields = ['user', 'role']

    def __init__(self, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if project:
            # Exclude users already in the project
            existing_members = project.team_members.all()
            self.fields['user'].queryset = User.objects.exclude(
                id__in=existing_members.values_list('id', flat=True)
            )