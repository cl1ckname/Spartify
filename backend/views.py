from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404
from backend.utils import track_full_name, clear_track, _make_devices_list
from .models import User
from lobby.lobby import Queue
from .spotify import api
from .forms import AddTrackForm


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

    if request.method == "POST":
        print(request.POST)

    data = api.get_user_devices(request.user.oauth_token)

    devices_list = _make_devices_list(data)

    return render(request, 'backend/devices.html', {'devices_list': devices_list})

