import base64
import datetime
import json
import requests as rq
from urllib.parse import quote


class SpotifyAPI(object):
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
        if self.client_secret == None or self.client_id == None:
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
        r = rq.post(self.url, data=data, headers=headers)
        token_response = r.json()
        if r.status_code not in range(200, 299):
            raise Exception('Authentificate failed')
        now = datetime.datetime.now()
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
        if expires < now or token == None:
            self.perform_auth()
            return self.access_token
        return token

    def search(self, query: str, search_type: str = 'track') -> dict:
        '''
        Searches for a track, playlist, album or artist by title and returns json from https://api.spotify.com/v1/search.
        query - part of title
        search_type - the type of object you are looking for. Possible values: album , artist, playlist, track, show and episode
        '''
        header = {
            'Authorization': f'Bearer {self.get_access_token()}'
        }

        endpoint = 'https://api.spotify.com/v1/search'
        data = quote(
            {'q': f'{query}', 'type': f'{search_type}', 'market': 'RU'})
        lookup = f'{endpoint}?{data}'
        r = rq.get(lookup, headers=header)
        if r.status_code in range(200, 299):
            return r.json()
        return {}

    def get_oauth(self, access_token: str, redirected_uri: str) -> str:
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

        if r.status_code not in range(200, 299):
            return ''

        return json.loads(r.content.decode())['access_token']

    def get_user_playback(self, oauth_token: str) -> dict:
        '''
        Makes a request for https://api.spotify.com/v1/me/player/currently-playing and returns the corresponding json.
        oauth_token - user token obtained using get_oauth()
        '''
        uri = 'https://api.spotify.com/v1/me/player/currently-playing'
        headers = {
            'Authorization': f'Bearer {oauth_token}'
        }
        r = rq.get(uri, headers=headers)

        if r.status_code not in range(200, 299):
            return {}

        content = r.content.decode()

        if content:
            return json.loads(r.content.decode())
        return {}

    def get_user_devices(self, oauth: str) -> dict:
        '''
        Makes a request for https://api.spotify.com/v1/me/player/devices and returns the corresponding json.
        '''
        uri = 'https://api.spotify.com/v1/me/player/devices'

        headers = {
            'Authorization': f'Bearer {oauth}'
        }

        r = rq.get(uri, headers=headers)

        if r.status_code not in range(200, 299):
            return {}

        return json.loads(r.content.decode())
