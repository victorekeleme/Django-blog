from django import forms
from blog.models import Post, Category, Comments
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image','category')

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','password1','password2')



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('content',)

