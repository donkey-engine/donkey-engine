from django.http.request import HttpRequest
from django.http.response import JsonResponse
from rest_framework import generics, status, views, viewsets

from common.tasks import server_build_task, server_run_task, server_stop_task
from servers.models import Server
from servers.serializers import CreateServerSerializer, ServerSerializer


class ServersViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows games to be viewed."""
    serializer_class = ServerSerializer

    def get_queryset(self):
        return Server.objects.filter(owner=self.request.user)


class CreateServerView(generics.CreateAPIView):
    serializer_class = CreateServerSerializer


class BuildServerView(views.APIView):
    def post(self, request: HttpRequest, server_id: int):
        try:
            server = Server.objects.get(
                id=server_id,
                owner=self.request.user,
            )
        except Server.DoesNotExist:
            return JsonResponse({
                'error': ['Not found'],
            }, status=status.HTTP_404_NOT_FOUND)
        server_build_task.delay(server_id=server.id)
        return JsonResponse({
            'status': 'ok',
        })


class RunServerView(views.APIView):
    def post(self, request: HttpRequest, server_id: int):
        try:
            server = Server.objects.get(
                id=server_id,
                owner=self.request.user,
            )
        except Server.DoesNotExist:
            return JsonResponse({
                'error': ['Not found'],
            }, status=status.HTTP_404_NOT_FOUND)
        server_run_task.delay(server_id=server.id)
        return JsonResponse({
            'status': 'ok',
        })


class StopServerView(views.APIView):
    def post(self, request: HttpRequest, server_id: int):
        try:
            server = Server.objects.get(
                id=server_id,
                owner=self.request.user,
            )
        except Server.DoesNotExist:
            return JsonResponse({
                'error': ['Not found'],
            }, status=status.HTTP_404_NOT_FOUND)
        server_stop_task.delay(server_id=server.id)
        return JsonResponse({
            'status': 'ok',
        })
