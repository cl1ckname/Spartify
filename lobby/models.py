import datetime
import shortuuid
from django.core.exceptions import ValidationError
from django.db import models
from backend.models import User
from shortuuidfield import ShortUUIDField

uid_generator = shortuuid.ShortUUID(
    alphabet='1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ')
def _get_short_uuid():
    return str(uid_generator.uuid())[:5]

class Lobby(models.Model):
    id = ShortUUIDField(primary_key=True, default = _get_short_uuid)
    password = models.CharField(max_length=12, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    history = models.JSONField(default=list, blank=True)
    num_members = models.PositiveIntegerField("num_members")
    max_members = models.PositiveIntegerField("max_members")
    ban_list = models.ManyToManyField(User, related_name="ban", blank=True)
    settings = models.JSONField(default={'num_members': 1, 'max_members': 5, 'ban_list': []})

    def add_user(self, user):
        """ Add user to lobby if it possible"""
        if self.num_members < self.max_members:
            if not self.ban_list.filter(id = user.id):
                self.num_members += 1
                user.lobby_in = self
                user.save()
                self.save()
            else:
                raise ValidationError("You are banned here", code='invalid')
        else:
            raise ValidationError("Lobby is full! Max members: %(max_members)s", params={'max_members': self.max_members})
    
    def remove_users(self, users: list):
        ''' Removes users from lobby '''
        for id in users:
            user = User.objects.get(id=int(id))
            if user.lobby_in == self:
                user.lobby_in = None
                user.save()
    
    def ban_user(self, username: str):
        ''' Ban user in lobby '''
        user = User.objects.get(username = username)
        if user.lobby_in == self:
            user.lobby_in = None
            user.save()
        self.ban_list.add(user)
        self.save()
    
    def add_history(self, username: str, title: str):
        ''' Adds track information to the lobby history '''
        to_json = {'title': title, 'time': datetime.datetime.now(
        ).strftime('%H:%M'), 'user': username}
        if len(self.history) > 9:
            self.history = self.history[0:9]  #max len of history - 10 tracks
        self.history = [to_json] + self.history
        self.save()

    def unban_users(self, to_unban: list):
        ''' Add users to ban list and removes his from lobby '''
        try:
            for user_id in to_unban:
                user = User.objects.get(id=int(user_id))
                self.ban_list.remove(user)
        except User.DoesNotExist:
            raise ValidationError("Unban error")
    
    def leave(self, member: User):
        self.num_members -= 1
        member.lobby_in = None
        self.save()
        member.save()