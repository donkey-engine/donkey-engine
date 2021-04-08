from django.contrib import admin

from games.models import Game, GameVersion, Mod, ModVersion


class VersionsInline(admin.TabularInline):  # type: ignore
    model = GameVersion
    extra = 1


class GameAdmin(admin.ModelAdmin):  # type: ignore
    """Change name game in admin panel"""
    list_display = ('name',)

    inlines = (VersionsInline,)


class ModVersionInline(admin.TabularInline):  # type: ignore
    model = ModVersion
    extra = 1


class ModAdmin(admin.ModelAdmin):  # type: ignore
    """Change name mods in admin panel"""
    list_display = ('name', 'game')
    list_filter = ('game',)

    inlines = (ModVersionInline,)


admin.site.register(Game, GameAdmin)
admin.site.register(Mod, ModAdmin)
