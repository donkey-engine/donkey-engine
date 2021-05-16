from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User

from accounts.models import Profile
from servers.models import Server


class UserServersInline(admin.StackedInline):  # type: ignore
    model = Server
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ('game',)
    readonly_fields = ('game',)


class ProfileInline(admin.StackedInline):  # type: ignore
    model = Profile
    can_delete = False
    fields = ('email_confirmed',)


class NewUserAdmin(UserAdmin):
    inlines = (UserServersInline, ProfileInline)


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, NewUserAdmin)
