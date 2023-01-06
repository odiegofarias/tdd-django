from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class LogoutTest(TestCase):
    def setUp(self) -> None:
        self.username = "testuser123"
        self.email = "testuser123@email.com"
        self.password = "password@123"

        User.objects.create_user(
            username = self.username,
            email = self.email,
            password = self.password,
        )
    
    def test_logout_view_logs_out_user(self):
        self.client.login(username=self.username, password=self.password)

        # Para saber se há usuário logado, eu busco o auth_user_id dentro da sessão, após fazer o login
        self.assertTrue('_auth_user_id' in self.client.session)

        self.client.get(reverse('accounts:logout_page'))

        #  Depois de fazer o logout o _auth_user_id não está mais dentro da sessão
        self.assertFalse('_auth_user_id' in self.client.session)