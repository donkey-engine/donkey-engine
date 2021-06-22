import typing as t

from servers.helpers.configurator.fields import BaseField
from servers.helpers.exceptions import ConfigurationValidationError


DictFields = t.Dict[str, t.Any]


class BaseConfigurator:
    fields: t.Dict[str, BaseField] = {}

    validated_data: DictFields = {}

    @classmethod
    def get_fields_representation(cls) -> DictFields:
        """Return fields config without values."""
        result = {}
        for name, field in cls.fields.items():
            representation = field.api_representation()
            if not representation['config']['editable']:
                continue
            result[name] = representation
        return result

    @classmethod
    def parse(cls, data: DictFields):
        """Parse API data."""
        instance = cls()
        instance.validated_data = {}
        for key, field in cls.fields.items():
            try:
                validated_value = field.validate(data.get(key))
            except ConfigurationValidationError as exc:
                raise ConfigurationValidationError('{}: {}'.format(key, exc))
            instance.validated_data[key] = validated_value
        return instance

    def exclude(self, key: str, equal=True):
        """Mutate `.validated_data` and exclude true values of `key`."""
        for field_key, field in self.fields.items():
            if field.config[key] == equal:
                del self.validated_data[field_key]
