from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(NewsArticle, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user} on {self.article}"

class Reaction(models.Model):
    REACTION_TYPES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )
    article = models.ForeignKey(NewsArticle, related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPES)

    class Meta:
        unique_together = ('article', 'user', 'reaction_type')

    def __str__(self):
        return f"{self.reaction_type} by {self.user} on {self.article}"

class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post by {self.user}"







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
