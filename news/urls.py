from django.urls import path
from news import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('community/', views.community, name='community'),
    path('post_comment/<int:article_id>/', views.post_comment, name='post_comment'),
    path('post_reaction/<int:article_id>/<str:reaction_type>/', views.post_reaction, name='post_reaction'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]