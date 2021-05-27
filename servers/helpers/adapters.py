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


def get_builder(build_key: str) -> t.Type[BaseBuilder]:
    try:
        return ALLOWED_GAMES[build_key][BUILDER]
    except KeyError as exc:
        logger.exception(exc)
        raise exceptions.BuilderNotFound() from exc


def get_runner(build_key: str) -> t.Type[BaseRunner]:
    try:
        return ALLOWED_GAMES[build_key][RUNNER]
    except KeyError as exc:
        logger.exception(exc)
        raise exceptions.RunnerNotFound() from exc


def build_server(server_id: int) -> None:
    try:
        server = Server.objects.select_related('game').get(id=server_id)
    except Server.DoesNotExist as exc:
        logger.exception(exc)
        raise exceptions.BaseError() from exc
    builder_class = get_builder(server.game.build_key)
    builder = builder_class(server)
    builder.build()


def run_server(server_id: int) -> None:
    try:
        server = Server.objects.select_related('game').get(id=server_id)
    except Server.DoesNotExist as exc:
        logger.exception(exc)
        raise exceptions.BaseError() from exc

    other_user_servers = Server.objects.filter(owner=server.owner, status='RUNNING')
    for user_server in other_user_servers:    
        runner_class = get_runner(server.game.build_key)
        runner = runner_class(user_server.id)
        runner.stop()

    runner_class = get_runner(server.game.build_key)
    runner = runner_class(server_id)
    runner.run()


def stop_server(server_id: int) -> None:
    try:
        server = Server.objects.select_related('game').get(id=server_id)
    except Server.DoesNotExist as exc:
        logger.exception(exc)
        raise exceptions.BaseError() from exc
    runner_class = get_runner(server.game.build_key)
    runner = runner_class(server_id)
    runner.stop()
