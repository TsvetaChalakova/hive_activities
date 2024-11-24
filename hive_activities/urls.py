from django.urls import path, include

from hive_activities.activities.views import ActivityListView
from hive_activities.core.views import LandingPageView, ContactView

app_name = 'hive-activities'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('dashboard/', ActivityListView.as_view(), name='dashboard'),
    path('users/', include('hive_activities.users.urls')),
    path('projects/', include('hive_activities.projects.urls')),
    path('notifications/', include('hive_activities.notifications.urls')),

    # path('api/tasks/update-status/', views.UpdateTaskStatusView.as_view(), name='update_task_status'),
    # path('api/projects/update-status/', views.UpdateProjectStatusView.as_view(), name='update_project_status'),
    # path('api/search/', views.SearchView.as_view(), name='search'),
]