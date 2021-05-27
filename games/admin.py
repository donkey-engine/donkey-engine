from django.contrib import admin

from games.models import Game, GameVersion, Mod


class VersionsInline(admin.TabularInline):  # type: ignore
    model = GameVersion
    extra = 1


class GameAdmin(admin.ModelAdmin):  # type: ignore
    """Change name game in admin panel"""
    list_display = ('name',)

    inlines = (VersionsInline,)


class ModAdmin(admin.ModelAdmin):  # type: ignore
    """Change name mods in admin panel"""
    list_display = ('name',)
    list_filter = ('name',)


admin.site.register(Game, GameAdmin)
admin.site.register(Mod, ModAdmin)
