from django.urls import path
from . import views

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name= 'logout'),
    path('', views.dashboard, name='dashboard'),
    path('devices', views.devices, name='devices'),
    path('ajax/add_queue', views.post_queue, name="post_queue"),
    path('authentication_error', views.authentication_error, name="authentication_error"),
    path('server_error', views.server_error, name="server_error")
]