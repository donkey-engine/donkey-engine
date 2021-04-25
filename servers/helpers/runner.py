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

    def get_or_create_image(self) -> str:  # TODO add reuse existed images
        image, build_log = self.client.images.build(
            tag=f'server_build_{self.server_id}',
            path=self.dockerfile_path,
            forcerm=True,
            nocache=True,
        )
        return image

    def run(self) -> None:
        image_name = self.get_or_create_image()
        self.client.containers.run(
            image_name,
            detach=True,
            volumes=[
                f'{self.dockerfile_path}:/home/app',
            ],
            ports={
                '25565/tcp': 25565,
            },
            name=f'server{self.server_id}',
        )


def run_server(server_id: int) -> None:
    runner = GameRunner(server_id)
    runner.run()
