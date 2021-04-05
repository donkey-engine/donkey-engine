from django.contrib import admin

from games.models import Game, Mods, Version


class VersionsInline(admin.TabularInline):  # type: ignore
    model = Version
    extra = 1


class GameAdmin(admin.ModelAdmin):  # type: ignore
    """Change name game in admin panel"""
    list_display = ('name',)

    inlines = (VersionsInline,)


class ModsAdmin(admin.ModelAdmin):  # type: ignore
    """Change name mods in admin panel"""
    list_display = ('name', 'game', 'version',)
    list_filter = ('game',)


admin.site.register(Game, GameAdmin)
admin.site.register(Mods, ModsAdmin)
