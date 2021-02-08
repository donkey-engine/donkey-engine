from django.contrib import admin
from .models import Game
from servers.models import Server


# Models for admin panel
admin.site.register(Game)
admin.site.register(Server)
