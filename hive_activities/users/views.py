from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, UpdateView, CreateView, TemplateView, ListView
from .forms import HiveActivitiesAuthenticationForm, ProfileEditForm, AppUserCreationForm
from .models import UserProfile, RoleRequest, UserType
from hive_activities.users.tasks import send_welcome_email


UserModel = get_user_model()


class HiveLoginView(LoginView):

    template_name = 'users/01_login.html'
    redirect_authenticated_user = True
    authentication_form = HiveActivitiesAuthenticationForm
    success_url = reverse_lazy('activities:team_dashboard')

    def form_valid(self, form):
        user = form.get_user()

        if not user.is_active:
            messages.error(
                self.request,
                "This account has been deactivated. Please contact support if you wish to reactivate it."
            )
            return self.form_invalid(form)

        if not form.cleaned_data.get('remember_me', False):
            self.request.session.set_expiry(0)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email or password.")

        return super().form_invalid(form)


class SignUpView(CreateView):

    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'users/03_signup.html'
    success_url = reverse_lazy('activities:team_dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('activities:team_dashboard')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)

        team_member_group = Group.objects.get(name='Team Member')
        self.object.groups.add(team_member_group)
        messages.success(self.request, "Your account has been created successfully!")
        profile = self.object.profile

        send_welcome_email.delay(
            self.object.email,
            profile.first_name,
            profile.last_name
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors detected.")
        return super().form_invalid(form)


def home_after_logout(request):
    return render(request, 'users/02_logout.html')


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

        return redirect('activities:team_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your profile has been successfully updated!")

        return response

    def get_success_url(self):
        return reverse_lazy('users:profile-detail', kwargs={'pk': self.object.pk})


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = UserProfile
    template_name = 'users/06_profile_delete.html'
    success_url = reverse_lazy('activities:home')

    def test_func(self):
        profile = get_object_or_404(UserProfile, pk=self.kwargs['pk'])

        return self.request.user == profile.user

    def form_valid(self, form):
        user = self.get_object().user
        user.is_active = False
        user.save()
        messages.success(self.request, "Your account has been successfully deactivated.")

        logout(self.request)

        return HttpResponseRedirect(self.success_url)


class RoleRequestView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    model = RoleRequest
    fields = ['requested_role']
    template_name = 'users/07_request_role_change.html'

    def test_func(self):
        return self.request.user.is_team_member()

    def handle_no_permission(self):
        messages.error(self.request, "Only team members can request role changes.")

        return redirect('activities:team_dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user

        if RoleRequest.objects.filter(user=self.request.user, approved__isnull=True).exists():
            messages.error(self.request, "You already have a pending request.")

            return redirect('activities:team_dashboard')

        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Your role request has been submitted.")

        return reverse_lazy('activities:team_dashboard')


class RoleRequestManagementView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = RoleRequest
    template_name = 'users/08_role_requests_management.html'
    context_object_name = 'role_requests'

    def test_func(self):
        return self.request.user.is_staff_admin()

    def post(self, request, *args, **kwargs):
        selected_requests = request.POST.getlist('selected_requests')
        action = request.POST.get('action')

        if not selected_requests:
            messages.warning(request, "No requests were selected.")
            return redirect('users:pending_role_requests')

        team_member_group = Group.objects.get(name='Team Member')
        role_requests = RoleRequest.objects.filter(id__in=selected_requests)

        if action == 'approve':
            for role_request in role_requests:
                # Convert PROJECT_MANAGER to "Project Manager", looks stupid but works
                group_name = role_request.requested_role.replace('_', ' ').title()
                new_group = Group.objects.get(name=group_name)

                role_request.approved = True
                role_request.user.user_type = role_request.requested_role
                role_request.user.groups.remove(team_member_group)
                role_request.user.groups.add(new_group)

                role_request.user.save()
                role_request.save()

            messages.success(request, f"{len(role_requests)} role requests approved.")

        elif action == 'reject':
            role_requests.update(approved=False)
            messages.warning(request, f"{len(role_requests)} role requests rejected.")

        return redirect('users:pending_role_requests')

    def get_queryset(self):
        return RoleRequest.objects.filter(approved__isnull=True).select_related('user')


class HivePasswordResetView(PasswordResetView):

    template_name = 'users/password/password_reset_form.html'
    email_template_name = 'users/password/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class HivePasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password/password_reset_done.html'


class HivePasswordResetConfirmView(PasswordResetConfirmView):

    template_name = 'users/password/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class HivePasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password/password_reset_complete.html'


class HivePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password/password_change.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your password has been successfully updated!")

        return response

    def get_success_url(self):
        return reverse_lazy('users:profile-detail', kwargs={'pk': self.request.user.profile.pk})