from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from posts.models import Post
from django.contrib.auth.decorators import login_required


def register_view(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('accounts:login_page')

    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context) 

def login_page(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user_authenticated = authenticate(username=username, password=password)

            if user_authenticated is not None:
                login(request, user_authenticated)

                return redirect('posts:index')

    context = {
        'form': form
    }

    return render(request, 'accounts/login.html', context)

def logout_page(request):
    logout(request)

    return redirect('posts:index')

@login_required
def current_user_profile(request):
    user = request.user
    posts = Post.objects.filter(author=user).all().order_by('-created_at')

    context = {
        'user': user,
        'posts': posts
    }

    return render(request, 'accounts/profile.html', context)