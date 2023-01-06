from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


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