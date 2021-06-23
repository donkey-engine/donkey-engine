class BaseError(Exception):
    """Base exception for servers"""


class BuilderNotFound(BaseError):
    """Builder not found"""


class BaseRunnerError(BaseError):
    """Base exception for runner."""


class ConfiguratorBaseError(BaseError):
    """Base exception for configurator."""


class ConfiguratorNotFound(ConfiguratorBaseError):
    """Configurator class not found."""


class ConfigurationValidationError(ConfiguratorBaseError):
    """Validation error."""


class ServerNotRunning(BaseRunnerError):
    """Server is stopped/not running."""


class RunnerNotFound(BaseRunnerError):
    """Runner class not found."""
