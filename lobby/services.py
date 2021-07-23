''' Some logic that made sense to move to a separate file '''

from django.core.exceptions import ValidationError
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

def _leave_from_lobby(id):
    member = User.objects.get(id = id)
    member.lobby_in = None
    member.save()
    return redirect('/lobby')