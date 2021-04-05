class BaseError(Exception):
    """Base exception for servers"""


class BuilderNotFound(BaseError):
    """Builder not found"""
