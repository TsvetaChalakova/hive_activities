from django.urls import path
from hive_activities.notifications import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notifications'),
    path('mark-read/<int:pk>/', views.MarkNotificationReadView.as_view(), name='mark_notification_read'),
]