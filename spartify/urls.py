from django.contrib import admin
from django.urls import path, include
from backend.views import get_code


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend.urls')),
    path('social/complete/spotify/', get_code),
    path('social/', include('social_django.urls')),
]