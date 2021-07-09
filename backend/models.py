from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    access_token = models.CharField('oauth_token', max_length=250)
    oauth_token = models.CharField('oauth_token', max_length=250)
    refresh_token = models.CharField('refreash_token', max_length=250)
    expires = models.DateTimeField('expires', auto_now_add=True)