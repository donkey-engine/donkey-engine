from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from common.tasks import server_build_task, server_run_task, server_stop_task
from servers.models import Server
from servers.serializers import CreateServerSerializer, ServerSerializer


class ServersViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):

    serializer_class = ServerSerializer

    def get_queryset(self):
        return Server.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        create_seriaizer = CreateServerSerializer(data=request.data, context=context)
        create_seriaizer.is_valid(raise_exception=True)
        create_seriaizer.save()
        serializer = ServerSerializer(create_seriaizer.instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
