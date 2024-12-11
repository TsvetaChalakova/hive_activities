from django.contrib.auth import get_user_model
from django.db import models

from hive_activities.activities.models import Activity

User = get_user_model()


class Note(models.Model):

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='notes'
    )

    content = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='note_created_by',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_closed = models.BooleanField(
        default=False,
    )

