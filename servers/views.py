from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin

from common.tasks import server_build_task, server_run_task, server_stop_task
from servers.models import Server
from servers.serializers import CreateServerSerializer, ServerSerializer


class ServersViewSet(viewsets.GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin):

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateServerSerializer
        else:
            return ServerSerializer

    def get_queryset(self):
        return Server.objects.filter(owner=self.request.user)

    @action(methods=['post'], detail=True)
    def build(self, request: Request, pk: str):
        server = self.get_object()
        server_build_task.delay(server_id=server.id)
        return Response({'status': 'ok'})

    @action(methods=['post'], detail=True)
    def run(self, request: Request, pk: str):
        server = self.get_object()
        server_run_task.delay(server_id=server.id)
        return Response({'status': 'ok'})

    @action(methods=['post'], detail=True)
    def stop(self, request: Request, pk: str):
        server = self.get_object()
        server_stop_task.delay(server_id=server.id)
        return Response({'status': 'ok'})
