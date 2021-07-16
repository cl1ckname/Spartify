''' Instruments that i use more than once '''

import re
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from lobby.models import Lobby


def track_full_name(track: dict) -> str:
    ''' makes a good string - song title 
        track - response of SpotifyApi.get_track() or SpotifyApi.get_user_playback()'''
    if 'item' in track.keys():
        name = ''
        for artist in track['item']['artists']:
            name += artist['name'] + ', '
        name = name[:-2] + ' - ' + track['item']['name']
    elif track:
        name = ''
        for artist in track['artists']:
            name += artist['name'] + ', '
        name = name[:-2] + ' - ' + track['name']
    else:
        name = 'Nothing'
    return name


def clear_track(link: str) -> str:
    ''' Returns id of track from link '''
    pattern = r'(https:\/\/open\.spotify\.com\/track\/)([0-9a-zA-Z]*)(\?si=[0-9a-z]*)'
    result = re.search(pattern, link)
    if not result:
        raise ValueError
    return result.group(2)


def _add_to_lobby(user, lobby_pin):
    user.lobby_in = Lobby.objects.get(id=lobby_pin)
    user.save()


def _make_devices_list(data):
    if "devices" not in data.keys():
        devices_list = ({'name': "Nothing", 'is_active': 0},)
    else:
        devices_list = data['devices']
    for i in devices_list:
        i['emoji'] = '⏩' if i['is_active'] else '⏹'
    return devices_list