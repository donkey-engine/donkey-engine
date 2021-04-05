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

    def put(self, filepath: str, content: bytes) -> None:
        """Save file to filesystem."""
        with open(filepath, 'wb') as file:
            file.write(content)


# FIXME add s3 storage (https://github.com/donkey-engine/donkey-engine/issues/22)
storage = DjangoStorage()
