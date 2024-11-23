from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from hive_activities.projects.forms import ProjectForm
from hive_activities.projects.models import Project, ProjectMembership

User = get_user_model()


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/01_project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.filter(team_members=self.request.user)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/03_project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all()
        context['team_members'] = self.object.team_members.all()
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/02_add_project_form.html'
    success_url = reverse_lazy('project_list')

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     response = super().form_valid(form)
    #     ProjectMembership.objects.create(
    #         user=self.request.user,
    #         project=self.object,
    #         role='MANAGER'
    #     )
    #     return response


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/02_add_project_form.html'
    success_url = reverse_lazy('project_list')


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('project_list')


class ProjectMembersView(ListView):
    model = ProjectMembership
    template_name = 'projects/04_project_members.html'
    context_object_name = 'memberships'

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return ProjectMembership.objects.filter(project=project)


class AddProjectMemberView(CreateView):
    model = ProjectMembership
    fields = ['user', 'role']
    template_name = 'projects/05_add_project_member.html'
    success_url = reverse_lazy('project_members')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['pk'])
        return context


