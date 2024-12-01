from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class RoleRequest(models.Model):
    REQUESTED_ROLE_CHOICES = [
        ('PROJECT_MANAGER', 'Project Manager'),
    ]

    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='role_request'
    )
    requested_role = models.CharField(max_length=20, choices=REQUESTED_ROLE_CHOICES)
    approved = models.BooleanField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
