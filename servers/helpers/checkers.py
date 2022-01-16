from datetime import datetime
from urllib.parse import urlparse

from django.conf import settings
from mcstatus import MinecraftServer

from common.clients.redis import client as redis
from common.clients.ws import client as ws
from common.clients.ws import get_user_room
from servers.helpers import adapters
from servers.models import Server

MAX_SERVER_FAILURES = 3
MAX_SERVER_EMPTINESS = 6
KEY_EXPIRING = 60 * 60


def check_minecraft_servers():
    for server in Server.objects.filter(status='RUNNING', game__build_key='Minecraft: Java Edition'):
        domain = urlparse(settings.HOST_NAME).netloc

        try:
            status = MinecraftServer.lookup(f'{domain}:{server.port}').status()
            # FIXME socket.timeout | BrokenPipeError
        except ConnectionRefusedError:
            redis_failure_key = f'servers:{server.id}:failures'
            redis.sadd(
                redis_failure_key,
                int(datetime.now().timestamp()),
            )
            redis.expire(
                redis_failure_key,
                KEY_EXPIRING,
            )
            failures_set = redis.smembers(redis_failure_key)
            if len(failures_set) >= MAX_SERVER_FAILURES:
                adapters.stop_server(server.id)
                ws.new_event(
                    get_user_room(server.owner.id),
                    {
                        'type': 'SERVERS',
                        'data': {
                            'server_id': server.id,
                            'status': 'STOPPED',
                        },
                    }
                )
        else:
            redis_emptiness_key = f'servers:{server.id}:emptiness'
            if status.players.online:
                redis.delete(redis_emptiness_key)
            else:
                redis.sadd(
                    redis_emptiness_key,
                    int(datetime.now().timestamp()),
                )
                redis.expire(
                    redis_emptiness_key,
                    KEY_EXPIRING,
                )
                emptiness_set = redis.smembers(redis_emptiness_key)
                if len(emptiness_set) >= MAX_SERVER_EMPTINESS:
                    adapters.stop_server(server.id)
                    ws.new_event(
                        get_user_room(server.owner.id),
                        {
                            'type': 'SERVERS',
                            'data': {
                                'server_id': server.id,
                                'status': 'STOPPED',
                            },
                        }
                    )
