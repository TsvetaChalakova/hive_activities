# # tasks.py (Celery tasks for periodic checks)
# from celery import shared_task
#
#
# @shared_task
# def check_approaching_due_dates():
#     """Check for tasks due in 24 hours"""
#     due_date_threshold = timezone.now() + timedelta(hours=24)
#     tasks = Task.objects.filter(
#         due_date__lte=due_date_threshold,
#         due_date__gt=timezone.now(),
#         status__in=['TODO', 'IN_PROGRESS']
#     )
#
#     for task in tasks:
#         NotificationManager.notify_due_date_approaching(task)

from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from hive_activities.activities.models import TemporaryActivity


def send_activity_reminders():
    upcoming_activities = TemporaryActivity.objects.filter(
        due_date__lt=timezone.now() + timedelta(days=1),
        due_date__gt=timezone.now()
    )

    for activity in upcoming_activities:
        subject = f"Reminder: Activity '{activity.title}' is due soon!"
        message = f"Hi! This is a reminder that your activity '{activity.title}' is due on {activity.due_date}."
        recipient_email = activity.email  # Send to the email associated with the activity

        send_mail(subject, message, 'from@example.com', [recipient_email])
