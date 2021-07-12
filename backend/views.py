from django.shortcuts import render

from urllib.parse import quote
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from .models import User
import datetime
import requests
from .lobby import Queue
from .spotify import SpotifyAPI
from .forms import AddTrackForm

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
        add_form = AddTrackForm(data = request.POST)
        queue.add(request.POST['link'], request.user.username)
            

    if len(token) > 10:
        track = api.get_user_playback(token)
        if track:
            name = ''
            for artist in track['item']['artists']:
                name += artist['name'] + ', '
            name = name[:-2] + ' - ' + track['item']['name']
        else:
            name = 'Nothing'
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
    devices_list = data['devices']
    for i in devices_list:
        if i['is_active']:
            i['emoji'] = '⏩'
        else:
            i['emoji'] = '⏹'

    return render(request, 'backend/devices.html', {'devices_list': devices_list})



def add_track(request, track_id):
    track = get_object_or_404()
