from django.urls import path
from django.contrib.auth.decorators import login_required
from lobby import views


urlpatterns = [
    path('', views.lobby, name='lobby'),
    path('<int:lobby_id>', login_required(views.LobbyView.as_view()), name="clobby"),
    path('ajax/add_lobby_track', views.ajax_add_track, name='add_lobby_track'),
    path('ajax/remove_members', views.ajax_remove_members, name='remove_members')
]