from django.db import models
from django.urls import reverse


"""
    class Post
        -id: int
        -title: varchar
        -body: text
        -created_at: datetime
        -updated_at: datetime
"""

class Post(models.Model):
    title = models.CharField(max_length=225)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title
    
    
