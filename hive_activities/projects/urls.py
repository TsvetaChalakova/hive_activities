from django.urls import path

from hive_activities.activities.views import ActivityCreateView
from hive_activities.projects.views import ProjectListView, ProjectCreateView, ProjectDetailView, ProjectUpdateView, \
    ProjectDeleteView, ProjectMembersView, AddProjectMemberView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('<int:pk>/members/', ProjectMembersView.as_view(), name='project_members'),
    path('<int:pk>/members/add/', AddProjectMemberView.as_view(), name='add_project_member'),
    path('<int:pk>/activity/create/', ActivityCreateView.as_view(), name='activity_create'),
]