from django.test import TestCase
from .models import Post


# Create your tests here.
class PostModelTest(TestCase):
    def test_post_model_exists_but_empty(self):
        posts = Post.objects.count()

        self.assertEqual(posts, 0)
