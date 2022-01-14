import logging
import typing as t
from io import BytesIO, StringIO

from django.conf import settings

from common.storage import storage
from servers.helpers.exceptions import BaseError
from servers.models import Server, ServerBuild

logger = logging.getLogger(__name__)


class BuildStage(t.TypedDict):
    name: str
    func: t.Callable[[], None]


class BaseBuilder:
    def __init__(self, server: Server):
        self.files: t.Dict[str, t.Union[BytesIO, StringIO]] = {}

        self.server = server
        self.build_instance = ServerBuild.objects.create(
            server=self.server,
            kind='BUILD',
        )

    def get_stages(self) -> t.List[BuildStage]:
        return []

    def build(self) -> None:
        logs = []

        for build_stage in self.get_stages():
            try:
                build_stage['func']()
            except BaseError as exc:
                logger.exception(exc)
                logs.append(f'{build_stage["name"]} - {exc}')
                self.build_instance.success = False
                self.build_instance.logs = '\n'.join(logs)
                self.build_instance.save()
                break
            except Exception as exc:
                logger.exception(exc)
                logs.append(f'{build_stage["name"]} - Unknown error')
                self.build_instance.success = False
                self.build_instance.logs = '\n'.join(logs)
                self.build_instance.save()
                break
            else:
                logs.append(f'{build_stage["name"]} - OK')
        else:
            logs.append('Success')
            self.build_instance.success = True
            self.build_instance.logs = '\n'.join(logs)
            self.build_instance.save()
            self.server.status = 'BUILT'
            self.server.save()
            self._save_files()

    def _save_files(self) -> None:
        for filename, content in self.files.items():
            storage.put(
                settings.BUILD_FILE_TEMPLATE.format(
                    server_id=self.server.id,
                    filename=filename,
                ),
                content.read(),
            )
