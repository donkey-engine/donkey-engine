from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return self.name


class Version(models.Model):
    version = models.CharField(max_length=64, blank=False, null=False)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.game}:{self.version}'

    class Meta:
        verbose_name_plural = 'Versions'
        verbose_name = 'Version'
        ordering = ['version']


class Mods(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='versions')
    version = models.ForeignKey('Version', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Mods'
        verbose_name = 'Mod'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}:{self.version}'
