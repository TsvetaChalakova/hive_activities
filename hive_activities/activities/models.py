from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from hive_activities.projects.models import Project

User = get_user_model()


class Activity(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('ASSIGNED', 'Assigned'),
        ('IN_PROGRESS', 'In Progress'),
        ('PENDING', 'Pending'),
        ('IN_REVIEW', 'In Review'),
        ('CLOSED', 'Closed'),
    )

    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    )

    ACTIVITY_TYPE_CHOICES = (
        ('PARENT', 'Parent Activity'),
        ('CHILD', 'Child Activity'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE_CHOICES,
        default='PARENT'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name='assigned_activities'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='created_activities'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OPEN',
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='LOW',
    )
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', 'due_date']
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.title} ({'Child' if self.parent else 'Parent'})"

    def clean(self):
        if self.parent:
            if self.parent.project != self.project:
                raise ValidationError("Child activity must belong to the same project as its parent.")
            if self.parent == self:
                raise ValidationError("An activity cannot be its own parent.")
            if self.pk:
                children = self.get_all_children()
                if self.parent.pk in [child.pk for child in children]:
                    raise ValidationError("Circular dependency detected in activity relationships.")
            if self.due_date > self.parent.due_date:
                raise ValidationError("Child activity due date cannot be later than parent activity due date.")

            self.activity_type = 'CHILD'
        else:

            self.activity_type = 'PARENT'

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_all_children(self):
        children = []
        for child in self.children.all():
            children.append(child)
            children.extend(child.get_all_children())
        return children

    def change_to_child(self, new_parent):
        if new_parent == self:
            raise ValidationError("An activity cannot be its own parent.")

        if self.children.exists():
            raise ValidationError("Cannot convert an activity with children to a child activity.")

        if new_parent.project != self.project:
            raise ValidationError("Parent activity must be in the same project.")

        self.parent = new_parent
        self.activity_type = 'CHILD'
        self.save()

    def change_to_parent(self):
        self.parent = None
        self.activity_type = 'PARENT'
        self.save()

    @property
    def is_parent(self):
        return self.activity_type == 'PARENT'

    @property
    def is_child(self):
        return self.activity_type == 'CHILD'

    @property
    def is_due_date_approaching(self):
        return self.due_date - timezone.now() <= timezone.timedelta(days=2)

    @property
    def is_overdue(self):
        return self.due_date < timezone.now()