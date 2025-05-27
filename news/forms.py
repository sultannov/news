from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from news.models import NewsArticle, Comment, CommunityPost


class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'content', 'image', 'video', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CommunityPostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ['content']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']