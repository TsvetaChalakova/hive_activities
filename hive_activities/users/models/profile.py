from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
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

    telephone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created at',
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='updated at',
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
