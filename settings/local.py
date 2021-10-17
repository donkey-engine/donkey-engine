import os

from settings.base import *  # noqa: F403, F401

SECRET_KEY = os.getenv('SECRET_KEY', 'local_secret_key')

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME', 'donkeyengine'),
        'USER': os.getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'password'),
        'HOST': os.getenv('DATABASE_HOST', '0.0.0.0'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

CELERY_BROKER_HOST = os.getenv('CELERY_BROKER_HOST', 'pyamqp://guest@localhost//')

INSTALLED_APPS += [  # type: ignore  # noqa: F405
    'corsheaders',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
]

MIDDLEWARE += [  # type: ignore  # noqa: F405
    'corsheaders.middleware.CorsMiddleware',
]

BUILD_FILE_DIRECTORY = 'local_storage/{server_id}/'
BUILD_FILE_TEMPLATE = BUILD_FILE_DIRECTORY + '{filename}'

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += [  # type: ignore  # noqa: F405
    'rest_framework.renderers.BrowsableAPIRenderer',
]

HOST_NAME = os.getenv('HOST_NAME', 'http://0.0.0.0:8000')
LOGIN_PAGE = os.getenv('LOGIN_PAGE', 'http://0.0.0.0:8000/login')

REDIS_HOST = '0.0.0.0'
REDIS_PORT = 6379
