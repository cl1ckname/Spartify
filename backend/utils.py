''' Instruments that i use more than once '''

def track_full_name(track: dict) -> str:
    ''' makes a good string - song title 
        track - response of SpotifyApi.get_track() or SpotifyApi.get_user_playback()'''
    if 'item' in track.keys():
        print(track.keys())
        name = ''
        for artist in track['item']['artists']:
            name += artist['name'] + ', '
        name = name[:-2] + ' - ' + track['item']['name']
    elif track:
        print(track.keys())
        name = ''
        for artist in track['artists']:
            name += artist['name'] + ', '
        name = name[:-2] + ' - ' + track['name']
    else:
        name = 'Nothing'
    return name

def clear_track(link: str) -> str:
    ''' Returns id of track from link '''
    return link.split('track/')[1].split('?')[0]