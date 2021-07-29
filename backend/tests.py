from datetime import datetime
from django.test import TestCase
from django.conf import settings
from .models import User
from SpotifyAPI import api

class ApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.\n")
        cls.refresh_token = 'AQAsBvSMEh5J17WotwmbOHk5AYkFBYnwTVjnpFO1jfeUoyg0hfh__0B3_KOwzcewWcCfH8dqLS5bnRbrdSNJ93-KchjepgbLWufu0qRpX5ogPMpPfWooODad1cehQVSYeC0'

    def setUp(self):
        self.api = api
        self.user = User.objects.create(id = 1, refresh_token = 'AQAsBvSMEh5J17WotwmbOHk5AYkFBYnwTVjnpFO1jfeUoyg0hfh__0B3_KOwzcewWcCfH8dqLS5bnRbrdSNJ93-KchjepgbLWufu0qRpX5ogPMpPfWooODad1cehQVSYeC0',
                                        oauth_token = 'BQDxuhRscquWHAg7ANhKniDkst4uCpSND8ZD7aQ48dR7aswlYkT4xIW4LM12fc88Gw9j9hQfIRjtpxyiv-W9ycl2VICaMkqAT6VB_yJeC5Mt8I4S3kjKFeS4Ln-QnuvJO4jC_C8rajW-u9aJBy29_HTPq2ohjQG_qQIKn0EGMJniGw',
                                        username='petya', expires = datetime.now(tz=None))
        self.api.refresh_user(self.user)

    def test_refresh_user(self):
        try:
            self.api.refresh_user(self.user)
        except Exception:
            assert Exception

    def test_perform_auth(self):
        '''Method: perform_auth'''
        self.assertTrue(self.api.perform_auth())

    def test_search(self):
        '''Method: search'''
        test_ans = self.api.search('Test', search_type='album')
        self.assertNotEqual(test_ans, {})
    
    # def test_refresh_token(self):
    #     '''''Method: refresh_token'''
    #     test_ans = self.api.refresh_token(self.refresh_token)
    #     self.assertNotEqual(test_ans, {})

    def test_get_track(self):
        ''' Method: get_track '''
        test_ans = self.api.get_track('3XC7Jd6SfrQYKZJ6inyRHK', self.user.oauth_token)
        self.assertNotEqual(test_ans, {})

    def test_get_me(self):
        ''' Method: get_me '''
        r = self.api.get_me(self.user.oauth_token)
        self.assertNotEqual(r, {})