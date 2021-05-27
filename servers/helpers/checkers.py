from urllib.parse import urlparse

from django.conf import settings
from mcstatus import MinecraftServer

from servers.helpers import adapters
from servers.models import Server


def check_minecraft_servers():
    for server in Server.objects.filter(status='RUNNING'):
        domain = urlparse(settings.HOST_NAME).netloc
        try:
            status = MinecraftServer.lookup(f'{domain}:{server.port}').status()
        except ConnectionRefusedError:
            adapters.stop_server(server.id)
        else:
            if not status.players.online:
                adapters.stop_server(server.id)
