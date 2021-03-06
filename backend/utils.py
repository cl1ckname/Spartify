''' Instruments that i use more than once '''

import re

def track_name_parts(track: dict) -> tuple:
    ''' makes a good string - song title 
        track - response of SpotifyApi.get_track() or SpotifyApi.get_user_playback()'''
    if 'item' in track.keys():
        name = ''
        for artist in track['item']['artists']:
            name += artist['name'] + ', '
        return (name[:-2], track['item']['name'])
    elif track:
        name = ''
        for artist in track['artists']:
            name += artist['name'] + ', '
        return name[:-2], track['name']
    else:
        return 'Nothing', None

def track_to_string(track: tuple):
    return track[0] + '-' + track[1]

def clear_track(link: str) -> str:
    ''' Returns id of track from link '''
    pattern = r'(https:\/\/open\.spotify\.com\/track\/)([0-9a-zA-Z]*)(\?si=[0-9a-z]*)?'
    result = re.search(pattern, link)
    if not result:
        raise ValueError
    return result.group(2)


def _make_devices_list(data) -> dict:
    """ Makes pretty device list """
    if "devices" not in data.keys():
        devices_list = ({'name': "Nothing", 'is_active': 0},)
    else:
        devices_list = data['devices']
    for i in devices_list:
        i['emoji'] = '⏩' if i['is_active'] else '⏹'
    return devices_list