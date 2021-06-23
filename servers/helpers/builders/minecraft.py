import typing as t
from datetime import datetime
from io import BytesIO, StringIO

from common.storage import storage
from servers.helpers.configurator.minecraft import MinecraftConfigurator
from servers.helpers.exceptions import BuilderNotFound

from .base import BaseBuilder, BuildStage


class MinecraftBuilder(BaseBuilder):
    def get_stages(self) -> t.List[BuildStage]:
        return [
            {
                'name': 'Create server.jar',
                'func': self._download_server,
            },
            {
                'name': 'Create running file',
                'func': self._create_dockerfile,
            },
            {
                'name': 'Accepting EULA',
                'func': self._create_eula,
            },
            {
                'name': 'Install plugins',
                'func': self._instal_plugins,
            },
            {
                'name': 'Configurating',
                'func': self._init_server_properties,
            },
        ]

    def _download_server(self) -> None:
        try:
            file_content = storage.read(self.server.version.filepath.path)
        except FileNotFoundError:
            raise BuilderNotFound('"server.jar" not found')
        self.files['server.jar'] = BytesIO(file_content)

    def _create_dockerfile(self) -> None:
        self.files['Dockerfile'] = StringIO('''FROM openjdk:8u212-jre-alpine
WORKDIR /home/app/
CMD ["java","-Xmx1024M","-Xms1024M","-jar","server.jar","nogui"]''')

    def _create_eula(self):
        self.files['eula.txt'] = StringIO('eula=TRUE')

    def _init_server_properties(self) -> None:
        configurator = MinecraftConfigurator.parse(self.server.config)

        date_now = datetime.now().strftime('%a %b %d %H:%M:%S MSK %Y')
        config_text = '#Minecraft server properties\n'
        config_text += f"#{date_now}\n"

        for key, value in configurator.validated_data.items():
            text_value = ''
            if isinstance(value, (str, int, float)):
                text_value = str(value)
            elif isinstance(value, bool):
                text_value = 'true' if value else 'false'
            config_text += f'{key}={text_value}\n'

        self.files['server.properties'] = StringIO(config_text)

    def _instal_plugins(self):
        for mod in self.server.mods.all():
            try:
                file_content = storage.read(mod.filepath.path)
            except FileNotFoundError:
                raise BuilderNotFound(f'"{mod.filepath.path}" not found')
            self.files[f'plugins/{mod.mod.name}__{mod.name}.jar'] = BytesIO(file_content)
