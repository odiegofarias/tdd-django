from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile


User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'address']

        labels = {
            'address': 'Endereço'
        }

        widgets = {
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3 mt-2'
                }
            ),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control mt-2'
                }
            )
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

        labels = {
            'first_name': 'Primeiro nome',
            'last_name': 'Sobrenome',
            'username': 'Usuário'
        }

        widgets = {
            'first_name': forms.TextInput(
                attrs= {
                    'class': 'form-control mb-2'
                }
            ),
            'last_name': forms.TextInput(
                attrs= {
                    'class': 'form-control mb-2'
                }
            ),
            'username': forms.TextInput(
                attrs= {
                    'class': 'form-control mb-2'
                }
            )
        }