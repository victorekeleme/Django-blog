from django import forms
from blog.models import Post, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class PostForm(forms.ModelForm):
    model = Post
    class Meta:
        fields = ('title', 'content')

class SignUpForm(UserCreationForm):
    model = User
    class Meta:
        fields = ('first_name','last_name','username','password1','password2')
