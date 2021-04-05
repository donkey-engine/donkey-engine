from servers.models import Server


class BaseBuilder:
    def __init__(self, server: Server):
        self.server = server

    def build(self) -> None:
        raise NotImplementedError()
