import typing as t
from io import BytesIO, StringIO

from common.storage import storage
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
            }
        ]

    def _download_server(self) -> None:
        try:
            file_content = storage.read(self.server.version.filepath)
        except FileNotFoundError:
            raise BuilderNotFound('"server.jar" not found')
        self.files['server.jar'] = BytesIO(file_content)

    def _create_dockerfile(self) -> None:
        self.files['Dockerfile'] = StringIO('''FROM openjdk:8u212-jre-alpine
COPY ./server.jar /home/app/server.jar
COPY ./server.properties ./home/app/server.properties
WORKDIR /home/app/
CMD ["java","-Xmx1024M","-Xms1024M","-jar","server.jar","nogui"]''')
