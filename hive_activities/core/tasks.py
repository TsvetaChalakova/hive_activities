# tasks.py (Celery tasks for periodic checks)
from datetime import timedelta
from celery import shared_task
from celery.utils.time import timezone
from django.core.mail import send_mail
from hive_activities.activities.models import Activity


@shared_task
def check_approaching_due_dates():
    """Check for tasks due in 24 hours"""
    due_date_threshold = timezone.now() + timedelta(hours=24)
    activities = Activity.objects.filter(
        due_date__lte=due_date_threshold,
        due_date__gt=timezone.now(),
        status__in=['TODO', 'IN_PROGRESS']
    )

    for activity in activities:
        NotificationManager.notify_due_date_approaching(activity)


def send_activity_reminders():
    upcoming_activities = Activity.objects.filter(
        due_date__lt=timezone.now() + timedelta(days=1),
        due_date__gt=timezone.now()
    )

    for activity in upcoming_activities:
        subject = f"Reminder: Activity '{activity.title}' is due soon!"
        message = f"Hi! This is a reminder that your activity '{activity.title}' is due on {activity.due_date}."
        recipient_email = activity.assigned_to.email

        send_mail(subject, message, 'hive.activities.notif@gmail.com', [recipient_email])
