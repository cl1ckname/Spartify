from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from lobby.models import Lobby
from backend.models import User


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
            lobby = Lobby.objects.get(id=value)
            if lobby.num_members >= lobby.max_members:
                raise ValidationError("Lobby is full. Max members: %(max_members)s", params={'max_members': lobby.max_members})
            return value
        except ObjectDoesNotExist:
            raise ValidationError("There is no lobby with this number!")


class JoinLobby(forms.Form):
    pin = PinField(required=True, label="Lobby PIN:",
                   help_text="Ask your lobby owner the #PIN code")

    class Meta:
        db_table = "lobby"


class LobbyForm(forms.ModelForm):

    class Meta:
        model = Lobby
        fields = ("max_members",)


class MaxMembersForm(forms.Form):
    def __init__(self, num_members=5, *args, **kwargs):
        super(MaxMembersForm, self).__init__(*args, **kwargs)
        self.num_members = num_members

        self.fields['max_members'] = forms.IntegerField(min_value=num_members, label='Max members:',
                                                        help_text='The max (abbreviated sup; plural suprema) of a subset S of a partially ordered set'
                                                        ' T is the least element in T that is greater than or equal to all elements of S, if'
                                                        ' such an element exists. Consequently, the max is also referred to as the least upper bound')


class BanForm(forms.Form):
    ''' Form containing a field for username '''
    def validate(value):
        ''' Validator for validate username '''
        try:
            user = User.objects.get(username=value)
        except ObjectDoesNotExist:
            raise ValidationError("There is no user with such username")
    username = forms.CharField(max_length=30, label="", validators=(validate,))
