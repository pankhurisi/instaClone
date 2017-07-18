from django import forms
from models import User


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'password']


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
