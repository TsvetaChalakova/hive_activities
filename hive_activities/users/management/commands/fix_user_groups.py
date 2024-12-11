from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):
    help = 'Assigns correct groups to staff and superusers, removing default group assignments'

    def handle(self, *args, **kwargs):
        # Create groups
        default_group, _ = Group.objects.get_or_create(name='Team Member')
        staff_admin_group, _ = Group.objects.get_or_create(name='Staff Admin')
        super_admin_group, _ = Group.objects.get_or_create(name='Super Admin')

        # Handle staff users
        staff_users = User.objects.filter(is_staff=True, is_superuser=False)
        for user in staff_users:
            user.groups.clear()
            user.groups.add(staff_admin_group)
            user.user_type = 'STAFF_ADMIN'
            user.save()

        # Handle superusers
        superusers = User.objects.filter(is_superuser=True)
        for user in superusers:
            user.groups.clear()
            user.groups.add(super_admin_group)
            user.user_type = 'SUPER_ADMIN'
            user.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated all user groups'))