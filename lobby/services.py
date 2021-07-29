''' Some logic that made sense to move to a separate file '''

import datetime
from requests import api
from backend.utils import clear_track, track_full_name
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import redirect, render
from lobby.models import Lobby
from backend.models import User
from lobby.forms import JoinLobby, LobbyForm


def _add_to_lobby(user, lobby_pin):
    """ Add user to lobby if it possible"""
    lobby = Lobby.objects.get(id=lobby_pin)
    if lobby.num_members < lobby.max_members:
        if not lobby.ban_list.filter(id = user.id):
            lobby.num_members += 1
            user.lobby_in = lobby
            user.save()
            lobby.save()
        else:
            raise ValidationError("You are banned here", code='invalid')
    else:
        raise ValidationError("Lobby is full! Max members: %(max_members)s", params={'max_members': lobby.max_members})

def _remove_users_from_lobby(users: list, lobby: Lobby):
    ''' Removes users from lobby '''
    for id in users:
        user = User.objects.get(id=int(id))
        if user.lobby_in == lobby:
            user.lobby_in = None
            user.save()

def _ban_user(lobby: Lobby, username: str):
    ''' Ban user in lobby '''
    user = User.objects.get(username = username)
    if user.lobby_in == lobby:
        user.lobby_in = None
        user.save()
    lobby.ban_list.add(user)
    lobby.save()

def _try_add_to_lobby(request):
    ''' Validate the user and tries to add him to the lobby '''
    pin = request.POST.get('pin')
    form = JoinLobby(data=request.POST)
    try:
        _add_to_lobby(request.user, pin)
        return redirect('/lobby/'+pin)
    except ValidationError as e:
        form.add_error('pin',e)
        data = {'form': form, 'lobby_form': LobbyForm()}
        return render(request, 'lobby/lobby.html', data)

def _leave_from_lobby(id:int):
    member = User.objects.get(id = id)
    member.lobby_in = None
    member.save()
    return redirect('/lobby')

def add_history(request, lobby: Lobby, link: str):
    ''' Adds track information to the lobby history '''
    track_id = clear_track(link)
    track_raw = api.get_track(track_id, lobby.owner.oauth_token)
    to_json = {'title': track_full_name(track_raw), 'time': datetime.now(
    ).strftime('%H:%M'), 'user': request.user.username}
    if len(lobby.history) > 9:
        lobby.history = lobby.history[0:9]  #max len of history - 10 tracks
    lobby.history = [to_json] + lobby.history
    lobby.save()

def _unban_users(to_unban: list, lobby: Lobby):
    try:
        for user_id in to_unban:
            user = User.objects.get(id=int(user_id))
            lobby.ban_list.remove(user)
    except ObjectDoesNotExist:
        raise ValidationError("Unban error")
        
