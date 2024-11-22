# tasks.py (Celery tasks for periodic checks)
from celery import shared_task


@shared_task
def check_approaching_due_dates():
    """Check for tasks due in 24 hours"""
    due_date_threshold = timezone.now() + timedelta(hours=24)
    tasks = Task.objects.filter(
        due_date__lte=due_date_threshold,
        due_date__gt=timezone.now(),
        status__in=['TODO', 'IN_PROGRESS']
    )

    for task in tasks:
        NotificationManager.notify_due_date_approaching(task)