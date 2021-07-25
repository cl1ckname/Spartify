from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.utils import track_full_name, clear_track, _make_devices_list
from .models import User
from lobby.lobby import Queue
from .spotify import api
from .forms import AddTrackForm


def user_login(request):

    return render(request, 'backend/login.html')


@login_required
def dashboard(request):
    user = request.user
    queue = Queue(request)
    api.refresh_user(user)
    token = user.oauth_token

    # if request.method == 'POST':
    #     link = request.POST['link']
    #     add_form = AddTrackForm(data=request.POST)
    #     if add_form.is_valid():
    #         uri = clear_track(link)
    #         api.add_queue(uri, token)
    #         queue.add(request.POST['link'], request.user.username)

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

    data = api.get_user_devices(user.oauth_token)

    devices_list = _make_devices_list(data)

    return render(request, 'backend/devices.html', {'devices_list': devices_list})


@login_required
def post_queue(request):
    if request.method == 'POST' and request.is_ajax():
        form = AddTrackForm(data = request.POST)
        if form.is_valid():
            queue = Queue(request)
            token = request.user.oauth_token
            link = request.POST['link']
            uri = clear_track(link)
            api.add_queue(uri, token)
            queue.add(request.POST['link'], request.user.username)
            track_id = clear_track(link)
            track_name = track_full_name(api.get_track(track_id, token))
            return JsonResponse({'title': track_name, 'username': request.user.username}, status=200)
        else:
            print(form.errors)
            return JsonResponse({'errors': form.errors}, status=400)