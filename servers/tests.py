from django.contrib.auth.models import User
from django.test import Client, TestCase

from games.models import Game, GameVersion
from servers.models import Server


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

        response = c.get(
            '/api/servers/',
            {},
            content_type='application/json',
        )
        self.assertEqual(
            response.status_code,
            403,
        )
        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.',
            }
        )

        c.login(
            username='username',
            password='password',
        )

        response = c.get(
            '/api/servers/',
            {},
            content_type='application/json',
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [{
                    'id': self.server.id,
                    'port': 0,
                    'status': 'CREATED',
                    'game': {
                        'id': self.game.id,
                        'name': self.game.name,
                    },
                    'version': {
                        'id': self.version.id,
                        'version': self.version.version,
                    }
                }]
            }
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
        self.assertEqual(
            response.status_code,
            403,
        )
        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.',
            }
        )

        c.login(
            username='username',
            password='password',
        )

        response = c.post(
            '/api/servers/',
            {
                'game_id': self.game.id,
                'version_id': self.version.id,
            },
            content_type='application/json',
        )
        self.assertEqual(
            response.status_code,
            201,
        )
        last_server = Server.objects.last()
        self.assertEqual(
            response.json(),
            {
                'id': last_server.id,  # type: ignore
                'game': {
                    'id': self.game.id,
                    'name': self.game.name,
                },
                'version': {
                    'id': self.version.id,
                    'version': self.version.version,
                }
            }
        )