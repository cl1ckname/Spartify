import re
from . import api

class Track:
    ''' Track class from Spotify.
        Params:
        - oauth - oauth token of user (requiered)
        - link - link to the track. if not transmitted, the currently playing track is used.
    '''
    link: str
    id: str
    image: str
    oauth: str
    def __init__(self, oauth: str, link: str = None):
        self.oauth = oauth
        if link:
            self.link = link
            self.id = self._clear_link(link)
            self._data = api.get_track(self.id, oauth)
        else:
            self._data = api.get_user_playback(oauth)
        self.title, self.artists = self._get_name_parts(self._data)
        if (self.title and self.artists):
            self.name = ', '.join(self.artists) + ' - ' + self.title
        else:
            self.name = ''

        if self._data:
            try:
                self.image = self._data['item']['album']['images'][0]['url']
            except KeyError:
                self.image = self._data['album']['images'][0]['url']

    def to_queue(self):
        print(self.id)
        api.add_queue(self.id, self.oauth)
    
    def show_artists(self):
        return ', '.join(self.artists)

    def _clear_link(self, link) -> str:
        ''' Returns id of track from link '''
        pattern = r'(https:\/\/open\.spotify\.com\/track\/)([0-9a-zA-Z]*)(\?si=[0-9a-z]*)'
        result = re.search(pattern, link)
        if not result:
            raise ValueError
        return result.group(2)

    def _get_name_parts(self, track: dict) -> tuple:
        ''' makes a good string - song title 
            track - response of SpotifyApi.get_track() or SpotifyApi.get_user_playback()'''
        if track:
            if 'item' in track.keys():
                artists = []
                for artist in track['item']['artists']:
                    artists.append(artist['name'])
                return track['item']['name'], artists
            else:
                artists = []
                for artist in track['artists']:
                    artists.append(artist['name'])
                return track['name'], artists
        else:
            return '', []
    
    def __str__(self):
        return self.name