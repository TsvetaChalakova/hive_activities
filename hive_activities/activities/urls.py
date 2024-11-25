from django.urls import path, URLPattern
from hive_activities.activities import views
from hive_activities.activities.views import ActivityDetailView, ActivityUpdateView, individual_view, \
    TeamDashboardView, ActivityStatusUpdate
from hive_activities.notes.views import NoteCreateView

app_name = 'activities'
urlpatterns = [
    path('', views.home, name='home'),
    path('individual/', individual_view, name='individual_dashboard'),
    path('team/', TeamDashboardView.as_view(), name='team_dashboard'),
    path('activity/create/', views.ActivityCreateView.as_view(), name='activity_create'),
    path('activity/<int:pk>/', ActivityDetailView.as_view(), name='activity_detail'),
    path('activity/<int:pk>/edit/', ActivityUpdateView.as_view(), name='activity_edit'),
    path('activity/<int:pk>/update-status/', ActivityStatusUpdate.as_view(), name='activity_status_update'),
    path('<int:pk>/notes/', NoteCreateView.as_view(), name='add_note'),
]
