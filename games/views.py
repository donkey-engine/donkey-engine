from rest_framework import viewsets

from games.models import Game, Mod
from games.serializers import GameSerializer, ModSerializer


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows games to be viewed."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameModViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModSerializer

    def get_queryset(self):
        gameid = self.kwargs['gameid']
        return Mod.objects.filter(game_id=gameid)
