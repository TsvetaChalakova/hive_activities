from django.urls import path
from hive_activities.projects.views import ProjectListView, ProjectCreateView, ProjectDetailView, ProjectUpdateView, \
    AddProjectMemberView, RemoveProjectMemberView

app_name = 'projects'
urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/members/add/', AddProjectMemberView.as_view(), name='add_project_member'),
    path('<int:project_pk>/remove-member/<int:pk>/', RemoveProjectMemberView.as_view(), name='remove_project_member'),
]