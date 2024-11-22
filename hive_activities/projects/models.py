from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    STATUS_CHOICES = (
        ('AWARDED', 'Awarded'),
        ('IN_PROGRESS', 'In Progress'),
        ('ON_HOLD', 'On Hold'),
        ('COMPLETED', 'Completed'),
        ('TERMINATED', 'Terminated'),
    )

    PRIORITY_CHOICES = (
        ('STANDARD', 'Standard'),
        ('HIGH_PRIORITY', 'High Priority'),
    )

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    manager = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='owned_projects'
    )
    team_members = models.ManyToManyField(
        User,
        through='ProjectMembership',
        related_name='projects'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AWARDED',
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='STANDARD',
    )
    start_date = models.DateField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("can_change_project_status", "Can change project status"),
            ("can_assign_team_members", "Can assign team members"),
        ]


class ProjectMembership(models.Model):
    ROLES = (
        ('VIEWER', 'Viewer'),
        ('MEMBER', 'Team Member'),
        ('MANAGER', 'Project Manager'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'project']


