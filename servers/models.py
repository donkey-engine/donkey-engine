from django.db import models
from django.conf import settings

from games.models import Game


class Server(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT, null=False, blank=False)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)