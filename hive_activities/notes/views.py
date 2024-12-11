from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from hive_activities.activities.models import Activity
from hive_activities.notes.forms import NoteForm
from hive_activities.notes.models import Note


class NoteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_add.html'

    def test_func(self):
        return not self.request.user.is_viewer()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity'] = self.activity

        return context

    def dispatch(self, request, *args, **kwargs):
        self.activity = get_object_or_404(Activity, pk=self.kwargs['pk'])

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.activity = self.activity
        form.instance.created_by = self.request.user

        response = super().form_valid(form)
        post_save.send(sender=Note, instance=form.instance, created=True, request=self.request)

        return response

    def get_success_url(self):
        return reverse('activities:activity_detail', kwargs={'pk': self.activity.pk})

