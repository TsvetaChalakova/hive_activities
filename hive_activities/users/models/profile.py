from django.db import models
from django.contrib.auth import get_user_model

from hive_activities.users.models import AppUser

UserModel = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
    )

    last_name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,  # Automatically sets the field to now when the object is first created
    )

    updated_at = models.DateTimeField(
        auto_now=True,  # Automatically updates the field to now every time the object is saved
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
