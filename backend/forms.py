from django import forms
from backend.fields import LinkField


class AddTrackForm(forms.Form):
    link = LinkField(required=True, label="Track link:",help_text="Input link on track")

