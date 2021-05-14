import json

from django.test import Client, TestCase
from django.contrib.auth.models import User

from games.models import Game, GameVersion


class GameTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create(
            name='Minecraft: Java Edition',
        )
        GameVersion.objects.create(
            version='1.16',
            game=self.game,
            filepath='file/pa.th',
        )
        User.objects.create_user(
            username='username',
            email='e@mail.ru',
            password='password',
        )

    def test_games(self):
        c = Client()

        response = c.get(
            '/api/games/',
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
            '/api/games/',
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
                'results': [{'id': self.game.id, 'name': self.game.name}]
            }
        )

    def test_specific_game(self):
        c = Client()

        response = c.get(
            f'/api/games/{self.game.id}/',
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
            f'/api/games/{self.game.id}/',
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
                'id': self.game.id,
                'name': self.game.name,
            }
        )
