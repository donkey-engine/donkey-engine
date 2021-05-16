from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from games.models import Game, Mod
from games.serializers import (GameSerializer, GameVersionSerializer,
                               ModSerializer)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows games to be viewed."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=True)
    def versions(self, request, pk):
        game = self.get_object()
        queryset = game.gameversion_set.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GameVersionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = GameVersionSerializer(queryset, many=True)
        return Response(serializer.data)


class GameModViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModSerializer

    def get_queryset(self):
        gameid = self.kwargs.get('game_id')
        return Mod.objects.filter(game_id=gameid)
