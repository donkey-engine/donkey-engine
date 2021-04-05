from celery import Celery

from servers.helpers.builder import build_server

app = Celery('tasks', broker='pyamqp://guest@localhost//')  # FIXME add settings


@app.task
def server_build_task(server_id: int):
    """Background server build entrypoint."""
    # TODO add retry and error catch
    return build_server(server_id)
