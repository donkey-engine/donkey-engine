import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')
app = Celery('tasks', broker=os.getenv('CELERY_BROKER_HOST', 'pyamqp://guest@localhost//'))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'stopping-empty-servers': {
        'task': 'common.tasks.check_servers',
        'schedule': 5 * 60,
    },
    'writing-logs': {
        'task': 'common.tasks.reading_logs',
        'schedule': 5,
    }
}


@app.task
def check_servers():
    """Check online on servers"""
    from servers.helpers.checkers import check_minecraft_servers
    check_minecraft_servers()


@app.task
def reading_logs():
    from servers.helpers.logs import get_logs
    get_logs()


@app.task
def server_build_task(server_id: int):
    """Background server build entrypoint."""
    from servers.helpers import adapters
    return adapters.build_server(server_id)


@app.task
def server_run_task(server_id: int):
    from servers.helpers import adapters
    return adapters.run_server(server_id)


@app.task
def server_stop_task(server_id: int):
    from servers.helpers import adapters
    return adapters.stop_server(server_id)
