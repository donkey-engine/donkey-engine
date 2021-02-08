from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return self.name
