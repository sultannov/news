from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Category, NewsArticle, Comment, Reaction, CommunityPost
from django.contrib import messages
from flask import redirect



class SuperuserAdminSite(admin.AdminSite):
    from django.http import HttpResponseRedirect  # Add this import

    class SuperuserAdminSite(admin.AdminSite):
        def __init__(self, name='superuser_admin'):
            super().__init__(name)

        def has_permission(self, request):
            # Allow only superusers or staff to access the admin panel
            return request.user.is_active and (request.user.is_superuser or request.user.is_staff)

        def login(self, request, extra_context=None):
            # Display error message if non-authorized user tries to access admin
            if request.user.is_authenticated and not (request.user.is_superuser or request.user.is_staff):
                messages.error(request, 'Only administrators or authorized staff can access the admin panel.')
                return HttpResponseRedirect(reverse('home'))  # Use HttpResponseRedirect
            return super().login(request, extra_context)


# Instantiate the custom admin site
superuser_admin_site = SuperuserAdminSite()


# Custom admin classes
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'author')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    fields = ('title', 'content', 'image', 'video', 'category', 'author', 'created_at')
    readonly_fields = ('created_at',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)


class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'reaction_type')
    list_filter = ('reaction_type',)


class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('content',)


# Register models with the custom admin site
superuser_admin_site.register(User, UserAdmin)
superuser_admin_site.register(Category, CategoryAdmin)
superuser_admin_site.register(NewsArticle, NewsArticleAdmin)
superuser_admin_site.register(Comment, CommentAdmin)
superuser_admin_site.register(Reaction, ReactionAdmin)
superuser_admin_site.register(CommunityPost, CommunityPostAdmin)