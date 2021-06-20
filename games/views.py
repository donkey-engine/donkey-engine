from rest_framework import exceptions, viewsets, views
from rest_framework.response import Response
from rest_framework.request import Request

from games.models import Game, GameVersion
from games.serializers import (GameSerializer, GameVersionSerializer,
                               ModVersionsSerializer)
from servers.helpers.adapters import get_configurator


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows games to be viewed."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameVersionsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GameVersionSerializer

    def get_queryset(self):
        gameid = self.kwargs.get('game_id')
        return GameVersion.objects.filter(game=gameid)


class GameConfiguratorView(views.APIView):
    def get(self, request: Request, game_id: int):
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {'detail': 'Not found.'},
                status=404,
            )

        configurator = get_configurator(game.build_key)

        return Response(configurator().api_representaion())


class GameModViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModVersionsSerializer

    def get_queryset(self):
        versionid = self.kwargs.get('version_id')
        gameid = self.kwargs.get('game_id')
        try:
            return GameVersion.objects.get(id=versionid, game=gameid).mods
        except GameVersion.DoesNotExist:
            raise exceptions.NotFound()
