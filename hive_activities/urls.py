from django.contrib import admin
from django.urls import path, include

app_name = 'hive-activities'

urlpatterns = [
    path('', include('hive_activities.activities.urls')),
    path('admin/', admin.site.urls),
    path('notifications/', include('hive_activities.notifications.urls')),
    path('projects/', include('hive_activities.projects.urls')),
    path('users/', include('hive_activities.users.urls')),

]