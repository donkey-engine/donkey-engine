from servers.helpers.configurator.base import BaseConfigurator
from servers.helpers.configurator.fields import PasswordField


class DontStarveConfigurator(BaseConfigurator):
    fields = {
        'password': PasswordField(
            name='Пароль',
            description='',
            required=False,
            default='',
            editable=True,
        )
    }
