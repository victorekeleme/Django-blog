from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','password1','password2')
