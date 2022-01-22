import os
import tempfile
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, TransactionTestCase

from games.models import Game, GameVersion, Mod, ModVersion
from servers.helpers.adapters import get_server_directory
from servers.models import Server


class ServerTestCase(TransactionTestCase):
    def setUp(self):
        self.game = Game.objects.create(
            name='Minecraft: Java Edition',
        )
        self.version = GameVersion.objects.create(
            version='1.16',
            game=self.game,
            filepath='file/pa.th',
        )
        self.user = User.objects.create_user(
            username='username',
            email='e@mail.ru',
            password='password',
        )
        self.server = Server.objects.create(
            game=self.game,
            version=self.version,
            owner=self.user,
        )

    def test_servers_list(self):
        c = Client()

        response = c.get('/api/servers/', {}, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.',
            }
        )

        c.login(username='username', password='password')

        response = c.get('/api/servers/', {}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{
                'id': self.server.id,
                'name': 'New server',
                'port': 0,
                'status': 'CREATED',
                'game': {
                    'id': self.game.id,
                    'name': self.game.name,
                    'icon': None,
                    'description': '',
                },
                'version': {
                    'id': self.version.id,
                    'version': self.version.version,
                },
                'mods': [],
                'config': {
                    'spawn-protection': 16,
                    'gamemode': 'survival',
                    'player-idle-timeout': 0,
                    'difficulty': 'easy',
                    'spawn-monsters': True,
                    'op-permission-level': 4,
                    'pvp': True,
                    'level-type': 'default',
                    'hardcore': False,
                    'enable-command-block': False,
                    'max-players': 3,
                    'max-world-size': 15000,
                    'spawn-npcs': True,
                    'allow-flight': True,
                    'spawn-animals': True,
                    'generate-structures': True,
                    'level-seed': None,
                    'motd': 'Donkey Engine server',
                    'online-mode': False,
                },
            }]
        )

    def test_create_server(self):
        c = Client()

        response = c.post(
            '/api/servers/',
            {
                'game_id': self.game.id,
                'version_id': self.version.id,
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.',
            }
        )

        c.login(username='username', password='password')

        response = c.post(
            '/api/servers/',
            {
                'game_id': self.game.id,
                'version_id': self.version.id,
                'config': {},
            },
            content_type='application/json',
        )
        last_server = Server.objects.last()
        self.assertEqual(
            response.json(),
            {
                'id': last_server.id,  # type: ignore
                'name': 'New server',
                'game': {
                    'id': self.game.id,
                    'name': self.game.name,
                    'icon': None,
                    'description': '',
                },
                'version': {
                    'id': self.version.id,
                    'version': self.version.version,
                },
                'mods': [],
                'config': {
                    'spawn-protection': 16,
                    'gamemode': 'survival',
                    'player-idle-timeout': 0,
                    'difficulty': 'easy',
                    'spawn-monsters': True,
                    'op-permission-level': 4,
                    'pvp': True,
                    'level-type': 'default',
                    'hardcore': False,
                    'enable-command-block': False,
                    'max-players': 3,
                    'max-world-size': 15000,
                    'spawn-npcs': True,
                    'allow-flight': True,
                    'spawn-animals': True,
                    'generate-structures': True,
                    'level-seed': None,
                    'motd': 'Donkey Engine server',
                    'online-mode': False,
                },
                'port': 0,
                'status': 'CREATED',
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_create_server_with_mods(self):
        c = Client()

        response = c.post(
            '/api/servers/',
            {
                'game_id': self.game.id,
                'version_id': self.version.id,
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.',
            }
        )

        c.login(username='username', password='password')

        mod = Mod.objects.create(
            name='Test Mod',
        )
        mod_version = ModVersion.objects.create(
            name='1.0.0',
            mod=mod,
            filepath='file/pa.th.jar',
        )
        mod_version.versions.set([self.version])
        mod_version.save()
        response = c.post(
            '/api/servers/',
            {
                'name': 'custom name',
                'game_id': self.game.id,
                'version_id': self.version.id,
                'mods': [mod.id],
                'config': {},
            },
            content_type='application/json',
        )
        last_server = Server.objects.last()
        self.assertEqual(
            response.json(),
            {
                'id': last_server.id,  # type: ignore
                'name': 'custom name',
                'game': {
                    'id': self.game.id,
                    'name': self.game.name,
                    'icon': None,
                    'description': '',
                },
                'version': {
                    'id': self.version.id,
                    'version': self.version.version,
                },
                'mods': [
                    {
                        'id': mod_version.id,
                        'name': mod_version.name,
                        'mod': {
                            'id': mod.id,
                            'name': mod.name,
                            'icon': None,
                            'description': '',
                        }
                    },
                ],
                'config': {
                    'spawn-protection': 16,
                    'gamemode': 'survival',
                    'player-idle-timeout': 0,
                    'difficulty': 'easy',
                    'spawn-monsters': True,
                    'op-permission-level': 4,
                    'pvp': True,
                    'level-type': 'default',
                    'hardcore': False,
                    'enable-command-block': False,
                    'max-players': 3,
                    'max-world-size': 15000,
                    'spawn-npcs': True,
                    'allow-flight': True,
                    'spawn-animals': True,
                    'generate-structures': True,
                    'level-seed': None,
                    'motd': 'Donkey Engine server',
                    'online-mode': False,
                },
                'port': 0,
                'status': 'CREATED',
            }
        )
        self.assertEqual(response.status_code, 201)

    @patch('common.clients.ws.WsClient.new_event', lambda *args: None)
    @patch('servers.helpers.adapters.get_user_room', lambda *args: None)
    def test_deleting_server_will_delete_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_directory = tmp + '/{server_id}'
            with self.settings(BUILD_FILE_DIRECTORY=build_directory):
                directory = get_server_directory(self.server.id)
                os.mkdir(directory)

                client = Client()
                client.login(username='username', password='password')
                client.delete(f'/api/servers/{self.server.id}/')
                self.assertFalse(os.path.exists(directory))

    def test_user_cant_delete_not_owned_server(self):
        User.objects.create_user(
            username='username2',
            email='e@mail.ru',
            password='password',
        )
        client = Client()
        client.login(username='username2', password='password')

        response = client.delete(f'/api/servers/{self.server.id}/')
        self.assertEqual(response.status_code, 404)

    @patch('servers.throttling.CreateServerRateThrottle.rate', '1/min')
    def test_create_server_throttling(self):
        c = Client()
        c.login(username='username', password='password')

        response = c.post(
            '/api/servers/',
            {
                'game_id': self.game.id,
                'version_id': self.version.id,
                'config': {},
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)

        throttle_response = c.post(
            '/api/servers/',
            {
                'game_id': self.game.id,
                'version_id': self.version.id,
                'config': {},
            },
            content_type='application/json',
        )
        self.assertEqual(throttle_response.status_code, 429)
        self.assertDictEqual(
            throttle_response.json(),
            {'detail': 'Request was throttled. Expected available in 60 seconds.'}
        )

    def test_build_endpoint(self):
        c = Client()

        response = c.post(
            f'/api/servers/{self.server.id}/build/',
            {},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.',
            }
        )

    def test_stop_endpoint(self):
        c = Client()

        response = c.post(
            f'/api/servers/{self.server.id}/stop/',
            {},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.',
            }
        )

    def test_run_endpoint(self):
        c = Client()

        response = c.post(
            f'/api/servers/{self.server.id}/run/',
            {},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.',
            }
        )
