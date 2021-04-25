from pathlib import Path

import docker
from django.conf import settings


def run_server(server_id: int):
    dockerfile_path = str(Path(settings.BUILD_FILE_DIRECTORY.format(
        server_id=server_id,
    )).absolute())

    client: docker.DockerClient = docker.from_env()

    client.images.build(
        tag=f'server_build_{server_id}',
        path=dockerfile_path,
        forcerm=True,
        nocache=True,
    )
