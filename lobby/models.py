from django.db import models
from backend.models import User

class Lobby(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    history = models.JSONField(default=list, blank=True)
    num_members = models.PositiveIntegerField("num_members")
    max_members = models.PositiveIntegerField("max_members")
    ban_list = models.ManyToManyField(User, related_name="ban", blank=True)
    settings = models.JSONField(default={'num_members': 1, 'max_members': 5, 'ban_list': []})

    def add(self, user):
        user.lobby_in = self
        user.save()
