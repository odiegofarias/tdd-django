from django.test import TestCase
from posts.models import Post
from http import HTTPStatus
from django.urls import resolve, reverse
from posts import views
from model_bakery import baker
from django.contrib.auth import get_user_model


User = get_user_model()

class HomepageTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)
        post1 = Post.objects.create(
            author=self.user,
            title='sample post 1',
            body='It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using "Content here, content here", making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for "lorem ipsum" will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).'
        )

        post2 = Post.objects.create(
            author=self.user,
            title='sample post 2',
            body='It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using "Content here, content here", making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for "lorem ipsum" will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).'
        )

    def test_homepage_returns_correct_response(self):
        response = self.client.get(reverse('posts:index'))
        view = resolve(reverse('posts:index'))
        url = reverse('posts:index')

        self.assertIs(view.func, views.index)
        self.assertEqual(url, '/posts/')
        self.assertTemplateUsed(response, 'posts/index.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.user)
        
    def test_homepage_returns_post_list(self):
        response = self.client.get(reverse('posts:index'))

        """
            Duas formas diferentes de fazer.
            Retornam resultados diferentes
                - response = self.client.get(reverse('posts:home'))
                - Usando o assertIn, retorna mesmo o resultado mesmo não sendo igual        
        """
        self.assertIn('sample post 1', response.content.decode('utf-8'))
        self.assertContains(response, 'sample post 2')