''' Instruments that i use more than once '''

import re
from lobby.models import Lobby

class LobbyIsFull(Exception):
    def __init__(self, max_members, *args):
        self.max_members = max_members
    def __str__(self):
        return f"Lobby is full! Max members: {self.max_members}"

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
    """ Add user to lobby if it possible"""
    lobby = Lobby.objects.get(id=lobby_pin)
    if lobby.num_members < lobby.max_members:
        lobby.num_members += 1
        user.lobby_in = lobby
        user.save()
        lobby.save()
    else:
        raise LobbyIsFull(lobby.max_members)


def _make_devices_list(data) -> dict:
    """ makes pretty device list """
    if "devices" not in data.keys():
        devices_list = ({'name': "Nothing", 'is_active': 0},)
    else:
        devices_list = data['devices']
    for i in devices_list:
        i['emoji'] = '⏩' if i['is_active'] else '⏹'
    return devices_list