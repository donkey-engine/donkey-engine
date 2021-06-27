import logging
import typing as t
from pathlib import Path

import docker
from django.conf import settings

from servers.helpers import exceptions
from servers.models import Server, ServerBuild

logger = logging.getLogger(__name__)


class BaseRunner:  # FIXME https://github.com/donkey-engine/donkey-engine/issues/51
    """Base class for game image/container management."""
    def __init__(self, server_id: int):
        self.server_id: int = server_id
        self.server = Server.objects.get(id=server_id)
        self.client: docker.DockerClient = docker.from_env()
        self.directory: str = self._get_dockerfile_directory()

    def get_container_port(self, attempts=100) -> int:
        """Get container oper port."""
        for _ in range(attempts):
            for container in self.client.containers.list():
                if container.name != f'server{self.server_id}':
                    continue
                for port in container.ports.get('25565/tcp', []):
                    if not port['HostPort']:
                        continue
                    return int(port['HostPort'])
        raise exceptions.ServerNotRunning()

    def get_or_create_image(self) -> str:  # TODO add reuse existed images
        """Get or create docker image."""
        image, build_log = self.client.images.build(
            tag=f'server_build_{self.server_id}',
            path=self.directory,
            forcerm=True,
            nocache=True,
        )
        return image

    def stop(self) -> None:
        """Stop container."""
        for container in self.client.containers.list():
            if container.name == f'server{self.server_id}':
                container.stop()
                break
        self.server.port = 0
        self.server.status = 'STOPPED'
        self.server.save()
        build_instance = ServerBuild.objects.filter(
            server_id=self.server_id,
            kind='RUN',
        ).order_by('finished').last()
        if build_instance:
            build_instance.logs += '\nStopped'
            build_instance.save()

    def run(self) -> t.Optional[int]:
        """Run server."""
        build_instance = ServerBuild.objects.create(
            server_id=self.server_id,
            kind='RUN',
        )

        logs = []

        self.stop()
        try:
            image_name = self.get_or_create_image()
        except Exception as exc:
            logger.exception(exc)
            logs.append('Create Minecraft server image - Error')
            build_instance.success = False
            build_instance.logs = '\n'.join(logs)
            build_instance.save()
            return None
        else:
            logs.append('Create Minecraft server image - OK')

        try:
            self.client.containers.run(
                image_name,
                detach=True,
                volumes=[
                    f'{self.directory}:/home/app',
                ],
                ports={
                    '25565/tcp': None,
                },
                name=f'server{self.server_id}',
                remove=True,
                hostname=f'server{self.server_id}',
                mem_limit='2048M',
            )
        except Exception as exc:
            logger.exception(exc)
            logs.append('Staring Minecraft server - Error')
            build_instance.success = False
            build_instance.logs = '\n'.join(logs)
            build_instance.save()
            return None
        else:
            logs.append('Staring Minecraft server - OK')

        try:
            port = self.get_container_port()
        except Exception as exc:
            logger.exception(exc)
            logs.append('Checking Minecraft server - Error')
            build_instance.success = False
            build_instance.logs = '\n'.join(logs)
            build_instance.save()
            return None
        else:
            logs.append(f'Minecraft server port - {port}')
        build_instance.success = True
        build_instance.logs = '\n'.join(logs)
        build_instance.save()
        self.server.status = 'RUNNING'
        self.server.port = port
        self.server.save()
        return port

    def _get_dockerfile_directory(self) -> str:
        return str(
            Path(
                settings.BUILD_FILE_DIRECTORY.format(
                    server_id=self.server_id,
                )
            ).absolute()
        )
