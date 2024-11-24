from celery import shared_task

from hive_activities.activities.models import TemporaryActivity


@shared_task
def cleanup_expired_activities():
    TemporaryActivity.cleanup_expired()
    return "Expired activities cleaned up."
