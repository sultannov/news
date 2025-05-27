from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import NewsArticle, Category, Comment, Reaction, CommunityPost
from .forms import NewsArticleForm, CommentForm, CommunityPostForm, UserRegisterForm


def home(request):
    categories = Category.objects.all()
    articles = NewsArticle.objects.all().order_by('-created_at')[:10]
    featured_articles = articles[:3]  # For carousel
    return render(request, 'news/home.html', {'categories': categories, 'articles': articles, 'featured_articles': featured_articles})

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = NewsArticle.objects.filter(category=category).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'news/category.html', {'category': category, 'articles': articles, 'categories': categories})

from .models import NewsArticle  # и другие модели

def article_detail(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    reactions = article.reactions.all()
    comments = article.comments.all()
    return render(request, 'news/article_detail.html', {
        'article': article,
        'reactions': reactions,
        'comments': comments,
        'comment_form': CommentForm(),
    })



@login_required
def post_comment(request, article_id):
    article = get_object_or_404(NewsArticle, id=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment posted successfully!')
            return redirect('article_detail', pk=article.id)
    return redirect('article_detail', pk=article.id)

@login_required
def post_reaction(request, article_id, reaction_type):
    article = get_object_or_404(NewsArticle, id=article_id)
    if reaction_type in ['like', 'dislike']:
        Reaction.objects.update_or_create(
            article=article,
            user=request.user,
            reaction_type=reaction_type,
            defaults={'reaction_type': reaction_type}
        )
        messages.success(request, f'{reaction_type.capitalize()} recorded!')
    return redirect('article_detail', pk=article.id)

def community(request):
    posts = CommunityPost.objects.all().order_by('-created_at')
    form = CommunityPostForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommunityPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Community post created!')
            return redirect('community')
    return render(request, 'news/community.html', {'posts': posts, 'form': form, 'categories': Category.objects.all()})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form, 'categories': Category.objects.all()})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials!')
    return render(request, 'news/login.html', {'categories': Category.objects.all()})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')









from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    video = models.FileField(upload_to='articles/videos/', blank=True, null=True)

    def __str__(self):
        return self.title
