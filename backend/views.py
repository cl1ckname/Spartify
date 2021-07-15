from datetime import datetime
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import requests
from backend.utils import track_full_name, clear_track
from .models import Lobby, User
from .lobby import Queue
from .spotify import SpotifyAPI
from .forms import AddTrackForm, JoinLobby


api = SpotifyAPI(settings.SOCIAL_AUTH_SPOTIFY_KEY,
                 settings.SOCIAL_AUTH_SPOTIFY_SECRET)


def user_login(request):

    return render(request, 'backend/login.html')


@login_required
def dashboard(request):
    user = get_object_or_404(User, username=request.user.username)
    queue = Queue(request)
    api.refresh_user(user)
    token = user.oauth_token

    if request.method == 'POST':
        link = request.POST['link']
        add_form = AddTrackForm(data=request.POST)
        if add_form.is_valid():
            uri = clear_track(link)
            api.add_queue(uri, token)
            queue.add(request.POST['link'], request.user.username)

    if len(token) > 10:
        track = api.get_user_playback(token)
        name = track_full_name(track)
    else:
        name = 'No token!'
    form = AddTrackForm()
    names = []
    for link in queue.get_links():
        resp = api.get_track(link, token)
        title = track_full_name(resp)
        names.append(title)

    info = zip(names, queue.get_times(), queue.get_users())
    return render(request, 'backend/dashboard.html', {'section': 'dashboard', 'track': name, 'form': form,
                                                      'info': info, 'queue': queue})


@login_required
def devices(request):
    user = request.user
    api.refresh_user(user)
    print(user.oauth_token)

    if request.method == "POST":
        print(request.POST)

    data = api.get_user_devices(request.user.oauth_token)
    if "devices" not in data.keys():
        data['devices'] = ({'name': "Nothing", 'is_active': 0},)
    devices_list = data['devices']
    for i in devices_list:
        if i['is_active']:
            i['emoji'] = '⏩'
        else:
            i['emoji'] = '⏹'
    return render(request, 'backend/devices.html', {'devices_list': devices_list})


@login_required
def lobby(request):
    user = request.user
    if request.method == "POST":
        pin = request.POST['pin']
        form = JoinLobby(data=request.POST)
        if form.is_valid():
            user.lobby_in = Lobby.objects.get(id=pin)
            user.save()
            return redirect('/lobby/'+pin)
    else:
        form = JoinLobby()
    if not user.lobby_in:
        return render(request, 'backend/lobby.html', {'form': form})
    else:
        return redirect('lobby/'+str(user.lobby_in.id))


class LobbyView(TemplateView):
    ''' Lobby Page View '''
    template_name = "backend/lobby_template.html"
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
        data = request.POST
        self.set_data(request, lobby_id)
        self.form = AddTrackForm(data=data)
        link = requests.POST['link']
        token = request.user.oauth_token
        if self.form.is_valid():
            uri = clear_track(link)
            api.add_queue(uri, token)
            self.add_history(request, data)

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
            return render(request, self.template_name, {'id': self.this_lobby.id, 'members': self.members, 'track': name, 'form': self.form,
                                                        'owner': self.owner.username, 'history': history})
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
