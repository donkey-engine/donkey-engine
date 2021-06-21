import typing as t

from servers.helpers.configurator.fields import BaseField
from servers.helpers.exceptions import ConfigurationValidationError


class BaseConfigurator:
    fields: t.Dict[str, BaseField] = {}

    def api_representaion(self):
        result = {}
        for name, field in self.fields.items():
            representation = field.api_representation()
            if not representation['config']['editable']:
                continue
            result[name] = representation
        return result

    def public_config(self, data: t.Dict[str, t.Any]):
        result = {}
        for key, field in self.fields.items():
            if not field.config['editable']:
                continue
            result[key] = data.get(key, field.config['default'])
        return result

    def validate(self, data: t.Dict[str, t.Any]):
        parsed_data = {}
        for key, field in self.fields.items():
            try:
                validated_value = field.validate(data.get(key))
            except ConfigurationValidationError as exc:
                raise ConfigurationValidationError('{}: {}'.format(key, exc))
            parsed_data[key] = validated_value
        return parsed_data
