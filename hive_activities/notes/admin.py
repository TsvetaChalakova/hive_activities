from django.contrib import admin
from hive_activities.notes.models import Note


@admin.register(Note)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('content', 'created_by', 'created_at', 'content_preview')

    list_filter = ('created_at', 'created_by', 'is_closed')

    search_fields = ('content', 'created_by__profile__get_full_name', 'activity__title')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Content'

