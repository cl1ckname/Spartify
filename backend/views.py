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
from .spotify import SpotifyAPI

api = SpotifyAPI(settings.SOCIAL_AUTH_SPOTIFY_KEY, settings.SOCIAL_AUTH_SPOTIFY_SECRET)

def user_login(request):
    
    
    return render(request, 'backend/login.html')


@login_required
def dashboard(request):
    user = get_object_or_404(User, username=request.user.username)
    # user = api.refresh_user(user, 'http://localhost:8000')
    # user.save()
    token = user.oauth_token
    
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
    return render(request, 'backend/dashboard.html', {'section': 'dashboard', 'track': name})

def test(request):
    token = api.get_access_token()
    ac = request.user
    oauth = api.get_oauth(request.user.access_token, 'http://localhost:8000')
    oauth = request.user.oauth_token
    print(1)
    buf = "-------Getting acces token---------<br>"
    buf += api.get_access_token()
    print(2)
    buf += '<br>-------Search_track---------------<br>'
    buf += str(len(str(api.search('OCB'))))
    print(3)
    buf += '<br>---------Getting oauth----------<br>'
    buf += str(api.get_oauth(request.user.access_token, 'http://localhost:8000'))
    print(4)
    buf += '<br>---------Getting devices-----------<br>'
    buf += str(api.get_user_devices(oauth))
    print(5)
    buf += '<br>---------Getting current track------------<br>'
    buf += str(len(str(api.get_user_playback(oauth))))
    return HttpResponse(buf)

@login_required
def devices(request):
    data = api.get_user_devices(request.user.oauth_token)
    devices_list = data['devices']
    for i in devices_list:
        if i['is_active']:
            i['emoji'] = '⏩'
        else:
            i['emoji'] = '⏹'
    print(devices_list)
    return render(request, 'backend/devices.html', {'devices_list': devices_list})
