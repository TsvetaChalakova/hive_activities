from django.contrib import admin
from hive_activities.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = ('recipient', 'note', 'created_at')

    search_fields = ('recipient__email', 'note__activity__title')
