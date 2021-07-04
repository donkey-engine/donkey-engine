from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import Client, TestCase

from accounts.models import Profile


class AuthTestCase(TestCase):
    def test_auth(self):
        user = User.objects.create_user(
            username='username',
            email='e@mail.ru',
            password='password',
        )

        c = Client()

        response = c.post('/api/auth/', {}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'username': ['This field is required.'],
                'password': ['This field is required.'],
            },
        )

        response = c.post(
            '/api/auth/',
            {
                'username': 'username',
                'password': 'wrong_password'
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'error': ['Bad credentials']})

        response = c.post(
            '/api/auth/',
            {
                'username': 'username',
                'password': 'password'
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'id': user.id,
                'username': user.username,
            }
        )

    def test_signup(self):
        c = Client()

        response = c.post('/api/signup/', {}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': ['This field is required.'],
                'username': ['This field is required.'],
                'password': ['This field is required.'],
            }
        )

        response = c.post(
            '/api/signup/',
            {
                'username': 'username',
                'password': 'password',
                'email': 'e@mail.ru',
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

        response = c.post(
            '/api/signup/',
            {
                'username': 'new_username',
                'password': 'password',
                'email': 'e@mail.ru',
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'email': ['Already exists']})

        response = c.post(
            '/api/signup/',
            {
                'username': 'username',
                'password': 'password',
                'email': 'new_e@mail.ru',
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'username': ['Already exists']})

    def test_created_user_is_not_active(self):
        client = Client()
        client.post(
            '/api/signup/',
            {
                'username': 'test_username',
                'email': 'test@email.ua',
                'password': 'test_password'
            },
            content_type='application/json'
        )
        created_user = User.objects.get(username='test_username')
        self.assertFalse(created_user.is_active)


class DiscordAuthTestCase(TestCase):

    # TODO: test case with existsed username

    @patch(
        'accounts.views.DiscordAuthView.exchange_code',
        return_value={'access_token': 'test_access_token'}
    )
    @patch(
        'accounts.views.DiscordAuthView.get_current_user',
        return_value={
            'id': 'discord_id',
            'username': 'discord_user',
            'email': 'email@test.com'
        }
    )
    def test_signup_will_create_profile(self, exchange_code_mock, get_current_user_mock):
        client = Client()
        client.get('/api/auth/discord/redirect/?code=test_code')
        profile = Profile.objects.last()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.discord_id, 'discord_id')  # type: ignore


class EmailConfirmationTestCase(TestCase):

    def test_wrong_confirmation_token(self):
        user = User(username='test_user', is_active=False)
        user.set_password('test_password')
        user.save()

        client = Client()
        response = client.get('/api/confirm_email/', {'token': 'token', 'username': user.username})
        self.assertTrue(response.status_code, 403)

    def test_user_confirmation(self):
        user = User(username='test_user', is_active=False)
        user.set_password('test_password')
        user.save()
        token = PasswordResetTokenGenerator().make_token(user=user)

        client = Client()
        client.get('/api/confirm_email/', {'token': token, 'username': user.username})
        user.refresh_from_db()
        self.assertTrue(user.is_active)
