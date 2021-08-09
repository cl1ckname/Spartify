''' Some logic that made sense to move to a separate file '''

from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lobby.models import Lobby
from backend.models import User
from lobby.forms import JoinLobby, LobbyForm


def _try_add_to_lobby(request):
    ''' Validate the user and tries to add him to the lobby '''
    pin = request.POST.get('pin')
    form = JoinLobby(data=request.POST)
    try:
        lobby = Lobby.objects.get(id=pin)
        lobby.add_user(request.user)
        return redirect('/lobby/'+pin)
    except ValidationError as e:
        form.add_error('pin', e)
        data = {'form': form, 'lobby_form': LobbyForm()}
        return render(request, 'lobby/lobby.html', data)




