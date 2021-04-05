from django.contrib import admin

from servers.models import Server, ServerBuild


class ServerAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ('owner', 'game', 'status')
    list_filter = ('owner', 'game', 'status')


class ServerBuildAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ('server', 'status', 'started', 'finished')
    list_filter = ('server', 'status')


admin.site.register(Server, ServerAdmin)
admin.site.register(ServerBuild, ServerBuildAdmin)
