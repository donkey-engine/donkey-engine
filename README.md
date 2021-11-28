# donkey-engine

[![CI](https://github.com/donkey-engine/donkey-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/donkey-engine/donkey-engine/actions/workflows/ci.yml)

## Run

- `$ virtualenv venv -p python`
- `$ source venv/bin/activate`

### Django

- Run PostgreSQL
- Migrate DB `$ python manage.py migrate --settings=settings.local`
- Create admin user `$ python manage.py createsuperuser --settings=settings.local`
- Run server `$ python manage.py runserver --settings=settings.local`

### Celery

- Run RabbitMQ
- Pass settings path to celery `$ export DJANGO_SETTINGS_MODULE=settings.local`
- Run Celery `$ celery -A common.tasks worker --loglevel=INFO`
