from datetime import datetime
from random import randint
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.views.generic.base import TemplateView
from backend.utils import LobbyIsFull, track_full_name, clear_track, _add_to_lobby
from .models import Lobby, User
from backend.forms import AddTrackForm
from lobby.forms import JoinLobby, LobbyForm
from backend.spotify import api


@login_required
def lobby(request):
    user = request.user
    if request.method == "POST":
        pin = request.POST.get('pin')
        max_members = request.POST.get('max_members')
        if pin:
            form = JoinLobby(data=request.POST)
            if form.is_valid():
                try:
                    _add_to_lobby(user, pin)
                    return redirect('/lobby/'+pin)
                except LobbyIsFull as e:
                    data = {'form': JoinLobby(), 'lobby_form': LobbyForm(), 'error': "aboba"}
                    print(str(data))
                    render(request, 'lobby/lobby.html', data)

        elif max_members:
            _lobby = Lobby(id = randint(0,9999), owner = user, max_members=max_members, num_members=1)
            _lobby.save()
            id = _lobby.id
            user.lobby_in = _lobby
            user.save()
            return redirect(f'/lobby/{id}')
        else:
            return render(request, 'lobby/lobby.html', {'form': JoinLobby(), 'lobby_form': LobbyForm(), })
    else:
        form = JoinLobby()
    if not user.lobby_in:
        return render(request, 'lobby/lobby.html', {'form': form, 'lobby_form': LobbyForm()})
    else:
        return redirect('lobby/'+str(user.lobby_in.id))


class LobbyView(TemplateView):
    ''' Lobby Page View '''
    template_name = "lobby/lobby_template.html"
    this_lobby = None
    members = None
    owner = None
    form = None

    def get(self, request, lobby_id=0, *args, **kwargs) -> HttpResponse:
        ''' Creates a form and returns a page render if the request method is GET '''
        self.form = AddTrackForm()
        self.set_data(request, lobby_id)
        return self.display_page(request)

    def post(self, request, lobby_id=0, *args, **kwargs) -> HttpResponse:
        ''' Creates a form and validates it and also returns a page render if the request method is POST'''
        data = dict(request.POST)
        link = data.get('link')
        to_delete = data.get('to_delete')
        self.set_data(request, lobby_id)
        token = request.user.oauth_token
        if link:
            self.form = AddTrackForm(data=data)
            if self.form.is_valid():
                uri = clear_track(link)
                api.add_queue(uri, token)
                self.add_history(request, data)
        elif to_delete:
            for id in to_delete:
                user = User.objects.get(id=int(id))
                user.lobby_in = None
                user.save()
        else:
            id_to_delete = request.POST.get('delete')
            if id_to_delete:
                if int(id_to_delete) == self.this_lobby.id:
                    self.this_lobby.delete()
                    return redirect('/lobby')

        return self.display_page(request)

    def set_data(self, request, lobby_id) -> None:
        ''' Sets the view data according to the request and the lobby '''
        self.this_lobby = Lobby.objects.get(id=lobby_id)
        self.members = User.objects.filter(lobby_in=self.this_lobby)
        self.owner = self.this_lobby.owner
        api.refresh_user(self.owner)

    def display_page(self, request) -> HttpResponse:
        ''' Collects the view fields in the HttpResponse and checks the user's access to the lobby '''
        track = api.get_user_playback(self.owner.oauth_token)
        history = self.this_lobby.history

        name = track_full_name(track)

        if request.user.lobby_in != self.this_lobby:
            return HttpResponse("Forbidden")

        if self.this_lobby:
            return render(request, self.template_name, {'lobby': self.this_lobby, 'members': self.members, 'track': name, 'form': self.form,
                                                        'owner': self.owner.username, 'history': history, 'is_owner': (self.owner==self.request.user)})
        else:
            raise Http404

    def add_history(self, request, data):
        ''' Adds track information to the lobby history '''
        track_id = clear_track(data['link'])
        track_raw = api.get_track(track_id, self.owner.oauth_token)
        to_json = {'title': track_full_name(track_raw), 'time': datetime.now(
        ).strftime('%H:%M'), 'user': request.user.username}
        self.this_lobby.history.append(to_json)
        self.this_lobby.save()
