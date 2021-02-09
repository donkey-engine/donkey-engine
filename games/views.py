from rest_framework import permissions, viewsets

from games.models import Game
from games.serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    """API endpoint that allows games to be viewed."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
