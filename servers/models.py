from django.conf import settings
from django.db import models

from games.models import Game, GameVersion, ModVersion

SERVER_STATUSES = (
    ('CREATED', 'Just created'),
    ('BUILT', 'Server ready to start'),
    ('RUNNING', 'Running'),
    ('STOPPED', 'Stopped'),
)

SERVER_BUILD_KINDS = (
    ('BUILD', 'Build'),
    ('RUN', 'Run'),
)


class Server(models.Model):
    DEFAULT_PORT = 0

    name = models.CharField(max_length=64, null=False, blank=False, default='New server')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    version = models.ForeignKey(GameVersion, on_delete=models.CASCADE, null=False)
    mods = models.ManyToManyField(ModVersion, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=SERVER_STATUSES, default='CREATED')
    port = models.IntegerField(null=False, default=DEFAULT_PORT)
    config = models.JSONField(default=dict)  # type: ignore

    def save(self, *args, **kwargs):
        if self.game != self.version.game:
            raise ValueError("Version game doesn't equal mod game")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.owner}:{self.game}'


class ServerBuild(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, null=False)
    kind = models.CharField(max_length=32, choices=SERVER_BUILD_KINDS, null=True)
    success = models.BooleanField(null=True)
    started = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(auto_now=True, blank=True)
    logs = models.TextField()
