from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, UpdateView, CreateView, TemplateView, ListView
from .forms import HiveActivitiesAuthenticationForm, ProfileEditForm, AppUserCreationForm
from .models import UserProfile, RoleRequest, UserType

UserModel = get_user_model()


class HiveLoginView(LoginView):
    template_name = 'users/01_login.html'
    redirect_authenticated_user = True
    authentication_form = HiveActivitiesAuthenticationForm
    success_url = reverse_lazy('activities:team_dashboard')

    def form_valid(self, form):
        if not form.cleaned_data.get('remember_me', False):
            self.request.session.set_expiry(0)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('Invalid email or password.'))
        return super().form_invalid(form)


class SignUpView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'users/03_signup.html'
    success_url = reverse_lazy('activities:team_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        team_member_group = Group.objects.get(name='Team Member')
        self.object.groups.add(team_member_group)
        messages.success(self.request, "Your account has been created successfully!")
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
        return reverse_lazy(
            'users:profile-detail',
            kwargs={'pk': self.object.pk},
        )


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserProfile
    template_name = 'users/06_profile_delete.html'
    success_url = reverse_lazy('activities:home')

    def test_func(self):
        profile = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
        return self.request.user == profile.user


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

        role_requests = RoleRequest.objects.filter(id__in=selected_requests)
        project_manager_group = Group.objects.get(name='Project Manager')
        team_member_group = Group.objects.get(name='Team Member')

        if action == 'approve':
            for role_request in role_requests:
                role_request.approved = True
                role_request.user.user_type = UserType.PROJECT_MANAGER
                role_request.user.save()
                role_request.user.groups.add(project_manager_group)
                role_request.user.groups.remove(team_member_group)
                role_request.save()
            messages.success(request, f"{len(role_requests)} role requests approved.")

        elif action == 'reject':
            role_requests.update(approved=False)
            messages.warning(request, f"{len(role_requests)} role requests rejected.")

        return redirect('users:pending_role_requests')

    def get_queryset(self):
        return RoleRequest.objects.filter(approved__isnull=True).select_related('user')

