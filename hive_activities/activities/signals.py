from django.db.models.signals import post_save
from django.dispatch import receiver

import logging

from hive_activities.notes.models import Note
from hive_activities.notifications.services import NotificationService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Note)
def note_added(sender, instance, created, **kwargs):
    if created:
        team_members = instance.activity.project.team_members.all()
        if team_members.exists():
            logger.debug(f"Team members: {team_members}")
            # Call the notification service
            NotificationService.create_note_notification(
                note=instance,
                team_members=team_members,
            )
        else:
            logger.warning(f"No team members found for activity: {instance.activity}")
