from django.test import TestCase
from posts.models import Post
from http import HTTPStatus
from django.urls import resolve, reverse
from posts import views
from model_bakery import baker
from django.contrib.auth import get_user_model


User = get_user_model()

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
        url = reverse('posts:post-detail', kwargs={'id': self.post.id})
        view = resolve(reverse('posts:post-detail', kwargs={'id': self.post.id}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/detail.html')
        self.assertEqual(url, f'/posts/post/{self.post.id}/')
        self.assertEqual(view.func, views.post_detail)

    def test_detail_page_returns_correct_content(self):
        response = self.client.get(reverse('posts:post-detail', kwargs={'id': self.post.id}))

        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)
        # self.assertContains(response, self.post.created_at)