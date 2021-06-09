from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    build_key = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        default='Minecraft: Java Edition',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Games'
        verbose_name = 'Game'
        ordering = ('name',)


class GameVersion(models.Model):
    version = models.CharField(max_length=64, blank=False, null=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    filepath = models.FileField(max_length=512, null=False)

    def __str__(self):
        return f'{self.game}:{self.version}'

    class Meta:
        verbose_name_plural = 'Versions'
        verbose_name = 'Version'
        ordering = ('version',)
        unique_together = (('version', 'game'))


class Mod(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Mods'
        verbose_name = 'Mod'
        ordering = ('name',)


class ModVersion(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    mod = models.ForeignKey(Mod, on_delete=models.CASCADE)
    versions = models.ManyToManyField(GameVersion, related_name='mods')
    filepath = models.FileField(max_length=512, null=False)

    def __str__(self):
        return f'{self.mod}:{self.name}'

    class Meta:
        verbose_name_plural = 'Mod versions'
        verbose_name = 'Mod version'
        ordering = ('mod', 'name',)
        unique_together = (('name', 'mod'))
