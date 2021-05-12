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
    'http://0.0.0.0:8080'
]

MIDDLEWARE += [  # type: ignore  # noqa: F405
    'corsheaders.middleware.CorsMiddleware',
]

BUILD_FILE_DIRECTORY = 'local_storage/{server_id}/'
BUILD_FILE_TEMPLATE = BUILD_FILE_DIRECTORY + '{filename}'

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.BrowsableAPIRenderer',
]
