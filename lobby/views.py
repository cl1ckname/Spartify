from datetime import datetime
from random import randint
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.views.generic.base import TemplateView
from lobby.services import _ban_user, _leave_from_lobby, _remove_users_from_lobby, _try_add_to_lobby, _unban_users, add_history
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
        return redirect('/lobby/'+str(user.lobby_in.id))


class LobbyView(TemplateView):
    ''' Lobby Page View '''
    template_name = "lobby/lobby_template.html"
    this_lobby = None
    members = None
    owner = None
    form = None
    username = None

    def get(self, request, lobby_id=0, *args, **kwargs) -> HttpResponse:
        ''' Creates a form and returns a page render if the request method is GET '''
        self.form = AddTrackForm()
        self.set_data(request, lobby_id)
        self.username = request.user.username
        return self.display_page(request)

    def post(self, request, lobby_id=0, *args, **kwargs) -> HttpResponse:
        ''' Creates a form and validates it and also returns a page render if the request method is POST'''
        self.username = request.user.username
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
        token = self.owner.oauth_token

        if username:
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

    

    def get_page_data(self) -> dict:
        track = api.get_user_playback(self.owner.oauth_token)
        name = track_full_name(track)
        history = self.this_lobby.history
        ban_list = self.this_lobby.ban_list.all()
        return {'lobby': self.this_lobby, 'members': self.members, 'track': name, 'form': self.form,
                'owner': self.owner.username, 'history': history, 'is_owner': (self.owner==self.request.user),
                'mmf': MaxMembersForm(num_members=3), 'ban_form': BanForm(), 'ban_list': ban_list}


def add_history(request, lobby: Lobby, link: str):
    ''' Adds track information to the lobby history '''
    track_id = clear_track(link)
    track_raw = api.get_track(track_id, lobby.owner.oauth_token)
    to_json = {'title': track_full_name(track_raw), 'time': datetime.now(
    ).strftime('%H:%M'), 'user': request.user.username}
    if len(lobby.history) > 9:
        lobby.history = lobby.history[0:9]  #max len of history - 10 tracks
    lobby.history = [to_json] + lobby.history
    print(lobby.history)
    lobby.save()

@login_required
def ajax_add_track(request) -> JsonResponse:
    if request.method == 'POST' and request.is_ajax():
        form = AddTrackForm(data = request.POST)
        print(request.POST, 132)
        if form.is_valid():
            link = request.POST['link']
            lobby_id = int(request.POST['add_to'])
            lobby = Lobby.objects.get(id=lobby_id)

            uri = clear_track(link)
            api.add_queue(uri, lobby.owner.oauth_token)
            track_name = track_full_name(api.get_track(uri, lobby.owner.oauth_token))

            add_history(request, lobby, link)
            return JsonResponse({'title': track_name, 'username': request.user.username}, status=200)
        else:
            print(form.errors)
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'errors': 'Not post or ajax'})

@login_required
def ajax_remove_members(request) -> JsonResponse:
    if request.method == 'POST' and request.is_ajax():
        to_delete = request.POST.getlist('to_delete')
        lobby_id = request.POST.get('lobby_id')
        lobby = Lobby.objects.get(id=lobby_id)
        _remove_users_from_lobby(to_delete, lobby)
        if not isinstance(to_delete, list):
            to_delete = [to_delete]
        print(to_delete)
        return JsonResponse({'to_delete': to_delete}, status=200)
    else:
        return JsonResponse({'errors': 'Not post or ajax'}, status=400)

@login_required
def ajax_ban_user(request) -> JsonResponse:
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['username']
        lobby_id = request.POST['lobby_id']
        ban_form = BanForm(data=request.POST)
        if ban_form.is_valid():
            lobby = Lobby.objects.get(id = int(lobby_id))
            _ban_user(lobby, username)
            return JsonResponse({'username': username}, status=200)

    else:
        return JsonResponse({'errors': 'Not post or ajax'}, status=400)

@login_required
def ajax_unban_user(request) -> JsonResponse:
    if request.method == 'POST' and request.is_ajax():
        to_unban = request.POST.getlist('to_unban')
        lobby_id = int(request.POST.get('lobby_id'))
        _unban_users(to_unban, Lobby.objects.get(id=lobby_id))
        return JsonResponse({'unbanned': to_unban}, status=200)
    else:
        return JsonResponse({'errors': 'Not post or ajax'}, status=400)