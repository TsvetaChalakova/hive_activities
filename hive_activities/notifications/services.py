from django.urls import reverse
from .models import Notification
from .tasks import send_notification_email


class NotificationService:
    @staticmethod
    def create_note_notification(note, team_members):
        activity_title = note.activity.title
        project_name = note.activity.project.title
        author_name = note.created_by.profile.get_full_name()

        for member in team_members:
            if member == note.created_by:
                continue

            notification = Notification.objects.create(
                recipient=member,
                note=note,
            )

            subject = f"New note in {project_name}"
            message = (
                f"{author_name} added a note to activity '{activity_title}'\n\n"
                f"Note content: {note.content}\n\n"
                f"View activity in the platform."
            )

            send_notification_email.delay(
                subject=subject,
                message=message,
                recipient_email=member.email
            )
