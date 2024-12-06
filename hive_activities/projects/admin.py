from django.contrib import admin

from hive_activities.projects.models import Project, ProjectMembership


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'manager', 'status', 'start_date', 'due_date', 'team_size')
    list_filter = ('status', 'start_date')
    search_fields = ('title', 'description', 'manager__profile__get_full_name')
    date_hierarchy = 'created_at'
    actions = ['mark_as_completed', 'mark_as_on_hold']

    def team_size(self, obj):
        return obj.team_members.count()
    team_size.short_description = 'Team Size'

    def mark_as_completed(self, request, queryset):
        queryset.update(status='COMPLETED')
    mark_as_completed.short_description = "Mark selected projects as completed"

    def mark_as_on_hold(self, request, queryset):
        queryset.update(status='ON_HOLD')
    mark_as_on_hold.short_description = "Mark selected projects as on hold"


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'joined_at')
    list_filter = ('role', 'joined_at')
    search_fields = ('user__email', 'project__title')
    date_hierarchy = 'joined_at'


