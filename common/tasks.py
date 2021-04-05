from celery import Celery
from django.conf import settings

from servers.helpers.builder import build_server

app = Celery('tasks', broker=settings.CELERY_BROKER_HOST)


@app.task
def server_build_task(server_id: int):
    """Background server build entrypoint."""
    # TODO add retry and error catch
    return build_server(server_id)
