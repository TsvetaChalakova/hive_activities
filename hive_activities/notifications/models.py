from django.contrib.auth import get_user_model
from django.db import models
from hive_activities.notes.models import Note

User = get_user_model()


class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
