from django.contrib.auth import get_user_model
from django.db import models

from hive_activities.activities.models import Activity

User = get_user_model()


class Note(models.Model):
    task = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='task_comments'
    )
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

