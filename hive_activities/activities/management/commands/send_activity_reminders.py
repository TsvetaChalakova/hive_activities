from django.core.management.base import BaseCommand
from hive_activities.core.activities import send_activity_reminders


class Command(BaseCommand):
    help = 'Send email reminders for upcoming activities'

    def handle(self, *args, **kwargs):
        send_activity_reminders()
        self.stdout.write(self.style.SUCCESS('Successfully sent email reminders for upcoming activities.'))
