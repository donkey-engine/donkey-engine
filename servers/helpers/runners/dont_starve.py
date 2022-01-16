from servers.helpers.runners.base import BaseRunner, ContainerConfig


class DontStarveContainerConfig(ContainerConfig):

    @property
    def volumes(self):
        return [
            f'{self.directory}/data:/data',
            f'{self.directory}/storage:/opt/storage',
        ]


class DontStarveRunner(BaseRunner):

    container_config_class = DontStarveContainerConfig
