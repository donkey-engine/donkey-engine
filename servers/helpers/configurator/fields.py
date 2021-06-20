import typing as t

from servers.helpers import exceptions


class BaseField:
    """Base class for configurator fields."""
    def __init__(
        self,
        name: str,
        description: str,
        required: bool = True,
        default: t.Any = None,
        editable: bool = True,
        **kwargs,
    ):
        self.name = name
        self.description = description
        self.config = {
            'required': required,
            'default': default,
            'editable': editable,
        }
        self.field_type: str = 'base'

    def api_representation(self):
        return {
            'type': self.field_type,
            'name': self.name,
            'description': self.description,
            'config': self.config,
        }

    def validate(self, value: t.Any):
        if not self.config['editable'] and value != self.config['default']:
            raise exceptions.ConfigurationValidationError(
                f"Этот параметр нельзя редактировать"
            )
        if self.config['required'] and value is None:
            raise exceptions.ConfigurationValidationError(
                f"Этот параметр обязательный"
            )
        if value is None:
            return self.config['default']
        return value

class BooleanField(BaseField):
    def __init__(
        self,
        name: str,
        description: str,
        required: bool = True,
        default: t.Any = None,
        editable: bool = True,
        **kwargs,
    ):
        super().__init__(
            name=name,
            description=description,
            required=required,
            default=default,
            editable=editable,
            **kwargs,
        )
        self.field_type = 'boolean'

    def validate(self, value):
        value = super().validate(value)
        if not isinstance(value, bool):
            raise exceptions.ConfigurationValidationError(
                f"{value} должно быть булевым значением"
            )
        return value



class TextField(BaseField):
    """Text input field."""
    def __init__(
        self,
        name: str,
        description: str,
        required: bool = True,
        default: t.Any = None,
        editable: bool = True,
        choices: t.Optional[t.List[str]] = None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            description=description,
            required=required,
            default=default,
            editable=editable,
            **kwargs,
        )
        self.field_type = 'text'
        self.config['choices'] = choices

    def validate(self, value):
        value = super().validate(value)
        if not isinstance(value, str):
            raise exceptions.ConfigurationValidationError(
                f"{value} должно быть строкой"
            )
        if self.config['choices'] and value not in self.config['choices']:
            raise exceptions.ConfigurationValidationError(
                f"{value} должно быть из списка разрешенных значений"
            )
        return value


class NumberField(BaseField):
    """Number input field."""
    def __init__(
        self,
        name: str,
        description: str,
        required: bool = True,
        default: t.Any = None,
        editable: bool = True,
        min_value: t.Optional[int] = None,
        max_value: t.Optional[int] = None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            description=description,
            required=required,
            default=default,
            editable=editable,
            **kwargs,
        )
        self.field_type = 'number'
        self.config['min_value'] = min_value
        self.config['max_value'] = max_value

    def validate(self, value):
        value = super().validate(value)
        if not isinstance(value, [int, float]):
            raise exceptions.ConfigurationValidationError(
                f"{value} должно быть числом"
            )
        if self.config['min_value'] is not None and value < self.config['min_value']:
            raise exceptions.ConfigurationValidationError(
                f"{value} меньше чем {self.config['min_value']}"
            )
        if self.config['max_value'] is not None and value > self.config['max_value']:
            raise exceptions.ConfigurationValidationError(
                f"{value} больше чем {self.config['max_value']}"
            )
        return value
