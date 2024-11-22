from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone

from hive_activities.users.models import AppUser


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('TASK_ASSIGNED', 'Task Assigned'),
        ('TASK_COMPLETED', 'Task Completed'),
        ('COMMENT_ADDED', 'New Comment'),
        ('DUE_DATE', 'Due Date Approaching'),
        ('PROJECT_UPDATE', 'Project Update'),
    )

    recipient = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'read', 'created_at']),
        ]

    def mark_as_read(self):
        self.read = True
        self.save()

    def get_absolute_url(self):
        if self.content_object:
            return self.content_object.get_absolute_url()
        return reverse('dashboard')


class NotificationManager:
    @staticmethod
    def notify_task_assigned(task, assigned_by):
        if task.assigned_to:
            Notification.objects.create(
                recipient=task.assigned_to,
                notification_type='TASK_ASSIGNED',
                title=f'New Task Assigned: {task.title}',
                message=f'{assigned_by.get_full_name()} assigned you a task in project {task.project.title}',
                content_object=task
            )

    @staticmethod
    def notify_task_completed(task):
        # Notify project owner and task creator
        recipients = {task.project.owner, task.created_by}
        for recipient in recipients:
            Notification.objects.create(
                recipient=recipient,
                notification_type='TASK_COMPLETED',
                title=f'Task Completed: {task.title}',
                message=f'Task in project {task.project.title} has been marked as complete',
                content_object=task
            )

    @staticmethod
    def notify_comment_added(comment):
        # Notify task assignee and previous commenters
        task = comment.task
        recipients = {task.assigned_to, task.created_by}
        previous_commenters = task.comments.exclude(
            author=comment.author
        ).values_list('author', flat=True).distinct()

        recipients.update(previous_commenters)

        for recipient in recipients:
            if recipient and recipient != comment.author:
                Notification.objects.create(
                    recipient=recipient,
                    notification_type='COMMENT_ADDED',
                    title=f'New Comment on Task: {task.title}',
                    message=f'{comment.author.get_full_name()} commented on a task you\'re following',
                    content_object=comment
                )

    @staticmethod
    def notify_due_date_approaching(task):
        if task.assigned_to:
            Notification.objects.create(
                recipient=task.assigned_to,
                notification_type='DUE_DATE',
                title=f'Due Date Approaching: {task.title}',
                message=f'Task is due in 24 hours',
                content_object=task
            )
