from django import forms
from django.contrib.auth.forms import UserCreationForm
from profiles.models import User
from profiles.models import Profile


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1','password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'bio', 'profile_pic', 'facebook', 'twitter', 'linkedin')