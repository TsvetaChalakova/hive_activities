from django.urls import path, URLPattern
from hive_activities.activities import views
from hive_activities.notes.views import NoteCreateView

urlpatterns = [

    path('', views.ActivityListView.as_view(), name='activities_list'),
    path('create/', views.ActivityCreateView.as_view(), name='activity_create'),
    path('<int:pk>/', views.ActivityDetailView.as_view(), name='activity_detail'),
    path('<int:pk>/edit/', views.ActivityUpdateView.as_view(), name='activity_edit'),
    path('<int:pk>/delete/', views.ActivityDeleteView.as_view(), name='activity_delete'),
    path('<int:pk>/notes/', NoteCreateView.as_view(), name='add_comment'),
    path('<int:pk>/attachments/', AttachmentCreateView.as_view(), name='add_attachment'),
    path('<int:pk>/time-sheets/create/', TimeSheetCreateView.as_view(), name='timesheet_create'),
]