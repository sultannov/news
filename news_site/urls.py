from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from news.admin import superuser_admin_site

urlpatterns = [
    path('admin/', superuser_admin_site.urls),
    path('', include('news.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)