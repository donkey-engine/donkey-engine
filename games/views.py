from rest_framework import viewsets
from rest_framework import permissions
from .serializers import GameSerializer
from .models import Game


class GameViewSet(viewsets.ModelViewSet):
    """API endpoint that allows games to be viewed."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
