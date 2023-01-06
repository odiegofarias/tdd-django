from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class LoginTest(TestCase):
    def setUp(self) -> None:
        self.username = "testuser123"
        self.email = 'testuser123@email.com'
        self.password = 'password@123'

        User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )

    """ TODO: Criar testes para view e URL """
    def test_login_page_exists(self):
        response = self.client.get(reverse('accounts:login_page'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_login_page_has_login_form(self):
        response = self.client.get(reverse('accounts:login_page'))

        # Verificando se o formulário de login consta no contexto da página
        form = response.context.get('form')

        # Verificando se o FORM é uma instancia do AuthForm
        self.assertIsInstance(form, AuthenticationForm)

    def test_login_page_logs_in_user(self):
        user_data = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post(reverse('accounts:login_page'), user_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('posts:index'))