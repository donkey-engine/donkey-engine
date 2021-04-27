from pathlib import Path

import docker
from django.conf import settings


class GameRunner:
    def __init__(self, server_id: int):
        self.server_id = server_id
        self.client: docker.DockerClient = docker.from_env()

        self.dockerfile_path = str(
            Path(
                settings.BUILD_FILE_DIRECTORY.format(
                    server_id=self.server_id,
                )
            ).absolute()
        )

    def get_container_port(self, attempts=100) -> int:
        for _ in range(attempts):
            for container in self.client.containers.list():
                if container.name != f'server{self.server_id}':
                    continue
                for port in container.ports.get('25565/tcp', []):
                    if not port['HostPort']:
                        continue
                    return int(port['HostPort'])
        return 0

    def get_or_create_image(self) -> str:  # TODO add reuse existed images
        image, build_log = self.client.images.build(
            tag=f'server_build_{self.server_id}',
            path=self.dockerfile_path,
            forcerm=True,
            nocache=True,
        )
        return image

    def stop(self) -> None:
        for container in self.client.containers.list():
            if container.name == f'server{self.server_id}':
                container.stop()
                break

    def run(self) -> int:
        self.stop()
        image_name = self.get_or_create_image()
        self.client.containers.run(
            image_name,
            detach=True,
            volumes=[
                f'{self.dockerfile_path}:/home/app',
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


def run_server(server_id: int) -> None:
    runner = GameRunner(server_id)
    runner.run()


def stop_server(server_id: int) -> None:
    runner = GameRunner(server_id)
    runner.stop()
