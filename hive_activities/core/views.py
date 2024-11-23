from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView
from hive_activities.activities.forms import TemporaryActivityForm
from hive_activities.core.search import SearchService

UserModel = get_user_model()


class LandingPageView(SuccessMessageMixin, FormView):
    template_name = 'common/02_home.html'
    form_class = TemporaryActivityForm
    success_url = reverse_lazy('landing')
    success_message = "Your activity has been created, and you'll receive a reminder email!"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ContactView(ListView):
    pass


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'common/06_search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')

        if query:
            context['query'] = query
            context['results'] = SearchService.global_search(query, self.request.user)

        return context