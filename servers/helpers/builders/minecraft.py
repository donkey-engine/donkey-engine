import typing as t
from io import BytesIO, StringIO

from common.storage import storage
from servers.helpers.exceptions import BuilderNotFound

from .base import BaseBuilder, BuildStage

BUILD_DIRECTORY = '/home/behindloader/Документы/{build_id}_{filename}'


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
                'name': 'Save files',
                'func': self._save_files,
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

    def _save_files(self) -> None:
        for filename, content in self.files.items():
            storage.put(
                BUILD_DIRECTORY.format(
                    build_id=self.build_id,
                    filename=filename,
                ),
                content.read(),
            )
