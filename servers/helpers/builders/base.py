import logging
import typing as t
from io import BytesIO, StringIO

from servers.helpers.exceptions import BaseError
from servers.models import Server, ServerBuild

logger = logging.getLogger(__name__)


class BuildStage(t.TypedDict):
    name: str
    func: t.Callable[..., None]


class BaseBuilder:
    files: t.Dict[str, t.Union[BytesIO, StringIO]] = {}

    def __init__(self, server: Server):
        self.server = server
        self.build_instance = ServerBuild.objects.create(
            server=self.server,
        )
        self.build_id: int = self.build_instance.id

    def get_stages(self) -> t.List[BuildStage]:
        return []

    def build(self) -> None:
        logs = []

        self.server.status = 'BUILDING'
        self.server.save()

        for build_stage in self.get_stages():
            try:
                build_stage['func']()
            except BaseError as exc:
                logger.exception(exc)
                logs.append(f'{build_stage["name"]} - {exc}')
                self.build_instance.status = False
                self.build_instance.logs = '\n'.join(logs)
                self.build_instance.save()
            except Exception as exc:
                logger.exception(exc)
                logs.append(f'{build_stage["name"]} - Unknown error')
                self.build_instance.status = False
                self.build_instance.logs = '\n'.join(logs)
                self.build_instance.save()
            else:
                logs.append(f'{build_stage["name"]} - OK')
        else:
            logs.append('Success')
            self.build_instance.status = True
            self.build_instance.logs = '\n'.join(logs)
            self.build_instance.save()
            self.server.status = 'BUILT'
            self.server.save()
