from backend.SpotifyAPI.tracks import Track
from random import randint
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from lobby.services import _leave_from_lobby, _try_add_to_lobby
from .models import Lobby, User
from backend.forms import AddTrackForm
from lobby.forms import BanForm, JoinLobby, LobbyForm, MaxMembersForm
from backend.SpotifyAPI import api
from backend.services import SafeView


@login_required
def lobby(request):
    user = request.user
    if request.method == 'POST':
        pin = request.POST.get('pin')
        max_members = request.POST.get('max_members')
        if pin:
            form = JoinLobby(data=request.POST)
            if form.is_valid():
                lobbyc = Lobby.objects.get(id=pin)
                response = _try_add_to_lobby(request)
                channel_layer = get_channel_layer()
                channel_name = 'lobby_%s' % lobbyc.id
                async_to_sync(channel_layer.group_send)(channel_name, {
                    'type': f'add_user', 'username': request.user.username, 'userid': request.user.id})
                return response

            else:
                data = {'form': form, 'lobby_form': LobbyForm(),
                        'error': form.errors}
                return render(request, 'lobby/lobby.html', data)

        elif max_members:
            _lobby = Lobby(id=randint(0, 9999), owner=user,
                           max_members=int(max_members), num_members=1)
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


class LobbyView(SafeView):
    ''' Lobby Page View '''
    template_name = 'lobby/lobby_template.html'
    this_lobby = None
    members = None
    owner = None
    form = None
    username = None
    channel_layer = get_channel_layer()
    channel_name = None

    def get(self, request, lobby_id=0, *args, **kwargs) -> HttpResponse:
        ''' Creates a form and returns a page render if the request method is GET '''
        self.form = AddTrackForm()
        try:
            self.set_data(request, lobby_id)
        except Lobby.DoesNotExist:
            return render(request, 'lobby/no_lobby.html')
        return self.display_page(request)

    def post(self, request, lobby_id=0, *args, **kwargs) -> HttpResponse:
        ''' Creates a form and validates it and also returns a page render if the request method is POST'''
        self.username = request.user.username
        data = dict(request.POST)
        leave = data.get('leave')
        to_unban = request.POST.getlist('to_unban')
        print(23123)
        username = data.get('username')
        try:
            self.set_data(request, lobby_id)
        except ObjectDoesNotExist:
            return redirect('/lobby')

        if username:
            ban_form = BanForm(data=request.POST)
            if ban_form.is_valid():
                self.send_websocket_data(type='send_lobby', username=username)
                self.this_lobby.ban_user(username)
        elif to_unban:
            lobby_id = int(request.POST.get('lobby_id'))
            channel_name = 'lobby_%s' % lobby_id
            async_to_sync(self.channel_layer.group_send)(
                channel_name, {'type': f'send_lobby', 'event':'unban', 'unbanned': to_unban})
        elif leave:
            return _leave_from_lobby(leave)
        elif request.POST.get('delete'):
            id_to_delete = request.POST.get('delete')
            if id_to_delete:
                if int(id_to_delete) == self.this_lobby.id:
                    self.this_lobby.delete()
                    return redirect('/lobby')

        return self.display_page(request)

    def set_data(self, request, lobby_id) -> None:
        ''' Sets the view data according to the request and the lobby '''
        self.username = request.user.username
        self.this_lobby = Lobby.objects.get(id=lobby_id)
        self.members = User.objects.filter(lobby_in=self.this_lobby)
        self.owner = self.this_lobby.owner
        self.channel_name = 'lobby_%s' % lobby_id
        api.refresh_user(self.owner)

    def display_page(self, request) -> HttpResponse:
        ''' Collects the view fields in the HttpResponse and checks the user's access to the lobby '''
        if request.user.lobby_in != self.this_lobby:
            return HttpResponse('Forbidden')
        if self.this_lobby:
            return render(request, self.template_name, self.get_page_data())
        else:
            raise Http404

    def get_page_data(self) -> dict:
        ''' Collect all data in one dict to '''
        track = Track(self.owner.oauth_token)
        history = self.this_lobby.history
        ban_list = self.this_lobby.ban_list.all()
        return {'section': 'lobby', 'lobby': self.this_lobby, 'members': self.members, 'track': track, 'form': self.form,
                'owner': self.owner.username, 'history': history, 'is_owner': (self.owner == self.request.user),
                'mmf': MaxMembersForm(num_members=3), 'ban_form': BanForm(), 'ban_list': ban_list}

    def send_websocket_data(self, **kwargs):
        async_to_sync(self.channel_layer.group_send)(self.channel_name, kwargs)


@login_required
def ajax_add_track(request) -> JsonResponse:
    if request.method == 'POST' and request.is_ajax():
        form = AddTrackForm(data=request.POST)
        if form.is_valid():
            link = request.POST['link']
            lobby_id = int(request.POST['add_to'])
            lobby = Lobby.objects.get(id=lobby_id)

            track = Track(lobby.owner.oauth_token, link)
            track.to_queue()

            channel_layer = get_channel_layer()
            channel_name = 'lobby_%s' % lobby.id
            async_to_sync(channel_layer.group_send)(channel_name, {
                'type': 'send_lobby', 'event': 'add_track', 'title': track.name, 'username': request.user.username})

            lobby.add_history(request.user.username, track.name)
            return JsonResponse({'title': track.name, 'username': request.user.username}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'errors': 'Not post or ajax'})


@login_required
def ajax_remove_members(request) -> JsonResponse:
    if request.method == 'POST' and request.is_ajax():
        to_delete = request.POST.getlist('to_delete')
        lobby_id = request.POST.get('lobby_id')
        lobby = Lobby.objects.get(id=lobby_id)

        channel_layer = get_channel_layer()
        channel_name = 'lobby_%s' % lobby.id
        async_to_sync(channel_layer.group_send)(channel_name, {
            'type': 'send_lobby', 'event': 'remove_members', 'to_delete': to_delete})

        lobby.remove_users(to_delete)
        if not isinstance(to_delete, list):
            to_delete = [to_delete]
        return JsonResponse({'to_delete': to_delete}, status=200)
    else:
        return JsonResponse({'errors': 'Not post or ajax'}, status=400)


@login_required
def ajax_ban_user(request) -> JsonResponse:
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['username']
        user = User.objects.get(username=username)
        lobby = request.user.lobby_in

        channel_layer = get_channel_layer()
        channel_name = 'lobby_%s' % lobby.id
        async_to_sync(channel_layer.group_send)(channel_name, {
            'type': 'send_lobby', 'event': 'ban', 'username': username, 'userid': user.id})

        ban_form = BanForm(data=request.POST)
        if ban_form.is_valid():
            lobby.ban_user(username)
            return JsonResponse({'username': username}, status=200)
    else:
        return JsonResponse({'errors': 'Not post or ajax'}, status=400)


@login_required
def ajax_unban_user(request) -> JsonResponse:
    if request.method == 'POST' and request.is_ajax():
        print(request.POST, 112)
        to_unban = request.POST.getlist('to_unban')
        lobby_id = int(request.POST.get('lobby_id'))
        lobby = Lobby.objects.get(id=lobby_id)

        channel_layer = get_channel_layer()
        channel_name = 'lobby_%s' % lobby_id
        async_to_sync(channel_layer.group_send)(
            channel_name, {'type': 'send_lobby', 'event': 'unban', 'unbanned': to_unban})

        lobby.unban_users(to_unban)
        return JsonResponse({'unbanned': to_unban}, status=200)
    else:
        return JsonResponse({'errors': 'Not post or ajax'}, status=400)
