from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Version(models.Model):
    version = models.CharField(max_length=64, blank=False, null=False)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

    filepath = models.URLField(null=False)

    def __str__(self):
        return f'{self.game}:{self.version}'

    class Meta:
        verbose_name_plural = 'Versions'
        verbose_name = 'Version'
        ordering = ('version',)
        unique_together = (('version', 'game'))


class Mods(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)

    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='versions')
    version = models.ForeignKey('Version', on_delete=models.CASCADE)

    filepath = models.URLField(null=False)

    def save(self, *args, **kwargs):
        if self.game != self.version.game:
            raise ValueError("Version game doesn't equal mod game")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Mods'
        verbose_name = 'Mod'
        ordering = ('name',)
        unique_together = (('name', 'game', 'version'))

    def __str__(self):
        return f'{self.name}:{self.game}:{self.version}'
