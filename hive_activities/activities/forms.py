from django import forms
from django.core.exceptions import ValidationError

from hive_activities.activities.models import Activity


class ActivityCreateForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'project', 'assigned_to',
                  'priority', 'due_date', 'parent']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

        if project:
            # Filter parent activity choices to only show parent activities from the same project
            self.fields['parent'].queryset = Activity.objects.filter(
                project=project,
                activity_type='PARENT'
            ).exclude(pk=self.instance.pk if self.instance.pk else None)

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')
        due_date = cleaned_data.get('due_date')

        if parent and due_date and due_date > parent.due_date:
            raise ValidationError({
                'due_date': 'Child activity due date cannot be later than parent activity due date.'
            })

        return cleaned_data


class ActivityTypeChangeForm(forms.Form):
    new_parent = forms.ModelChoiceField(
        queryset=Activity.objects.none(),
        required=False,
        empty_label="No parent (convert to parent activity)"
    )

    def __init__(self, *args, **kwargs):
        activity = kwargs.pop('activity', None)
        super().__init__(*args, **kwargs)

        if activity:
            # Filter possible parent activities
            self.fields['new_parent'].queryset = Activity.objects.filter(
                project=activity.project,
                activity_type='PARENT'
            ).exclude(
                pk=activity.pk
            ).exclude(
                pk__in=[child.pk for child in activity.get_all_children()]
            )