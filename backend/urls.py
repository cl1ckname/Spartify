from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
]


urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name= 'logout'),
    path('', views.dashboard, name='dashboard'),
    path('devices', views.devices, name='devices'),
    path('lobby', views.lobby, name='lobby'),
    path('lobby/<int:lobby_id>', login_required(views.LobbyView.as_view()), name="clobby"),
    path('lobby_redirect', views.lobby_redirect, name='lobby_redirect')

]