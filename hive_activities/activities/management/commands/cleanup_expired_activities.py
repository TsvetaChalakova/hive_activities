from django.core.management.base import BaseCommand

from hive_activities.activities.models import TemporaryActivity


class Command(BaseCommand):
    help = 'Clean up expired activities older than 7 days'

    def handle(self, *args, **kwargs):
        TemporaryActivity.cleanup_expired()
        self.stdout.write(self.style.SUCCESS('Successfully cleaned up expired activities.'))
