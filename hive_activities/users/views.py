from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import get_object_or_404
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
        return reverse_lazy('dashboard')


class HiveLogoutView(LogoutView):
    template_name = 'users/02_logout.html'
    success_url = reverse_lazy('landing')


class SignUpView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'users/03_signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Your account has been created successfully!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors detected.")
        return super().form_invalid(form)

    def get_success_url(self):
        if self.object.user_type == 'PROJECT_MANAGER':
            return reverse_lazy('dashboard')
        return super().get_success_url()


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserProfile
    template_name = 'users/profile-delete-page.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        profile = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
        return self.request.user == profile.user


class ProfileListView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'users/profile-list.html'


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'users/profile-details-page.html'


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = ProfileEditForm
    template_name = 'users/profile-edit-page.html'

    def test_func(self):
        profile = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.object.pk,
            }
        )


class AppUserCreationForm:
    pass





