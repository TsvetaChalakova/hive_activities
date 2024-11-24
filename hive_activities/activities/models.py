from celery.utils.time import timezone
from django.db import models
from django.contrib.auth import get_user_model
from hive_activities.projects.models import Project

User = get_user_model()


class Activity(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User,
        related_name='created_activities',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    assigned_to = models.ForeignKey(
        User,
        related_name='assigned_activities',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    project = models.ForeignKey(
        Project,
        related_name='activities',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='TODO'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    @property
    def is_overdue(self):
        return self.due_date and self.due_date < timezone.now().date()
