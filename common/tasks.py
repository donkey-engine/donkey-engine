from celery import Celery
from django.conf import settings

from servers.helpers.builder import build_server
from servers.helpers.runner import run_server

app = Celery('tasks', broker=settings.CELERY_BROKER_HOST)


@app.task
def server_build_task(server_id: int):
    """Background server build entrypoint."""
    return build_server(server_id)


def server_run_task(server_id: int):
    return run_server(server_id)
