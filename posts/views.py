from django.shortcuts import render, redirect
from .models import Post
from .forms import PostCreationForm


def index(request):
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'posts/index.html', {'posts': posts})

def post_detail(request, id):
    post = Post.objects.get(id=id)
    context = {
        'post': post
    }

    return render(request, 'posts/detail.html', context)

def create_post(request):
    form = PostCreationForm()

    if request.method == "POST":
        form = PostCreationForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.author = request.user
            form_obj.save()

            return redirect('posts:index')

    context = {
        'form': form
    }

    return render(request, 'posts/create_post.html', context)