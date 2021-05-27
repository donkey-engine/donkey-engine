from django.contrib.auth.models import User
from django.test import Client, TestCase

from games.models import Game, GameVersion
from servers.models import Server, Mod


class GameTestCase(TestCase):
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
                },
                'version': {
                    'id': self.version.id,
                    'version': self.version.version,
                },
                'mods': [],
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
                },
                'version': {
                    'id': self.version.id,
                    'version': self.version.version,
                },
                'mods': [],
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
            mod='file/pa.th.jar',
        )
        mod.versions.set([self.version])
        mod.save()
        response = c.post(
            '/api/servers/',
            {
                'name': 'custom name',
                'game_id': self.game.id,
                'version_id': self.version.id,
                'mods': [mod.id],
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
                },
                'version': {
                    'id': self.version.id,
                    'version': self.version.version,
                },
                'mods': [{'id': mod.id, 'name': mod.name}],
                'port': 0,
                'status': 'CREATED',
            }
        )
        self.assertEqual(response.status_code, 201)


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
