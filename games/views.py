from rest_framework import permissions, viewsets

from games.models import Game
from games.models import Mods
from games.serializers import GameSerializer
from games.serializers import ModsSerializer


class GameViewSet(viewsets.ModelViewSet):
    """API endpoint that allows games to be viewed."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ModsViewSet(viewsets.ModelViewSet):
    """API endpoint that allows games to be viewed."""
    queryset = Mods.objects.all()
    serializer_class = ModsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
