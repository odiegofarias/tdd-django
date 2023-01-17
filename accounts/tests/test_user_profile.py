from django.test import TestCase
from django.urls import reverse, resolve
from http import HTTPStatus
from accounts import views
from accounts.forms import ProfileUpdateForm, UserUpdateForm
from django.contrib.auth import get_user_model
from django.http import HttpRequest


User = get_user_model()


class UpdateProfileTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('accounts:update_user_profile')
        self.template_name = 'accounts/updateprofile.html'
        self.view = resolve(reverse('accounts:update_user_profile'))
        self.username = 'testuser1'
        self.email = 'testuser@email.com'
        self.password = 'password@123'

        User.objects.create_user(
            username = self.username,
            email = self.email,
            password = self.password
        )

    def test_profile_update_page_exists(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(self.view.func, views.update_user_profile)
    
        # Pegando  os formulários do perfil e o user estão sendo passados no contexto da página
        profile_form = response.context.get('profile_form', None)
        user_form = response.context.get('user_form', None)

        # Verificando se são instancias dos ModelForms
        self.assertIsInstance(profile_form, ProfileUpdateForm)
        self.assertIsInstance(user_form, UserUpdateForm)

    def test_profile_and_user_update_forms_update_users(self):

        # Atribuindo o request do POST para formulário
        request = HttpRequest()

        # Pegando o usuário criado no setup
        request.user = User.objects.get(id=1)

        # Aqui temos os dados do formulário para atualizar
        request.POST = {
            'bio': 'sample bio test',
            'address': 'sample address test 123',
            'first_name': 'testtestando123',
            'last_name': 'testtestando1234',
            'username': 'test1234'
        }

        # Passando o formulário com os dados
        """
            Atribuindo ao formulário a instancia de Profile,
            Passando as informações para cada campo e pegando os campos ('')
        """
        profile_form = ProfileUpdateForm(instance=request.user.profile, data={
            'bio': request.POST.get('bio', None),
            'address': request.POST.get('address', None)
        })
        user_form = UserUpdateForm(instance=request.user, data={
            'first_name': request.POST.get('first_name', None),
            'username': request.POST.get('username', None),
            'last_name': request.POST.get('last_name', None)
        })

        # Verificando se é válido
        self.assertTrue(profile_form.is_valid())
        self.assertTrue(user_form.is_valid())

        profile_form.save()
        user_form.save()

        # Verificando se o usuário atual/profile é o mesmo que foi enviado no campo POST
        self.assertEqual(request.user.username, request.POST.get('username', None))
        self.assertEqual(request.user.profile.bio, request.POST.get('bio', None))



