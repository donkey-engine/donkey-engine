import logging
import typing as t

import docker

from servers.helpers import exceptions
from servers.models import Server, ServerBuild

logger = logging.getLogger(__name__)


class ContainerConfig:

    volumes: t.Sequence[str] = []
    port: str

    def __init__(self, directory: str, filepath: str):
        self.directory = directory
        self.filepath = filepath


class BaseRunner:  # FIXME https://github.com/donkey-engine/donkey-engine/issues/51
    """Base class for game image/container management."""

    container_config_class = ContainerConfig

    def __init__(self, server_id: int, directory: str):
        self.server_id: int = server_id
        self.server = Server.objects.select_related('version').get(id=server_id)
        self.client: docker.DockerClient = docker.from_env()
        self.directory: str = directory
        self.container_config = self.container_config_class(
            directory=self.directory,
            filepath=self.server.version.filepath.path,
        )

    def get_container_port(self, attempts=100) -> int:
        """Get container open port."""
        for _ in range(attempts):
            for container in self.client.containers.list():
                if container.name != f'server{self.server_id}':
                    continue
                for port in container.ports.get(self.container_config.port, []):
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
        self.server.port = Server.DEFAULT_PORT
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
            logs.append('Create server image - Error')
            build_instance.success = False
            build_instance.logs = '\n'.join(logs)
            build_instance.save()
            return None
        else:
            logs.append('Create server image - OK')

        try:
            self.client.containers.run(
                image_name,
                detach=True,
                volumes=self.container_config.volumes,
                ports={self.container_config.port: None},
                name=f'server{self.server_id}',
                remove=True,
                hostname=f'server{self.server_id}',
                mem_limit='2048M',
            )
        except Exception as exc:
            logger.exception(exc)
            logs.append('Staring server - Error')
            build_instance.success = False
            build_instance.logs = '\n'.join(logs)
            build_instance.save()
            return None
        else:
            logs.append('Staring server - OK')

        try:
            port = self.get_container_port()
        except Exception as exc:
            logger.exception(exc)
            logs.append('Checking server - Error')
            build_instance.success = False
            build_instance.logs = '\n'.join(logs)
            build_instance.save()
            return None
        else:
            logs.append(f'Server port - {port}')
        build_instance.success = True
        build_instance.logs = '\n'.join(logs)
        build_instance.save()
        self.server.status = 'RUNNING'
        self.server.port = port
        self.server.save()
        return port
