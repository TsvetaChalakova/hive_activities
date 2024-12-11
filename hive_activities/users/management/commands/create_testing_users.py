from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


User = get_user_model()


class Command(BaseCommand):
    help = 'Creates test users for each user group with corresponding profiles'

    def handle(self, *args, **kwargs):
        # Test user data
        test_users = [
            {
                'email': 'team@test.com',
                'password': '123admin123',
                'user_type': 'TEAM_MEMBER',
                'is_staff': False,
                'is_superuser': False,
                'group': 'Team Member',
                'profile_data': {
                    'first_name': 'Test',
                    'last_name': 'Member',
                }
            },
            {
                'email': 'staff@test.com',
                'password': '123admin123',
                'user_type': 'STAFF_ADMIN',
                'is_staff': True,
                'is_superuser': False,
                'group': 'Staff Admin',
                'profile_data': {
                    'first_name': 'Test',
                    'last_name': 'Staff',
                }
            },
            {
                'email': 'super@test.com',
                'password': '123admin123',
                'user_type': 'SUPER_ADMIN',
                'is_staff': True,
                'is_superuser': True,
                'group': 'Super Admin',
                'profile_data': {
                    'first_name': 'Test',
                    'last_name': 'Super',
                }
            },
            {
                'email': 'viewer@test.com',
                'password': '123admin123',
                'user_type': 'VIEWER',
                'is_staff': False,
                'is_superuser': False,
                'group': 'Viewer',
                'profile_data': {
                    'first_name': 'Test',
                    'last_name': 'Viewer',
                }
            },
            {
                'email': 'pm@test.com',
                'password': '123admin123',
                'user_type': 'PROJECT_MANAGER',
                'is_staff': False,
                'is_superuser': False,
                'group': 'Project Manager',
                'profile_data': {
                    'first_name': 'Test',
                    'last_name': 'Super',
                }
            }
        ]

        for user_data in test_users:
            # Check if user already exists
            if not User.objects.filter(email=user_data['email']).exists():
                # Create user
                user = User.objects.create_user(
                    email=user_data['email'],
                    password=user_data['password'],
                )

                # Set staff and superuser status
                user.is_staff = user_data['is_staff']
                user.is_superuser = user_data['is_superuser']
                user.user_type = user_data['user_type']
                user.save()

                # Add to appropriate group
                group = Group.objects.get(name=user_data['group'])
                user.groups.add(group)

                # Update profile
                if hasattr(user, 'profile'):
                    profile = user.profile
                    profile.first_name = user_data['profile_data']['first_name']
                    profile.last_name = user_data['profile_data']['last_name']
                    profile.save()

                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created {user_data["user_type"]} test user: {user.email}'))
            else:
                self.stdout.write(f'User {user_data["email"]} already exists, skipping...')

        self.stdout.write(self.style.SUCCESS('All test users created successfully'))