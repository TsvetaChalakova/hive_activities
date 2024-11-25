from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, UpdateView, CreateView

from .forms import HiveAuthenticationForm, ProfileEditForm, AppUserCreationForm
from .models import UserProfile

UserModel = get_user_model()


class HiveLoginView(LoginView):
    template_name = 'users/01_login.html'
    redirect_authenticated_user = True
    authentication_form = HiveAuthenticationForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me', False)
        if remember_me is not None and not remember_me:
            self.request.session.set_expiry(0)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('Invalid email or password.'))
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('activities:team_dashboard')


class SignUpView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'users/03_signup.html'
    success_url = reverse_lazy('activities:team_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Your account has been created successfully!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors detected.")
        return super().form_invalid(form)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'users/04_profile_details.html'

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['projects'] = user.projects.count()
        context['activities'] = user.assigned_activities.count()
        context['notifications'] = user.notifications.count()
        return context


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = ProfileEditForm
    template_name = 'users/05_profile_edit.html'

    def test_func(self):
        return self.request.user == self.get_object().user

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to edit this profile.")
        return redirect('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your profile has been successfully updated!")
        return response

    def get_success_url(self):
        return reverse_lazy(
            'users:profile-detail',
            kwargs={'pk': self.object.pk},
        )


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserProfile
    template_name = 'users/06_profile_delete.html'
    success_url = reverse_lazy('landing')

    def test_func(self):
        profile = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
        return self.request.user == profile.user





