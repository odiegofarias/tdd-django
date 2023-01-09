from django.test import TestCase
from django.urls import reverse, resolve
from http import HTTPStatus
from accounts import views
from django.contrib.auth import get_user_model


User = get_user_model()


class ProfileTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('accounts:current_user_profile')
        self.template_name = 'accounts/profile.html'
        self.view = resolve(reverse('accounts:current_user_profile'))
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.password = 'password@123'

        User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_current_user_profile_exists(self):
        self.client.login(username=self.username, password=self.password)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(self.view.func, views.current_user_profile)

    def test_current_user_profile_requires_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response,
            expected_url='/accounts/login/?next=/accounts/profile/'
        )