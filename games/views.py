from rest_framework import viewsets

from games.models import Game, GameVersion, Mod
from games.serializers import (GameSerializer, GameVersionSerializer,
                               ModSerializer)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows games to be viewed."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameModViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModSerializer

    def get_queryset(self):
        gameid = self.kwargs.get('game_id')
        return Mod.objects.filter(game_id=gameid)


class GameVersionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GameVersionSerializer

    def get_queryset(self):
        game_id = self.request.query_params.get('game_id')
        return GameVersion.objects.filter(game_id=game_id)
