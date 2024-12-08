from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core import mail

from hive_activities.users.models import UserProfile, UserType, RoleRequest

User = get_user_model()


class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')
        self.signup_url = reverse('users:signup')
        self.dashboard_url = reverse('activities:team_dashboard')

        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            is_active=True
        )

        team_member_group = Group.objects.get(name='Team Member')
        self.user.groups.add(team_member_group)

        UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User'
        )

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'testpass123',
        })
        self.assertRedirects(response, self.dashboard_url)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_with_wrong_password(self):
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_login_with_nonexistent_user(self):
        response = self.client.post(self.login_url, {
            'username': 'nonexistent@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_signup_success(self):
        form_data = {
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.signup_url, form_data)
        self.assertRedirects(response, self.dashboard_url)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_redirect_if_already_logged_in(self):
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.dashboard_url)

    def test_signup_with_existing_email(self):
        form_data = {
            'email': 'test@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.context['form'].errors)

    def test_signup_with_mismatched_passwords(self):
        form_data = {
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'differentpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('password2', response.context['form'].errors)

    def test_signup_with_missing_fields(self):
        form_data = {
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
        }
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('first_name', response.context['form'].errors)
        self.assertIn('last_name', response.context['form'].errors)


class ProfileViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User'
        )
        self.client.login(email='test@example.com', password='testpass123')

    def test_profile_detail_view(self):
        url = reverse('users:profile-detail', kwargs={'pk': self.profile.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.profile)

    def test_profile_edit_view(self):
        url = reverse('users:profile-edit', kwargs={'pk': self.profile.pk})
        response = self.client.post(url, {
            'first_name': 'Updated',
            'last_name': 'Name',
            'telephone': '1234567890'
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Updated')
        self.assertEqual(self.profile.last_name, 'Name')

    def test_profile_delete_view(self):
        url = reverse('users:profile-delete', kwargs={'pk': self.profile.pk})
        response = self.client.post(url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)


class RoleRequestViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.team_member_group = Group.objects.get(name='Team Member')
        self.project_manager_group = Group.objects.get(name='Project Manager')

        self.team_member = User.objects.create_user(
            email='team@example.com',
            password='pass123',
            user_type=UserType.TEAM_MEMBER
        )
        UserProfile.objects.create(
            user=self.team_member,
            first_name='Team',
            last_name='Member'
        )

        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='pass123',
            user_type=UserType.STAFF_ADMIN,
            is_staff=True
        )
        UserProfile.objects.create(
            user=self.admin,
            first_name='Admin',
            last_name='User'
        )

        self.team_member.groups.add(self.team_member_group)

    def test_role_request_creation(self):
        self.client.login(username='team@example.com', password='pass123')
        url = reverse('users:role_change')
        response = self.client.post(url, {
            'requested_role': UserType.PROJECT_MANAGER
        })
        self.assertTrue(RoleRequest.objects.filter(user=self.team_member).exists())

    def test_role_request_management(self):
        self.client.login(username='admin@example.com', password='pass123')

        role_request = RoleRequest.objects.create(
            user=self.team_member,
            requested_role=UserType.PROJECT_MANAGER
        )

        url = reverse('users:pending_role_requests')
        response = self.client.post(url, {
            'selected_requests': [role_request.id],
            'action': 'approve'
        })

        role_request.refresh_from_db()
        self.team_member.refresh_from_db()
        self.assertTrue(role_request.approved)
        self.assertEqual(self.team_member.user_type, UserType.PROJECT_MANAGER)


class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

        team_member_group = Group.objects.get(name='Team Member')
        self.user.groups.add(team_member_group)

        UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User'
        )

    def test_password_reset_request(self):
        url = reverse('users:password_reset')
        response = self.client.post(url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['test@example.com'])

    def test_password_change(self):
        self.client.login(username='test@example.com', password='testpass123')
        url = reverse('users:password_change')
        response = self.client.post(url, {
            'old_password': 'testpass123',
            'new_password1': 'newtestpass123',
            'new_password2': 'newtestpass123'
        })
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newtestpass123'))