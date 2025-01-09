from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),  # Polls app URLs
    path('accounts/', include('allauth.urls')),  # Allauth URLs should come first
    path('accounts/', include('django.contrib.auth.urls')),  # Django auth URLs

    
]
