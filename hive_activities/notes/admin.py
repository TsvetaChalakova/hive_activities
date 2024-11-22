# from django.contrib import admin
#
# from hive_activities.notes.models import Note
#
#
# @admin.register(Note)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('task', 'author', 'created_at', 'content_preview')
#     list_filter = ('created_at', 'author')
#     search_fields = ('content', 'author__email', 'task__title')
#
#     def content_preview(self, obj):
#         return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
#     content_preview.short_description = 'Content'
#
