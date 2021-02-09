from django.contrib import admin

from games.models import Game


class GameAdmin(admin.ModelAdmin):
    """Change name game in admin panel"""
    list_display = ('name',)


admin.site.register(Game, GameAdmin)
