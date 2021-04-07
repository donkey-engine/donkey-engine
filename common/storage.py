import typing as t


class BaseStorage:
    """Base storage class for IO."""

    def read(self, filepath: str) -> bytes:
        """Return file contents."""
        raise NotImplementedError()

    def put(self, filepath: str, content: bytes) -> None:
        """Save file."""
        raise NotImplementedError()


class DjangoStorage(BaseStorage):
    """Storage class for filesystem."""

    def read(self, filepath: str) -> bytes:
        """Return file contents from filesystem."""
        with open(filepath, 'rb') as file:
            return file.read()

    def put(self, filepath: str, content: t.Union[str, bytes]) -> None:
        """Save file to filesystem."""
        if isinstance(content, str):
            mode = 'w'
        elif isinstance(content, bytes):
            mode = 'wb'

        with open(filepath, mode) as file:
            file.write(content)


# FIXME add s3 storage (https://github.com/donkey-engine/donkey-engine/issues/22)
storage = DjangoStorage()
