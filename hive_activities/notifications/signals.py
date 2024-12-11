from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from hive_activities.notes.models import Note
from hive_activities.notifications.models import Notification
from hive_activities.notifications.tasks import send_note_email_notification


@receiver(post_save, sender=Note)
def create_notification(sender, instance, created, **kwargs):

    if created:

        project = instance.activity.project
        team_members = project.team_members.all()

        for member in team_members:

            if member != instance.created_by:

                try:
                    context = {
                        'recipient': member,
                        'note': instance,
                        'activity': instance.activity,
                        'project': project,
                        'created_by': instance.created_by
                    }

                    message = render_to_string(
                        'notifications/email/note_notification_subject.txt',
                        context
                    ).strip()

                    notification, created = Notification.objects.get_or_create(
                        recipient=member,
                        note=instance,
                        defaults={'message': message}
                    )

                    if created:
                        recipient_data = {
                            'id': member.id,
                            'email': member.email,
                            'first_name': member.profile.first_name,
                            'last_name': member.profile.last_name,
                        }

                        note_data = {
                            'id': instance.id,
                            'content': instance.content,
                            'created_at': instance.created_at.isoformat()
                        }

                        activity_data = {
                            'id': instance.activity.id,
                            'title': instance.activity.title
                        }

                        project_data = {
                            'id': project.id,
                            'title': project.title
                        }

                        creator_data = {
                            'id': instance.created_by.id,
                            'first_name': instance.created_by.profile.first_name,
                            'last_name': instance.created_by.profile.last_name
                        }

                        send_note_email_notification.delay(
                            recipient_data,
                            note_data,
                            activity_data,
                            project_data,
                            creator_data
                        )

                except IntegrityError:
                    pass