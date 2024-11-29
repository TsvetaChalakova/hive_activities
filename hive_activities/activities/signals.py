from django.db.models.signals import post_save
from django.dispatch import receiver
from hive_activities.activities.models import Activity
from hive_activities.notes.models import Note
from hive_activities.notifications.services import NotificationService


@receiver(post_save, sender=Activity)
def activity_updated(sender, instance, created, **kwargs):
    if not created and instance.tracker.has_changed('status'):
        team_members = instance.project.team_members.all()
        NotificationService.create_notification(
            activity=instance,
            notification_type='status_change',
            team_members=team_members
        )


@receiver(post_save, sender=Note)
def note_added(sender, instance, created, **kwargs):
    if created:
        team_members = instance.activity.project.team_members.all()
        NotificationService.create_notification(
            activity=instance.activity,
            notification_type='note_added',
            team_members=team_members
        )