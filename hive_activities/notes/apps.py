from django.apps import AppConfig


class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hive_activities.notes'

    def ready(self):
        import hive_activities.notes.signals
