from django.contrib.auth.models import User
from django.test import Client, TestCase


class AuthTestCase(TestCase):
    def test_auth(self):
        user = User.objects.create_user(
            username='username',
            email='e@mail.ru',
            password='password',
        )

        c = Client()

        response = c.post(
            '/api/auth/',
            {},
            content_type='application/json',
        )
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
        self.assertEqual(
            response.json(),
            {
                'error': ['Bad credentials'],
            }
        )

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

        response = c.post(
            '/api/signup/',
            {},
            content_type='application/json',
        )
        self.assertEqual(
            response.status_code,
            400,
        )
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
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            response.json(),
            {
                'status': 'ok',
            }
        )

        response = c.post(
            '/api/signup/',
            {
                'username': 'new_username',
                'password': 'password',
                'email': 'e@mail.ru',
            },
            content_type='application/json',
        )
        self.assertEqual(
            response.status_code,
            422,
        )
        self.assertEqual(
            response.json(),
            {
                'email': ['Already exists'],
            }
        )

        response = c.post(
            '/api/signup/',
            {
                'username': 'username',
                'password': 'password',
                'email': 'new_e@mail.ru',
            },
            content_type='application/json',
        )
        self.assertEqual(
            response.status_code,
            422,
        )
        self.assertEqual(
            response.json(),
            {
                'username': ['Already exists'],
            }
        )
