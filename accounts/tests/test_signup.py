from django.test import TestCase
from django.urls import reverse, resolve
from http import HTTPStatus
from accounts import views
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import UserRegistrationForm
from django.contrib.auth import get_user_model


class AccountCreationTest(TestCase):
    def setUp(self) -> None:
        self.form_class = UserRegistrationForm

    def test_signup_page_exists(self):
        response = self.client.get(reverse('accounts:signup-view'))
        url = reverse('accounts:signup-view')
        view = resolve(reverse('accounts:signup-view'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(url, '/accounts/signup/')
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertEqual(view.func, views.register_view)
        self.assertContains(response, 'Crie sua conta')


    def test_signup_form_works_correctly(self):

        # Verifica se é uma subclasse da UserCreationForm
        self.assertTrue(issubclass(self.form_class, UserCreationForm))
        # Verifica se tem um field "email" dentro de UserRegistrationForm > Meta.fields
        self.assertTrue('email' in self.form_class.Meta.fields)
        self.assertTrue('username' in self.form_class.Meta.fields)
        self.assertTrue('password1' in self.form_class.Meta.fields)
        self.assertTrue('password2' in self.form_class.Meta.fields)

        # Dados para serem enviados no formulário
        sample_data = {
            'email': 'test@email.com',
            'username': 'test01',
            'password1': 'passw0rd001',
            'password2': 'passw0rd001',
        }

        # POSTando os dados no formulário
        form = self.form_class(sample_data)

        # Verificando se o form é válido
        self.assertTrue(form.is_valid())

    def test_signup_form_create_user_in_db(self):
        user = {
            'email': 'test1@email.com',
            'username': 'test012',
            'password1': 'passw0rd0012',
            'password2': 'passw0rd0012',
        }

        form = self.form_class(user)
        User = get_user_model()

        if form.is_valid():
            form.save()

        
        # Verifica que o usuário é criado
        self.assertEqual(User.objects.count(), 1)
        
