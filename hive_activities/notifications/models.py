from django.contrib.auth import get_user_model
from django.db import models
from hive_activities.notes.models import Note

User = get_user_model()


class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE,
    )

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-created_at']
        unique_together = ['recipient', 'note', 'created_at']

    def __str__(self):
        return f'Notification for {self.recipient} on {self.note}'
