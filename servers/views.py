from django.http.request import HttpRequest
from django.http.response import JsonResponse
from rest_framework import generics, views, viewsets

from servers.models import Server
from servers.serializers import CreateServerSerializer, ServerSerializer


class ServersViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows games to be viewed."""
    serializer_class = ServerSerializer

    def get_queryset(self):
        return Server.objects.filter(owner=self.request.user)


class CreateServerView(generics.CreateAPIView):
    serializer_class = CreateServerSerializer


class StartServerView(views.APIView):
    def post(self, request: HttpRequest, server_id: int):
        return JsonResponse({})


class StopServerView(views.APIView):
    def post(self, request: HttpRequest, server_id: int):
        return JsonResponse({})
