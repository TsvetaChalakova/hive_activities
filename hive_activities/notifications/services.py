from django.conf import settings

from .models import Notification
from .tasks import send_notification_email


class NotificationService:
    @staticmethod
    def create_note_notification(note, team_members):

        activity_title = note.activity.title
        project_name = note.activity.project.name
        author_name = note.author.get_full_name()

        for member in team_members:
            if member == note.author:
                continue

            notification = Notification.objects.create(
                recipient=member,
                note=note,
            )

            subject = f"New note in {project_name}"
            message = (
                f"{author_name} added a note to activity '{activity_title}'\n\n"
                f"Note content: {note.content}\n\n"
                f"View activity: {settings.BASE_URL}/activities/{note.activity.id}/"
            )

            send_notification_email.delay(
                subject=subject,
                message=message,
                recipient_email=member.email
            )