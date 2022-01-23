import json
import typing as t

from servers.helpers import exceptions


class BaseField:
    """Base class for configurator fields."""

    field_type = 'base'

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

    def api_representation(self):
        return {
            'type': self.field_type,
            'name': self.name,
            'description': self.description,
            'config': self.config,
        }

    def validate(self, value: t.Any):
        if (
            not self.config['editable']
            and value is not None
            and value != self.config['default']
        ):
            raise exceptions.ConfigurationValidationError(
                "Этот параметр нельзя редактировать"
            )
        if (
            self.config['required']
            and value is None
            and self.config['default'] is None
        ):
            raise exceptions.ConfigurationValidationError(
                "Этот параметр обязательный"
            )
        if value is None:
            return self.config['default']
        return value


class BooleanField(BaseField):

    field_type = 'boolean'

    def validate(self, value):
        value = super().validate(value)
        if not isinstance(value, bool):
            raise exceptions.ConfigurationValidationError(
                f"{value} должно быть булевым значением"
            )
        return value


class TextField(BaseField):
    """Text input field."""

    field_type = 'text'

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
        self.config['choices'] = choices

    def validate(self, value):
        value = super().validate(value)
        if value is not None and not isinstance(value, str):
            raise exceptions.ConfigurationValidationError(
                f"{value} должно быть строкой"
            )
        if value is not None and self.config['choices'] and value not in self.config['choices']:
            raise exceptions.ConfigurationValidationError(
                f"{value} должно быть из списка разрешенных значений"
            )
        if value is not None and len(value) > 1024:
            raise exceptions.ConfigurationValidationError(
                "Значение слишком длинное. Максимум 1024"
            )
        return value


class NumberField(BaseField):
    """Number input field."""

    field_type = 'number'

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
        self.config['min_value'] = min_value
        self.config['max_value'] = max_value

    def validate(self, value):
        value = super().validate(value)
        if value is not None:
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    raise exceptions.ConfigurationValidationError(
                        f"{value} должно быть числом"
                    )
            if not isinstance(value, (int, float)):
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


class PasswordField(BaseField):

    field_type = 'password'
