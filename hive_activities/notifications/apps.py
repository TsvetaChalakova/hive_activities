from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hive_activities.notifications'

    def ready(self):
        import hive_activities.notifications.signals
