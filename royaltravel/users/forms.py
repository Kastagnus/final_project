from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField()
