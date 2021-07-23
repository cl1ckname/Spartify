from datetime import datetime
from random import randint
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.views.generic.base import TemplateView
from lobby.services import _ban_user, _leave_from_lobby, _remove_users_from_lobby, _try_add_to_lobby
from backend.utils import clear_track, track_full_name
from .models import Lobby, User
from backend.forms import AddTrackForm
from lobby.forms import BanForm, JoinLobby, LobbyForm, MaxMembersForm
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
                return _try_add_to_lobby(request)
            else:
                print(form.errors)
                data = {'form': form, 'lobby_form': LobbyForm(), 'error': form.errors}
                return render(request, 'lobby/lobby.html', data)

        elif max_members:
            _lobby = Lobby(id = randint(0,9999), owner = user, max_members=max_members, num_members=1)
            _lobby.save()
            id = _lobby.id
            user.lobby_in = _lobby
            user.save()
            return redirect(f'/lobby/{id}')
        else:
            return render(request, 'lobby/lobby.html', {'form': JoinLobby(), 'lobby_form': LobbyForm()})
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
        leave = data.get('leave')
        if isinstance(leave, list):
            leave = int(leave[0])
        if isinstance(link, list):
            link = link[0]
        to_delete = data.get('to_delete')
        username = data.get('username')
        try:
            self.set_data(request, lobby_id)
        except ObjectDoesNotExist:
            return redirect('/lobby')
        token = request.user.oauth_token
        if link:
            self.form = AddTrackForm(data=data)
            if self.form.is_valid():
                uri = clear_track(link)
                api.add_queue(uri, token)
                self.add_history(request, data)
        elif to_delete:
            _remove_users_from_lobby(to_delete, self.this_lobby)
        elif username:
            ban_form = BanForm(data=request.POST)
            if ban_form.is_valid():
                if isinstance(username, list):
                    username = username[0]
                _ban_user(self.this_lobby, username)
        elif leave:
            return _leave_from_lobby(leave)
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
        if request.user.lobby_in != self.this_lobby:
            return HttpResponse("Forbidden")
        if self.this_lobby:
            return render(request, self.template_name, self.get_page_data())
        else:
            raise Http404

    def add_history(self, request, data):
        ''' Adds track information to the lobby history '''
        link = data.get('link')
        if isinstance(link, list):
            link = link[0]
        track_id = clear_track(link)
        track_raw = api.get_track(track_id, self.owner.oauth_token)
        to_json = {'title': track_full_name(track_raw), 'time': datetime.now(
        ).strftime('%H:%M'), 'user': request.user.username}
        self.this_lobby.history.append(to_json)
        self.this_lobby.save()

    def get_page_data(self) -> dict:
        track = api.get_user_playback(self.owner.oauth_token)
        name = track_full_name(track)
        history = self.this_lobby.history
        ban_list = self.this_lobby.ban_list.all()
        return {'lobby': self.this_lobby, 'members': self.members, 'track': name, 'form': self.form,
                'owner': self.owner.username, 'history': history, 'is_owner': (self.owner==self.request.user),
                'mmf': MaxMembersForm(num_members=3), 'ban_form': BanForm(), 'ban_list': ban_list}