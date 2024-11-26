from django.contrib.auth import get_user_model
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

    # def get_queryset(self):
    #     return Project.objects.filter(team_members=self.request.user)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/02_add_project_form.html'
    success_url = reverse_lazy('projects:project_list')

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
        context['activities'] = self.object.activities.all()
        context['memberships'] = self.object.team_members.all()
        return context


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/02_add_project_form.html'

    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    success_url = reverse_lazy('projects:project_list')


class ProjectMembersView(LoginRequiredMixin, ListView):
    template_name = 'projects/04_project_members.html'
    context_object_name = 'memberships'

    def get_queryset(self):
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return ProjectMembership.objects.filter(
            project=self.project
        ).select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        context['is_manager'] = self.project.manager == self.request.user
        return context


class AddProjectMemberView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ProjectMembership
    form_class = ProjectMembershipForm
    template_name = 'projects/05_add_project_member.html'

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
        return reverse_lazy('projects:project_members', kwargs={'pk': self.project.pk})
