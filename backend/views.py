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
import requests
from .spotify import SpotifyAPI

api = SpotifyAPI(settings.SOCIAL_AUTH_SPOTIFY_KEY, settings.SOCIAL_AUTH_SPOTIFY_SECRET)

def user_login(request):
    
    
    return render(request, 'backend/login.html')


@login_required
def dashboard(request):
    user_token = request.user.oauth_token
    if len(user_token) > 10:
        track = api.get_user_playback(request.user.oauth_token)
        if track:
            name = track['item']['name']
        else:
            name = 'Nothing'
    else:
        name = 'No token!'
    return render(request, 'backend/dashboard.html', {'section': 'dashboard', 'track': name})

def get_code(request):
    try:
        user = get_object_or_404(User, username = request.user.username)
    except Http404:
        return HttpResponse('something goes worng')
    if request.method == 'GET':
        if 'code' in request.GET.keys():
            access_token = request.GET['code']
            token = api.get_oauth(access_token, 'http://localhost:8000/social/complete/spotify/')
            user.oauth_token = token
            user.save()
    return redirect('/')
