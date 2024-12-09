from django.apps import AppConfig
from django.db.models.signals import post_migrate
from hive_activities.users.signals import create_groups_and_permissions


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hive_activities.users'

    def ready(self):
        post_migrate.connect(create_groups_and_permissions, sender=self)
