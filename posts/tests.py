from django.test import TestCase
from .models import Post
from http import HTTPStatus
from django.urls import resolve, reverse
from . import views
from model_bakery import baker
from django.contrib.auth import get_user_model


User = get_user_model()


# Create your tests here.
class PostModelTest(TestCase):
    def test_post_model_exists_but_empty(self):
        posts = Post.objects.count()

        self.assertEqual(posts, 0)

    def test_string_representation_of_objects(self):
        post = baker.make(Post)

        self.assertEqual(str(post), post.title)
        self.assertTrue(isinstance(post, Post))


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
        response = self.client.get('/')
        view = resolve(reverse('posts:index'))

        self.assertIs(view.func, views.index)
        self.assertTemplateUsed(response, 'posts/index.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
    def test_homepage_returns_post_list(self):
        response = self.client.get('/')

        """
            Duas formas diferentes de fazer.
            Retornam resultados diferentes
                - response = self.client.get(reverse('posts:home'))
                - Usando o assertIn, retorna mesmo o resultado mesmo não sendo igual        
        """
        self.assertIn('sample post 1', response.content.decode('utf-8'))
        self.assertContains(response, 'sample post 2')


class DetailPageTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)
        self.post = Post.objects.create(
            title='Learn Javascript in the 23 hour course',
            body='this is a beginner course on JS',
            author=self.user,
        )

    def test_detail_page_returns_correct_response(self):
        response = self.client.get(reverse('posts:post-detail', kwargs={'id': self.post.id}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/detail.html')

    def test_detail_page_returns_correct_content(self):
        response = self.client.get(reverse('posts:post-detail', kwargs={'id': self.post.id}))

        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)
        # self.assertContains(response, self.post.created_at)


class PostAuthorTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)
        self.post = Post.objects.create(
            title='Test title',
            body='Test body',
            author=self.user,
        )


    def test_author_and_post_is_instance_of_user_model(self):
        self.assertTrue(isinstance(self.user, User))

    def test_post_belongs_to_user(self):
        self.assertTrue(hasattr(self.post, 'author'))
        self.assertEqual(self.post.author, self.user)
        