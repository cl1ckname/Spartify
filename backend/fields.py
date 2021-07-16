''' Special fields for forms '''

from django import forms
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from lobby.models import Lobby
from backend.utils import clear_track

class LinkField(forms.CharField):
    ''' Field for Spotify tracks links'''
    def validate(self, value):
        try:
            clear_track(value)
        except ValueError:
            raise ValidationError("Incorrect link")
        return value
            