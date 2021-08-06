from django.contrib import admin
from django.urls import path, include

handler404 = 'backend.views.handler404'
handler500 = 'backend.views.handler500'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend.urls')),
    path('social/', include('social_django.urls')),
    path('lobby/', include('lobby.urls'))
]
