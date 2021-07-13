from django import forms

class AddTrackForm(forms.Form):
    link = forms.CharField(required=True, label="Track link:",help_text="Input link on track")

class DeleteTrackForm(forms.Form):
    def __init__(self, id):
        super().__init__()

class JoinLobby(forms.Form):
    pin = forms.IntegerField(required=True, label="q", help_text="Ask your lobby owner the #PIN code")