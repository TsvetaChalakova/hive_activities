from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .forms import ActivityCreateForm, ActivityTypeChangeForm, TemporaryActivityForm
from ..core.search import SearchService
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from .models import Activity

UserModel = get_user_model()


class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activities/04_activity_list.html'
    context_object_name = 'tasks'
    paginate_by = 20

    def get_queryset(self):
        return Activity.objects.filter(assigned_to=self.request.user)


class ActivityCreateView(CreateView):
    model = Activity
    form = ActivityCreateForm


class ActivityDetailView(DetailView):
    pass


class ActivityUpdateView(UpdateView):
    pass


class ActivityDeleteView(DeleteView):
    pass


class ActivityTypeChangeView(LoginRequiredMixin, UpdateView):
    model = Activity
    form_class = ActivityTypeChangeForm
    template_name = 'activities/03_activity_type_change.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['activity'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        activity = self.get_object()
        new_parent = form.cleaned_data.get('new_parent')

        try:
            if new_parent:
                activity.change_to_child(new_parent)
                messages.success(self.request, 'Activity converted to child activity.')
            else:
                activity.change_to_parent()
                messages.success(self.request, 'Activity converted to parent activity.')
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('activities:activity_detail', kwargs={'pk': self.object.pk})
