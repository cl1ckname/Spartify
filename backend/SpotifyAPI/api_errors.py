from requests import Response


class SpotifyError(Exception):
    ''' Errors related to Spotify API '''
    def __init__(self, response: Response):
        self.text = 'API Errror'
        self.endpoint = response.url
        self.status = response.status_code

    def __str__(self) -> str:
        return self.text

class AuthenticationError(SpotifyError):
    ''' Whenever the application makes requests related 
    to authentication or authorization to Web API, such 
    as retrieving an access token or refreshing an access 
    token, the error response follows RFC 6749 on the OAuth 2.0 Authorization Framework
    '''
    def __init__(self, response: Response):
        super(AuthenticationError, self).__init__(response)
        self.text = response.json()['error_description']


class RegularError(SpotifyError):
    ''' Apart from the response code, unsuccessful responses return a JSON object containing the following information '''
    def __init__(self, response):
        super(RegularError, self).__init__(response)
        self.text = response.json().get('message') or 'dibli-dubli'
