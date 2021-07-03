from datetime import datetime

import docker

from common.clients.redis import client as redis
from common.clients.ws import client as ws
from common.clients.ws import get_user_room
from servers.models import Server, ServerBuild

LOGS_LOCK_REDIS_KEY = 'servers:logs-lock'
LOGS_LOCK_REDIS_EXPIRE = 5 * 60


def get_logs():
    if redis.get(LOGS_LOCK_REDIS_KEY):
        return

    docker_client = docker.from_env()

    try:
        # Redis lock
        redis.incr(LOGS_LOCK_REDIS_KEY)
        redis.expire(LOGS_LOCK_REDIS_KEY, LOGS_LOCK_REDIS_EXPIRE)

        for server in Server.objects.filter(status='RUNNING'):
            # Get ServerBuild for this server
            build_instance = ServerBuild.objects.filter(
                server_id=server.id,
                kind='RUN',
            ).order_by('finished').last()

            if not build_instance:
                continue

            # Get server container
            server_container = None
            for container in docker_client.containers.list():
                if container.name == f'server{server.id}':
                    server_container = container
                    break

            if not server_container:
                continue

            redis_last_logs_key = f'builds:{build_instance.id}:logs:timestamp'

            if not redis.get(redis_last_logs_key):
                redis.set(redis_last_logs_key, 1)

            redis.expire(redis_last_logs_key, 60 * 60)

            # Get logs
            now = int(datetime.now().timestamp())
            logs = server_container.logs(
                stream=False,
                since=int(redis.get(redis_last_logs_key)),
            )
            redis.set(redis_last_logs_key, now)

            # Send logs to WebSocket server
            ws.new_event(
                get_user_room(server.owner.id),
                {
                    'type': 'LOGS',
                    'data': {
                        'server_id': server.id,
                        'logs': logs.decode('UTF-8'),
                    },
                }
            )

            # Save logs to db
            build_instance.logs += logs.decode('UTF-8')
            build_instance.save()

    finally:
        # Release lock
        redis.expire(LOGS_LOCK_REDIS_KEY, 3)
