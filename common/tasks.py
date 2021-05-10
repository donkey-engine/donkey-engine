from celery import Celery
from django.conf import settings

from servers.helpers import adapters

app = Celery('tasks', broker=settings.CELERY_BROKER_HOST)


@app.task
def server_build_task(server_id: int):
    """Background server build entrypoint."""
    return adapters.build_server(server_id)


@app.task
def server_run_task(server_id: int):
    return adapters.run_server(server_id)


@app.task
def server_stop_task(server_id: int):
    return adapters.stop_server(server_id)
