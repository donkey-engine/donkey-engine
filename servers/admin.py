from django.contrib import admin

from servers.models import Server


class ServerAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ('owner', 'game')
    list_filter = ('owner', 'game')


admin.site.register(Server, ServerAdmin)
