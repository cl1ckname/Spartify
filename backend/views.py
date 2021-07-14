from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from backend.utils import track_full_name, clear_track
from .models import Lobby, User
from .lobby import Queue
from .spotify import SpotifyAPI
from .forms import AddTrackForm, JoinLobby


api = SpotifyAPI(settings.SOCIAL_AUTH_SPOTIFY_KEY, settings.SOCIAL_AUTH_SPOTIFY_SECRET)

def user_login(request):
    
    
    return render(request, 'backend/login.html')


@login_required
def dashboard(request):
    user = get_object_or_404(User, username=request.user.username)
    queue = Queue(request)
    api.refresh_user(user)
    token = user.oauth_token
    
    if request.method == 'POST':
        # add_form = AddTrackForm(data = request.POST)
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
        title = ''
        for artist in resp['artists']:
            title += artist['name'] + ', '
        title = title[:-2] + ' - ' + resp['name']
        names.append(title)

    info = zip(names, queue.get_times(), queue.get_users())
    return render(request, 'backend/dashboard.html', {'section': 'dashboard', 'track': name, 'form': form,
                                                      'info': info, 'queue': queue})

@login_required
def devices(request):
    user = request.user
    api.refresh_user(user)

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
    form = JoinLobby()
    user = request.user
    if not user.lobby_in:
        return render(request, 'backend/lobby.html', {'form': form})
    else:
        return redirect('lobby/'+str(user.lobby_in.id))



class LobbyView(TemplateView):
    template_name = "backend/lobby_template.html"
    def get(self, request, lobby_id=0, *args, **kwargs):
        if lobby_id:
            this_lobby = Lobby.objects.get(id=lobby_id)
            members = User.objects.filter(lobby_in=this_lobby)
            owner = this_lobby.owner
            api.refresh_user(owner)

            form = AddTrackForm()
            track = api.get_user_playback(owner.oauth_token)
            history = this_lobby.history

            name = track_full_name(track)

            if this_lobby:
                return render(request, self.template_name, {'id': lobby_id, 'members': members, 'track': name, 'form': form,
                                                            'owner': owner.username, 'history': history})
            else:
                raise Http404
        else:
            raise Http404
    def post(self, request, lobby_id=0, *args, **kwargs):
        if lobby_id:
            data = request.POST
            this_lobby = Lobby.objects.get(id=lobby_id)
            owner = this_lobby.owner
            api.refresh_user(owner)
            members = User.objects.filter(lobby_in=this_lobby)
            track_id = clear_track(data['link'])
            track_raw = api.get_track(track_id, owner.oauth_token)
            to_json = {'title': track_full_name(track_raw), 'time': datetime.now().strftime('%H:%M'), 'user': request.user.username}
            this_lobby.history.append(to_json)
            this_lobby.save()
            
            form = AddTrackForm()
            track = api.get_user_playback(owner.oauth_token)
            history = this_lobby.history

            name = track_full_name(track)

            if this_lobby:
                return render(request, self.template_name, {'id': lobby_id, 'members': members, 'track': name, 'form': form,
                                                            'owner': owner.username, 'history': history})
            else:
                raise Http404
        else:
            raise Http404

def lobby_redirect(request):
    pin = request.GET['pin']
    try:
        lobby = get_object_or_404(Lobby, id=pin)
        request.user.lobby_in = lobby
        request.user.save()
    except Http404:
        return redirect('lobby')
    return redirect('lobby/'+pin)