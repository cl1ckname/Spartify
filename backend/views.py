from django.contrib.auth import logout
from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.SpotifyAPI.tracks import Track
from backend.utils import _make_devices_list
from lobby.queue import Queue
from backend.SpotifyAPI import api
from .forms import AddTrackForm


def user_login(request):
    return render(request, 'backend/login.html')


def user_logout(request):
    logout(request)
    return render(request, 'backend/logout.html')


@login_required
def dashboard(request):
    user = request.user
    queue = Queue(request)
    api.refresh_user(user)
    token = user.oauth_token

    if token:
        track = Track(token)
        user_info = api.get_me(token)
    else:
        raise Exception('No TOKEN')

    form = AddTrackForm()

    info = zip(queue.get_names(), queue.get_times(), queue.get_users())
    return render(request, 'backend/dashboard.html', {'section': 'dashboard', 'track': track, 'form': form,
                                                      'info': info, 'user_info': user_info})


@login_required
def devices(request):
    user = request.user
    api.refresh_user(user)

    if request.method == "POST":
        print(request.POST)

    data = api.get_user_devices(user.oauth_token)

    devices_list = _make_devices_list(data)

    return render(request, 'backend/devices.html', {'section': 'devices', 'devices_list': devices_list})


@login_required
def post_queue(request):
    print(132132131)
    print(request.method == 'POST', request.is_ajax())
    username = request.user.username
    if request.method == 'POST' and request.is_ajax():
        form = AddTrackForm(data=request.POST)
        if form.is_valid():
            queue = Queue(request)
            token = request.user.oauth_token
            link = request.POST['link']

            track = Track(token, link)
            track.to_queue()
            queue.add(track.name, username)

            return JsonResponse({'title': track.name, 'username': username}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)


def authentication_error(request):
    logout(request)
    return render(request, 'backend/authentication_error.html')


def handler500er(request):
    logout(request)
    return render(request, 'backend/error_500.html')

def handler400(request):
    logout(request)
    return render(request, 'backend/error_500.html')