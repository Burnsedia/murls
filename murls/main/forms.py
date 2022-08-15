from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import ProfileLink

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    username = forms.CharField(
        label='Login',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        label='Adres e-mail',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


    password1 = forms.CharField(
        label='Hasło',
        max_length=150,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label='Potwórz hasło',
        max_length=150,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class AddProfile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['link'].widget.attrs.update({'class': 'form-control custom-input'})
        self.fields['application'].widget.attrs.update({'class': 'form-control custom-input'})

    application = forms.CharField(
        label='Tytuł',
        max_length=40,
    )

    link = forms.URLField(
        label='Link do profilu',
        max_length=200,
        error_messages={'required': 'Please let us know what to call you!'}
    )
    class Meta:
        model = ProfileLink
        fields = ["application", "link"]
