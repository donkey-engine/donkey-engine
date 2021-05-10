from pathlib import Path

import docker
from django.conf import settings

from servers.helpers import exceptions

CONTAINER_NAME_TEMPLATE = ''
IMAGE_NAME_TEMPLATE = ''


class BaseRunner:  # FIXME https://github.com/donkey-engine/donkey-engine/issues/51
    """Base class for game image/container management."""
    def __init__(self, server_id: int):
        self.server_id: int = server_id
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

    def run(self) -> int:
        """Run server."""
        self.stop()
        image_name = self.get_or_create_image()
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
            mem_limit='1024M',
        )
        return self.get_container_port()

    def _get_dockerfile_directory(self) -> str:
        return str(
            Path(
                settings.BUILD_FILE_DIRECTORY.format(
                    server_id=self.server_id,
                )
            ).absolute()
        )
