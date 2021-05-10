class BaseError(Exception):
    """Base exception for servers"""


class BuilderNotFound(BaseError):
    """Builder not found"""


class BaseRunnerError(BaseError):
    """Base exception for runner."""


class ServerNotRunning(BaseRunnerError):
    """Server is stopped/not running."""


class RunnerNotFound(BaseRunnerError):
    """Runner class not found."""
