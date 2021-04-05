from settings.base import *  # noqa: F403, F401

SECRET_KEY = 'SECRET KEY'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
