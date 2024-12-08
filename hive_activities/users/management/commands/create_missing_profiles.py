
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from hive_activities.users.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates missing profiles for users'

    def handle(self, *args, **kwargs):
        # Get all existing profile user IDs
        existing_profile_user_ids = UserProfile.objects.values_list('user_id', flat=True)

        # Find users without profiles
        users_without_profiles = User.objects.exclude(id__in=existing_profile_user_ids)
        profiles_created = 0

        for user in users_without_profiles:
            UserProfile.objects.create(
                user=user,
                first_name=user.email,
                last_name='gaff',
            )
            profiles_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {profiles_created} profiles'
            )
        )