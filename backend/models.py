from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect




class User(AbstractUser):
    '''Extended standard user class that stores information necessary to work with Spotify API'''
    id = models.AutoField(primary_key=True)
    access_token = models.CharField('oauth_token', max_length=250)
    oauth_token = models.CharField('oauth_token', max_length=250)
    refresh_token = models.CharField('refresh_token', max_length=250)
    expires = models.DateTimeField('expires', auto_now_add=True)
    device_id = models.CharField('device_id', max_length=50)
    lobby_in = models.ForeignKey('Lobby', null=True ,on_delete=models.SET_NULL)

class Lobby(models.Model):
    id = models.IntegerField(primary_key=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    history = models.JSONField(default=list, blank=True)

    def add(self, user):
        user.lobby_in = self
        user.save()

