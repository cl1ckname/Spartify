from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler500
from backend.views import handler500er

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend.urls')),
    path('social/', include('social_django.urls')),
    path('lobby/', include('lobby.urls'))
]

handler500 = 'backend.views.handler500er'