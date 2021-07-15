''' Special fields for forms '''

from django import forms
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from backend.models import Lobby
from backend.utils import clear_track

class PinField(forms.Field):
    ''' Field for pin '''
    def to_python(self, value):
        ''' Attempts to convert the entered value to a number '''
        print('validatiooon', 1)
        if not value:
            raise ValidationError("Field is empty")
        try:
            return int(value)
        except ValueError:
            raise ValidationError("The entered value is not a number")
    def validate(self, value):
        ''' Checks if a lobby with this number exists '''
        super(PinField, self).validate(value)
        try:
            print('validatioooooon', 2)
            Lobby.objects.get(id=value)
            return value
        except ObjectDoesNotExist:
            raise ValidationError("There is no lobby with this number!")

class LinkField(forms.CharField):
    ''' Field for Spotify tracks links'''
    def validate(self, value):
        try:
            id = clear_track(value)
        except ValueError:
            raise ValidationError("Incorrect link")
        return value
            