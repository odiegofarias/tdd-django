from django.shortcuts import render
from .forms import UserRegistrationForm


def register_view(request):
    form = UserRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context) 
