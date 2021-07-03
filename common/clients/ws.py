"""Module for WebSocket server client."""

import typing as t
from uuid import UUID, uuid4

import requests
from django.conf import settings

from common.clients.redis import client as redis

REDIS_USER_ROOM_KEY = 'ws:{user_id}'
REDIS_USER_ROOM_EXPIRE = 60 * 60 * 24
EventType = t.Dict[str, t.Any]
HttpMethods = t.Literal['GET', 'POST', 'PUT', 'DELETE']


def get_user_room(user_id: int, extend: bool = False) -> UUID:
    """Get or create a user room for WebSocket server."""
    redis_key = REDIS_USER_ROOM_KEY.format(user_id=user_id)
    if room_id := redis.get(redis_key):
        if extend:
            redis.expire(redis_key, REDIS_USER_ROOM_EXPIRE)
        return UUID(room_id.decode('UTF-8'))
    room_id = uuid4()
    redis.set(redis_key, room_id.hex, ex=REDIS_USER_ROOM_EXPIRE)
    return room_id


class WsClient:
    """Client for WebSocket server."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self._session = requests.Session()

    def _request(
        self,
        method: HttpMethods,
        url: str,
        data: EventType,
    ) -> requests.Response:
        """Make a request."""
        response = self._session.request(
            method,
            f'http://{self.host}:{self.port}/{url}',
            json=data,
        )
        print(response.text)
        return response

    def new_event(self, to: UUID, event: EventType):
        """Send new event to WebSocket server."""
        return self._request(
            'POST',
            'events/',
            {
                'to': to.hex,
                'event': event,
            },
        )


client = WsClient(
    host=settings.SERVICE_WSBACKEND_HOST,
    port=settings.SERVICE_WSBACKEND_PORT,
)
