from django import forms
from backend.fields import PinField, LinkField


class AddTrackForm(forms.Form):
    link = LinkField(required=True, label="Track link:",help_text="Input link on track")

class DeleteTrackForm(forms.Form):
    def __init__(self, id):
        super().__init__()

class JoinLobby(forms.Form):
    pin = PinField(required=True, label="Lobby PIN:", help_text="Ask your lobby owner the #PIN code")
