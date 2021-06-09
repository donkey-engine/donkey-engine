from rest_framework import exceptions, viewsets

from games.models import Game, GameVersion
from games.serializers import (GameSerializer, GameVersionSerializer,
                               ModVersionsSerializer)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows games to be viewed."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameVersionsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GameVersionSerializer

    def get_queryset(self):
        gameid = self.kwargs.get('game_id')
        return GameVersion.objects.filter(game=gameid)


class GameModViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModVersionsSerializer

    def get_queryset(self):
        versionid = self.kwargs.get('version_id')
        gameid = self.kwargs.get('game_id')
        try:
            return GameVersion.objects.get(id=versionid, game=gameid).mods
        except GameVersion.DoesNotExist:
            raise exceptions.NotFound()
