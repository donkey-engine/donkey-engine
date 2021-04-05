from django.contrib import admin

from games.models import Game, Mods, Version


class GameAdmin(admin.ModelAdmin):  # type: ignore
    """Change name game in admin panel"""
    list_display = ('name',)


class VersionAdmin(admin.ModelAdmin):  # type: ignore
    """Change name version in admin panel"""
    list_display = ('version', 'game',)


class ModsAdmin(admin.ModelAdmin):  # type: ignore
    """Change name mods in admin panel"""
    list_display = ('name', 'game', 'version',)


admin.site.register(Game, GameAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Mods, ModsAdmin)
