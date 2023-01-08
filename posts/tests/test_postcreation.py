from django.test import TestCase
from django.urls import reverse, resolve
from http import HTTPStatus
from posts.forms import PostCreationForm
from posts import views
from django.http.request import HttpRequest
from model_bakery import baker
from django.contrib.auth import get_user_model
from posts.models import Post


User = get_user_model()


class PostCreationTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('posts:create_post')
        self.template_name = 'posts/create_post.html'
        self.view = resolve(reverse('posts:create_post'))
        self.form_class = PostCreationForm
        self.title = 'Sample Title'
        self.body = 'Sample Body Test'

        User.objects.create_user(
            username = 'testeuser',
            email = 'testuser@email.com',
            password = 'Password@123'
        )
        

    def test_post_creation_page_exists(self):
        self.client.login(username = 'testeuser', password = 'Password@123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(self.view.func, views.create_post)

        # Verifica se o formulário está no contexto da resposts
        form = response.context.get('form', None)

        # Verifica se o formulário é uma instância do PostCreationForm
        self.assertIsInstance(form, self.form_class)

    def test_post_creation_form_creates_post(self):
        post_request = HttpRequest()

        # Cria o usuário com o bakery
        post_request.user = baker.make(User)

        # Aqui está o formulário de envio
        post_data = {
            'title': self.title,
            'body': self.body
        }

        # Acoplha o formulário na requisição POST
        post_request.POST = post_data

        # Coloca dentro do formulário
        form = self.form_class(post_request.POST)

        # Verifica se o formulário é válido, campos e etc.
        self.assertTrue(form.is_valid())

        # Salva o formulário com um commit False para acrescentar o author
        post_obj = form.save(commit=False)

        # Verifica se é uma instância de POST
        self.assertIsInstance(post_obj, Post)

        # Atribui o request.user(usuário atual, logado no sistema), como autor da postagem e depois salva o formulário
        post_obj.author = post_request.user
        post_obj.save()

        # Verifica se o Post foi efetivamente criado com a contagem de POST.
        self.assertEqual(Post.objects.count(), 1)

    def test_post_creation_requires_login(self):
        """ Teste para verificar se o redirecionamento leva para a URL correta """
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # Redireciona para a URL correta
        self.assertRedirects(response, expected_url='/accounts/login/?next=/posts/create_post/')
