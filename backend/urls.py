from django.contrib import admin
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
    path('devices', views.devices, name='devices')
]