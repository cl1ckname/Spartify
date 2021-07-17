from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import User

class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class Admin(UserAdmin):
    form = UserChangeForm
    model = User
    list_display = ('id','username','oauth_token', 'refresh_token', 'expires', 'lobby_in')
    # fieldsets = UserAdmin.fieldsets + ((None, {'fields': ("oauth_token",)}),)



admin.site.register(User, Admin)
