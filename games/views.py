from rest_framework import permissions, viewsets

from games.models import Game, Mods
from games.serializers import GameSerializer, ModsSerializer


class GameViewSet(viewsets.ModelViewSet):
    """API endpoint that allows games to be viewed."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]


class GameModsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModsSerializer

    def get_queryset(self):
        gameid = self.kwargs['gameid']
        return Mods.objects.filter(game_id=gameid)
    permission_classes = [permissions.IsAuthenticated]
