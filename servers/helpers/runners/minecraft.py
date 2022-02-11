from servers.helpers.runners.base import BaseRunner, ContainerConfig


class MinecraftContainerConfig(ContainerConfig):

    port = '25565/tcp'

    @property
    def volumes(self):
        return [
            f'{self.directory}:/home/app',
            f'{self.filepath}:/server.jar:ro',
        ]


class MinecraftRunner(BaseRunner):

    container_config_class = MinecraftContainerConfig
