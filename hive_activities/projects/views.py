from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from hive_activities.projects.forms import ProjectForm, ProjectMembershipForm
from hive_activities.projects.models import Project, ProjectMembership

User = get_user_model()


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/01_project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.filter(team_members=self.request.user)


class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/02_add_project_form.html'
    success_url = reverse_lazy('projects:project_list')

    def test_func(self):
        return self.request.user.is_project_manager()

    def form_valid(self, form):
        form.instance.manager = self.request.user
        response = super().form_valid(form)
        ProjectMembership.objects.create(
            project=self.object,
            user=self.request.user,
            role='MANAGER'
        )
        return response


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/03_project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        memberships = self.object.memberships.select_related('user')
        memberships_paginator = Paginator(memberships, 5)
        memberships_page_number = self.request.GET.get('memberships_page', 1)

        try:
            context['memberships'] = memberships_paginator.get_page(memberships_page_number)
        except Exception:
            raise Http404("Memberships page not found.")

        activities = self.object.activities.all()
        activities_paginator = Paginator(activities, 10)
        activities_page_number = self.request.GET.get('activities_page', 1)

        try:
            context['activities'] = activities_paginator.get_page(activities_page_number)
        except Exception:
            raise Http404("Activities page not found.")

        return context


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/02_add_project_form.html'

    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.object.pk})


class AddProjectMemberView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ProjectMembership
    form_class = ProjectMembershipForm
    template_name = 'projects/04_add_project_member.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.project.manager == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        existing_members = self.project.team_members.all()
        form.fields['user'].queryset = User.objects.exclude(
            id__in=existing_members.values_list('id', flat=True)
        )
        return form

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.project.pk})


class RemoveProjectMemberView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProjectMembership
    template_name = 'projects/05_remove_project_member.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        self.membership = get_object_or_404(ProjectMembership, pk=self.kwargs['pk'], project=self.project)
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.project.manager == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        context['membership'] = self.membership
        return context

    def get_object(self, queryset=None):
        return self.membership

    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.project.pk})