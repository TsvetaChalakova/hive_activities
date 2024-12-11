from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from hive_activities.core.validators import validate_due_date_after_start_date, validate_no_special_characters

User = get_user_model()


class Project(models.Model):

    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('ON_HOLD', 'On Hold'),
        ('COMPLETED', 'Completed'),
    ]

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a unique project title",
        validators=[validate_no_special_characters],
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text="Describe the project goals and scope",
    )

    manager = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='owned_projects',
    )

    team_members = models.ManyToManyField(
        User,
        through='ProjectMembership',
        related_name='projects'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='IN_PROGRESS',
    )

    start_date = models.DateField(
        help_text="Project start date"
    )

    due_date = models.DateField(
        help_text="Project deadline"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def clean(self):
        validate_due_date_after_start_date(self.start_date, self.due_date)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class ProjectMembership(models.Model):

    ROLES = (
        ('MEMBER', 'Team Member'),
        ('MANAGER', 'Project Manager'),
        ('VIEWER', 'Viewer'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='memberships',
    )

    role = models.CharField(
        max_length=20,
        choices=ROLES,
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.project.title} ({self.get_role_display()})"

    class Meta:
        unique_together = ['user', 'project']
        verbose_name = "Project Membership"
        verbose_name_plural = "Project Memberships"


