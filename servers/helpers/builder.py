import logging
import typing as t

from servers.helpers import exceptions
from servers.models import Server

from .builders.base import BaseBuilder
from .builders.minecraft import MinecraftBuilder

logger = logging.getLogger(__name__)

ALLOWED_BUILDERS: t.Dict[str, t.Type[BaseBuilder]] = {
    'Minecraft: Java Edition': MinecraftBuilder,
}


def get_builder(game_name: str) -> t.Type[BaseBuilder]:
    try:
        return ALLOWED_BUILDERS[game_name]
    except KeyError as exc:
        logger.exception(exc)
        raise exceptions.BuilderNotFound() from exc


def build_server(server_id: int) -> None:
    try:
        server = Server.objects.select_related('game').get(id=server_id)
    except Server.DoesNotExist as exc:
        logger.exception(exc)
        raise exceptions.BaseError() from exc

    builder_class = get_builder(server.game.name)
    builder = builder_class(server)
    builder.build()
