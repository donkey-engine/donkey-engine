from django.contrib import admin
from .models import Game
from servers.models import Server


class GmaeAdmin(admin.ModelAdmin):
    """Change name game in admin panel"""
    list_display = ('name',)


# Models for admin panel
admin.site.register(Game, GmaeAdmin)
admin.site.register(Server)
