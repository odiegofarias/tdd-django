from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


"""
    class Post
        -id: int
        -title: varchar
        -body: text
        -created_at: datetime
        -updated_at: datetime
"""
User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=225)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.title
    
    
