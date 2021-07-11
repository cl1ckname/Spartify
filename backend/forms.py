from django import forms

class AddTrackForm(forms.Form):
    link = forms.TimeField(required=True, label="Track link:",help_text="Input link on track")

class DeleteTrackForm(forms.Form):
    def __init__(self, id):
        super().__init__()