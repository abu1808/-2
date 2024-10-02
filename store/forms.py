from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """Форма для регистрации пользователей."""
    username = forms.CharField(label='Логин', max_length=150)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    """Форма для входа пользователей."""
    username = forms.CharField(label='Логин', max_length=254)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
