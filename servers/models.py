from django.conf import settings
from django.db import models

from games.models import Game


class Server(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.owner}:{self.game}'


class ServerBuild(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, null=False)
    status = models.BooleanField(null=True)
    started = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(null=True)
