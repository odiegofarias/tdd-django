from django.shortcuts import render, redirect
from .forms import UserRegistrationForm


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
    return render(request, 'accounts/login.html')