from django import forms

from hive_activities.projects.models import Project, ProjectMembership, User


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'due_date', 'status']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class ProjectMembershipForm(forms.ModelForm):

    class Meta:
        model = ProjectMembership
        fields = ['user', 'role']