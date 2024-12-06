from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from hive_activities.activities.models import Activity
from hive_activities.projects.views import ProjectUpdateView


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_link', 'assigned_to', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__profile__get_full_name')
    ordering = ('-created_at', )
    raw_id_fields = ('assigned_to', 'project')
    actions = ['mark_as_complted', 'mark_as_in_progress']

    def project_link(self, obj):
        url = reverse(ProjectUpdateView, args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', url, obj.project.title)
    project_link.short_description = 'Project'

    def mark_as_completed(self, request, queryset):
        queryset.update(status='COMPLETED')
    mark_as_completed.short_description = "Mark selected tasks as done"

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='IN_PROGRESS')
    mark_as_in_progress.short_description = "Mark selected tasks as in progress"
