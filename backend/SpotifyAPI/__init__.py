''' A package for using api spotify. Contains an api object that gets the user code and secret code from the project settings. '''

import base64
import datetime
import json
from django.conf import settings
from django.utils.timezone import make_aware
import requests as rq
from urllib.parse import quote
from requests.models import Response
from .api_errors import AuthenticationError, RegularError

def check_response(func):
    ''' Returns content of response or raise API error'''
    def new_f(self, *args, **kwargs) -> dict:
        r = func(self, *args, **kwargs)
        if r.status_code not in range(200, 299):
            if r.status_code == 401:
                raise AuthenticationError(r)
            raise RegularError(r)
        content = r.content.decode()
        if content:
            return json.loads(content)
        return {}
    return new_f

class SpotifyAPI(object):
    '''
    Api class. No more documentation yet
    '''
    acces_token = None
    acces_token_expires = datetime.datetime.now()
    acces_token_did_expire = True
    client_id = None
    client_secret = None

    def __init__(self, client_id: str, client_secret: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_creditales(self) -> str:
        '''
        Returns a base64 encoded string
        '''
        if self.client_secret is None or self.client_id is None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f'{self.client_id}:{self.client_secret}'
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def perform_auth(self) -> bool:
        '''
        Try to get and save client credentials access token. 
        Returns true on success or false.
        '''
        url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'client_credentials'
        }
        headers = {
            'Authorization': f'Basic {self.get_client_creditales()}'
        }
        r = rq.post(url, data=data, headers=headers)
        token_response = r.json()
        if r.status_code not in range(200, 299):
            raise Exception('Authentificate failed')
        now = make_aware(datetime.datetime.now())
        self.acces_token = token_response['access_token']
        expire_in = token_response['expires_in']
        self.acces_token_expires = now + datetime.timedelta(seconds=expire_in)
        self.acces_token_did_expire = self.acces_token_expires < now
        return True

    def get_access_token(self) -> str:
        '''
        An interface for obtaining an access token. Retrieves the token if the current one has expired. Returns the access token.
        '''
        token = self.acces_token
        expires = self.acces_token_expires
        now = datetime.datetime.now()
        if expires < now or token is None:
            self.perform_auth()
            return self.acces_token
        return token

    @check_response
    def search(self, query: str, search_type: str = 'track', *args, **kwargs) -> Response:
        '''
        Searches for a track, playlist, album or artist by title and returns json from https://api.spotify.com/v1/search.
        query - part of title
        search_type - the type of object you are looking for. Possible values: album , artist, playlist, track, show and episode
        '''
        header = {
            'Authorization': f'Bearer {self.get_access_token()}'
        }
        lookup = 'https://api.spotify.com/v1/search?q={}&type={}&market=RU'.format(query, search_type)
        r = rq.get(lookup, headers=header)
        return r

    @check_response
    def get_oauth(self, access_token: str, redirected_uri: str) -> Response:
        '''
        Makes a request for https://accounts.spotify.com/api/token and returns the user's oauth token.
        access_token - the token received by the corresponding request to https://accounts.spotify.com/api/token
        redirected_uri - a valid redirection path. Set in the settings of the Spotify app
        '''
        uri = 'https://accounts.spotify.com/api/token'

        headers = {
            'Authorization': 'Basic MThmNDkxNGQ3NzE4NGI2NzgwZTgzNmFkOWQ4ZjY4NGM6YTY0NWI2NTVjYTEzNGNlYzllNDRiZTE5NDNmMDJhNjQ=',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'authorization_code',
            'code': access_token,
            'redirect_uri': redirected_uri
        }

        r = rq.post(uri, data, headers=headers)
        return r

    @check_response
    def refresh_token(self, refresh_token) -> Response:
        uri = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': f'Basic {self.get_client_creditales()}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type':'refresh_token',
            'refresh_token': refresh_token
        }
        r = rq.post(uri, data=data, headers=headers)
        print(r.text)
        print(refresh_token)
        return r

    @check_response
    def get_user_playback(self, oauth_token: str) -> Response:
        '''
        Makes a request for https://api.spotify.com/v1/me/player/currently-playing and returns the corresponding json.
        oauth_token - user token obtained using get_oauth()
        '''
        uri = 'https://api.spotify.com/v1/me/player/currently-playing'
        headers = {
            'Authorization': f'Bearer {oauth_token}'
        }
        r = rq.get(uri, headers=headers)
        return r

    @check_response
    def get_user_devices(self, oauth: str) -> Response:
        '''
        Makes a request for https://api.spotify.com/v1/me/player/devices and returns the corresponding json.
        '''
        uri = 'https://api.spotify.com/v1/me/player/devices'

        headers = {
            'Authorization': f'Bearer {oauth}'
        }

        r = rq.get(uri, headers=headers)
        return r

    @check_response
    def get_track(self, id, oauth):
        ''' Makes a request for https://api.spotify.com/v1/tracks/ and returns the information about track'''
        lookup = f'https://api.spotify.com/v1/tracks/{id}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {oauth}'
        }
        r = rq.get(lookup, headers=headers)
        return r

    @check_response
    def add_queue(self, uri:str, oauth:str):
        ''' Add track in user player queue '''
        endpoint = f'https://api.spotify.com/v1/me/player/queue?uri={quote("spotify:track:"+uri, safe="")}'
        headers = {
            'Authorization': f'Bearer {oauth}'
        }
        data = {
            'uri': 'spotify:track:'+uri,
        }
        r = rq.post(endpoint, headers=headers, data=data)
        return r

    @check_response
    def get_me(self, oauth: str):
        ''' get information about user '''
        endpoint = 'https://api.spotify.com/v1/me'
        headers = {
            'Authorization': f'Bearer {oauth}'
        }
        r = rq.get(endpoint, headers=headers)
        return r

    def refresh_user(self, user) -> None:
        ''' Checks if the user's token has expired and refreshes it if necessary '''
        print(1, user.username, user.refresh_token)
        if user.expires.replace(tzinfo=None) < datetime.datetime.now(tz=None):
            refresh_data = self.refresh_token(user.refresh_token)
            print(2)
            user.oauth_token = refresh_data['access_token']
            user.expires = make_aware(datetime.datetime.now(tz=None)) + datetime.timedelta(seconds=refresh_data['expires_in'])
            user.save()

api = SpotifyAPI(settings.SOCIAL_AUTH_SPOTIFY_KEY,
                 settings.SOCIAL_AUTH_SPOTIFY_SECRET)