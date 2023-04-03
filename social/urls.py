from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from feed.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('feed.urls'), name='dashboard'),
    path('home/', TemplateView.as_view(template_name='dashboard/home.html'), name='home'),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
