from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class HiveLoginViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword'
        )
        self.login_url = reverse('users:login')

    def test_login_valid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'test@example.com', 'password': 'testpassword', 'remember_me': True})
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'test@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email or password.')

