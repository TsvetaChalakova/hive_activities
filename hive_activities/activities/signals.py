from django.contrib.sessions.models import Session
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from hive_activities.activities.models import Activity


@receiver(pre_delete, sender=Session)
def cleanup_session_activities(sender, instance, **kwargs):

    Activity.objects.filter(
        session_key=instance.session_key,
        project__isnull=True,
        created_by__isnull=True
    ).delete()