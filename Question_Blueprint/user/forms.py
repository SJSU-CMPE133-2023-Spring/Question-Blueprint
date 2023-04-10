from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = models.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserInfoUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    username = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email']


# class for update profile
class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    image = forms.ImageField(required=False)
    facebook_link = forms.URLField(required=False)
    twitter_link = forms.URLField(required=False)
    linkedin_link = forms.URLField(required=False)
    
    class Meta:
        model = Profile
        fields = ['bio', 'image', 'facebook_link', 'twitter_link', 'linkedin_link']

