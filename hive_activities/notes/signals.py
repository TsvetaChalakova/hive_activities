from django.db.models.signals import post_save
from django.dispatch import receiver
from hive_activities.notes.models import Note
from hive_activities.notifications.services import NotificationService


@receiver(post_save, sender=Note)
def note_created(sender, instance, created, **kwargs):
    if created:
        team_members = instance.activity.project.team_members.all()
        NotificationService.create_note_notification(
            note=instance,
            team_members=team_members
        )