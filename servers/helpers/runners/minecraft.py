from servers.helpers.runners.base import BaseRunner, ContainerConfig


class MinecraftContainerConfig(ContainerConfig):

    ports = {
        '25565/tcp': None,
    }

    @property
    def volumes(self):
        return [
            f'{self.directory}:/home/app',
            f'{self.filepath}:/server.jar:ro',
        ]


class MinecraftRunner(BaseRunner):

    container_config_class = MinecraftContainerConfig
