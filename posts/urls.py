from . import views
from django.urls import path


app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:id>/', views.post_detail, name='post-detail'),
]