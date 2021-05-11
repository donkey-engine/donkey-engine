import logging
import typing as t

from servers.helpers import exceptions
from servers.helpers.builders.base import BaseBuilder
from servers.helpers.builders.minecraft import MinecraftBuilder
from servers.helpers.runners.base import BaseRunner
from servers.helpers.runners.minecraft import MinecraftRunner
from servers.models import Server

logger = logging.getLogger(__name__)

RUNNER = 'RUNNER'
BUILDER = 'BUILDER'
ALLOWED_GAMES = {
    'Minecraft: Java Edition': {
        RUNNER: MinecraftRunner,
        BUILDER: MinecraftBuilder,
    },
}


def get_builder(game_name: str) -> t.Type[BaseBuilder]:
    try:
        return ALLOWED_GAMES[game_name][BUILDER]
    except KeyError as exc:
        logger.exception(exc)
        raise exceptions.BuilderNotFound() from exc


def get_runner(game_name: str) -> t.Type[BaseRunner]:
    try:
        return ALLOWED_GAMES[game_name][RUNNER]
    except KeyError as exc:
        logger.exception(exc)
        raise exceptions.RunnerNotFound() from exc


def build_server(server_id: int) -> None:
    try:
        server = Server.objects.select_related('game').get(id=server_id)
    except Server.DoesNotExist as exc:
        logger.exception(exc)
        raise exceptions.BaseError() from exc
    builder_class = get_builder(server.game.name)
    builder = builder_class(server)
    builder.build()


def run_server(server_id: int) -> None:
    try:
        server = Server.objects.select_related('game').get(id=server_id)
    except Server.DoesNotExist as exc:
        logger.exception(exc)
        raise exceptions.BaseError() from exc
    runner_class = get_runner(server.game.name)
    runner = runner_class(server_id)
    runner.run()


def stop_server(server_id: int) -> None:
    try:
        server = Server.objects.select_related('game').get(id=server_id)
    except Server.DoesNotExist as exc:
        logger.exception(exc)
        raise exceptions.BaseError() from exc
    runner_class = get_runner(server.game.name)
    runner = runner_class(server_id)
    runner.stop()
