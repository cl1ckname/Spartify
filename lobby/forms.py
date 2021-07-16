from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from lobby.models import Lobby

class PinField(forms.Field):
    ''' Field for pin '''
    def to_python(self, value):
        ''' Attempts to convert the entered value to a number '''
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
            Lobby.objects.get(id=value)
            return value
        except ObjectDoesNotExist:
            raise ValidationError("There is no lobby with this number!")

class JoinLobby(forms.Form):
    pin = PinField(required=True, label="Lobby PIN:", help_text="Ask your lobby owner the #PIN code")
    class Meta:
        db_table = "lobby"