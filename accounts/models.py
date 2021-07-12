from django.conf import settings
from django.db import models


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE)

    discord_id = models.TextField(
        null=True, unique=True)

    class Meta:
        verbose_name_plural = 'Users profile'
        verbose_name = "User's profile"

    def __str__(self):
        return str(self.user)
