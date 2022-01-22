import logging
import shutil
import typing as t
from pathlib import Path

from django.conf import settings

from common.clients.ws import client as ws
from common.clients.ws import get_user_room
from servers.helpers import exceptions
from servers.helpers.builders.base import BaseBuilder
from servers.helpers.builders.dont_starve import DontStarveBuilder
from servers.helpers.builders.minecraft import MinecraftBuilder
from servers.helpers.configurator.base import BaseConfigurator
from servers.helpers.configurator.dont_starve import DontStarveConfigurator
from servers.helpers.configurator.minecraft import MinecraftConfigurator
from servers.helpers.runners.base import BaseRunner
from servers.helpers.runners.dont_starve import DontStarveRunner
from servers.helpers.runners.minecraft import MinecraftRunner
from servers.models import Server

logger = logging.getLogger(__name__)

RUNNER = 'RUNNER'
BUILDER = 'BUILDER'
CONFIGURATOR = 'CONFIGURATOR'
ALLOWED_GAMES = {
    'Minecraft: Java Edition': {
        RUNNER: MinecraftRunner,
        BUILDER: MinecraftBuilder,
        CONFIGURATOR: MinecraftConfigurator,
    },
    "Don't Starve: Together": {
        RUNNER: DontStarveRunner,
        BUILDER: DontStarveBuilder,
        CONFIGURATOR: DontStarveConfigurator,
    }
}


def get_builder(build_key: str) -> t.Type[BaseBuilder]:
    try:
        return ALLOWED_GAMES[build_key][BUILDER]
    except KeyError as exc:
        logger.exception(exc)
        raise exceptions.BuilderNotFound() from exc


def get_configurator(build_key: str) -> t.Type[BaseConfigurator]:
    try:
        return ALLOWED_GAMES[build_key][CONFIGURATOR]
    except KeyError as exc:
        logger.exception(exc)
        raise exceptions.ConfiguratorNotFound() from exc


def get_runner(build_key: str) -> t.Type[BaseRunner]:
    try:
        return ALLOWED_GAMES[build_key][RUNNER]
    except KeyError as exc:
        logger.exception(exc)
        raise exceptions.RunnerNotFound() from exc


def get_server_directory(server_id: int) -> str:
    path = Path(settings.BUILD_FILE_DIRECTORY.format(server_id=server_id))
    return str(path.absolute())


def build_server(server_id: int) -> None:
    try:
        server = Server.objects.select_related('game').get(id=server_id)
    except Server.DoesNotExist as exc:
        logger.exception(exc)
        raise exceptions.BaseError() from exc
    builder_class = get_builder(server.game.build_key)
    builder = builder_class(server)
    builder.build()

    ws.new_event(
        get_user_room(server.owner.id),
        {
            'type': 'SERVERS',
            'data': {
                'server_id': server.id,
                'status': 'BUILT',
            },
        }
    )


def run_server(server_id: int) -> None:
    try:
        server = Server.objects.select_related('game').get(id=server_id)
    except Server.DoesNotExist as exc:
        logger.exception(exc)
        raise exceptions.BaseError() from exc

    other_user_servers = Server.objects.filter(owner=server.owner, status='RUNNING')
    for user_server in other_user_servers:
        runner_class = get_runner(server.game.build_key)
        directory = get_server_directory(user_server.id)
        runner = runner_class(user_server.id, directory)
        runner.stop()

    runner_class = get_runner(server.game.build_key)
    directory = get_server_directory(server_id)
    runner = runner_class(server_id, directory)
    runner.run()

    ws.new_event(
        get_user_room(server.owner.id),
        {
            'type': 'SERVERS',
            'data': {
                'server_id': server.id,
                'status': 'RUNNING',
            },
        }
    )


def stop_server(server_id: int) -> None:
    try:
        server = Server.objects.select_related('game').get(id=server_id)
    except Server.DoesNotExist as exc:
        logger.exception(exc)
        raise exceptions.BaseError() from exc
    runner_class = get_runner(server.game.build_key)
    directory = get_server_directory(server_id)
    runner = runner_class(server_id, directory)
    runner.stop()

    ws.new_event(
        get_user_room(server.owner.id),
        {
            'type': 'SERVERS',
            'data': {
                'server_id': server.id,
                'status': 'STOPPED',
            },
        }
    )


def delete_server(server_id: int) -> None:
    Server.objects.filter(id=server_id).delete()
    directory = get_server_directory(server_id)
    shutil.rmtree(directory, ignore_errors=True)
    logger.info(f'Server №{server_id} has been deleted')
