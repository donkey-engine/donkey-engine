import typing as t
from io import StringIO

from django.conf import settings

from servers.helpers.builders.base import BaseBuilder, BuildStage


class DontStarveBuilder(BaseBuilder):

    def get_stages(self) -> t.List[BuildStage]:
        return [
            {
                'name': 'Create running file',
                'func': self._create_dockerfile,
            },
        ]

    def _create_dockerfile(self):
        self.files['Dockerfile'] = StringIO(f'''FROM yeetzone/dontstarvetogether
ENV NAME="{self.server.name}"
ENV TOKEN="{settings.DST_TOKEN}"
ENV LANGUAGE="ru"
ENV PAUSE_WHEN_EMPTY="true"
ENV PASSWORD="{self.server.config['password']}"''')
