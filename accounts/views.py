from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileUpdateForm, UserUpdateForm
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

@login_required
def update_user_profile(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    if request.method == "POST":
        profile_form = ProfileUpdateForm(instance=request.user.profile, data={
            'bio': request.POST.get('bio', None),
            'address': request.POST.get('address', None)
        })
        user_form = UserUpdateForm(instance=request.user, data={
            'first_name': request.POST.get('first_name', None),
            'username': request.POST.get('username', None),
            'last_name': request.POST.get('last_name', None)
        })

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()

            return redirect('accounts:current_user_profile')

    context = {
        'profile_form': profile_form,
        'user_form': user_form,
    }

    return render(request, 'accounts/updateprofile.html', context)