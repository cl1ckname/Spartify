from django.db import models
from backend.models import User

class Lobby(models.Model):
    id = models.IntegerField(primary_key=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    history = models.JSONField(default=list, blank=True)

    def add(self, user):
        user.lobby_in = self
        user.save()
