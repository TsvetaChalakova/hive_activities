from django.urls import path, URLPattern
from hive_activities.activities import views
from hive_activities.activities.views import ActivityDetailView, ActivityUpdateView, individual_view, \
    TeamDashboardView, SearchResultsView, custom_404_view
from hive_activities.notes.views import NoteCreateView

app_name = 'activities'
urlpatterns = [
    path('', views.home, name='home'),
    path('404/', custom_404_view),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('individual_dashboard/', individual_view, name='individual_dashboard'),
    path('activities/update-activity-status/<int:pk>/', views.update_activity_status, name='update_activity_status'),
    path('team_dashboard/', TeamDashboardView.as_view(), name='team_dashboard'),
    path('activity/create/', views.ActivityCreateView.as_view(), name='activity_create'),
    path('activities/<int:pk>/', ActivityDetailView.as_view(), name='activity_detail'),
    path('activity/<int:pk>/edit/', ActivityUpdateView.as_view(), name='activity_edit'),
    path('activity/<int:pk>/notes/create/', NoteCreateView.as_view(), name='note_create'),
]
