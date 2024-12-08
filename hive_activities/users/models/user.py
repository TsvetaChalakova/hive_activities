from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from hive_activities.users.management.managers import AppUserManager
from django.db.models import TextChoices


class UserType(TextChoices):
    TEAM_MEMBER = 'TEAM_MEMBER', 'Team Member'
    PROJECT_MANAGER = 'PROJECT_MANAGER', 'Project Manager'
    VIEWER = 'VIEWER', 'Viewer'
    STAFF_ADMIN = 'STAFF_ADMIN', 'Staff Admin'
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'


class AppUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = "email"

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.TEAM_MEMBER,
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='appuser_set',
        related_query_name='appuser'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='appuser_set',
        related_query_name='appuser'
    )

    def __str__(self):
        return self.email or "Anonymous User"

    def is_team_member(self):
        return self.user_type == UserType.TEAM_MEMBER

    def is_viewer(self):
        return self.user_type == UserType.VIEWER

    def is_project_manager(self):
        return self.user_type == UserType.PROJECT_MANAGER

    def is_staff_admin(self):
        return self.is_staff and not self.is_superuser

    def is_super_admin(self):
        return self.is_superuser

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['pk']

    objects = AppUserManager()




