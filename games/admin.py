from django.contrib import admin
from .models import Game


class GameAdmin(admin.ModelAdmin):
    """Change name game in admin panel"""
    list_display = ('name',)


# Models for admin panel
admin.site.register(Game, GameAdmin)
