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
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}:{self.game}'

    class Meta:
        verbose_name_plural = 'Mods'
        verbose_name = 'Mod'
        ordering = ('name',)
        unique_together = (('name', 'game'))


class ModVersion(models.Model):
    version = models.ForeignKey(GameVersion, on_delete=models.CASCADE)
    mod = models.ForeignKey(Mod, on_delete=models.CASCADE)
    filepath = models.FileField(max_length=512, null=False)

    def __str__(self):
        return f'{self.mod}:{self.version}'

    class Meta:
        verbose_name_plural = 'Mod versions'
        verbose_name = 'Mod version'
        unique_together = (('version', 'mod'))
