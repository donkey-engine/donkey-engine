import typing as t

from servers.helpers.configurator.fields import BaseField


class BaseConfigurator:
    fields: t.Dict[str, t.Type[BaseField]] = {}

    def api_representaion(self):
        result = {}
        for name, field in self.fields.items():
            representation = field.api_representation()
            if not representation['config']['editable']:
                continue
            result[name] = representation
        return result
