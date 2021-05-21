from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.request import Request
from rest_framework.response import Response

from common.tasks import server_build_task, server_run_task, server_stop_task
from servers.models import Server
from servers.serializers import (CreateServerSerializer, ServerSerializer,
                                 UpdateServerSerializer)


class ServersViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):

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

    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed('PUT')

    def partial_update(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        update_seriaizer = UpdateServerSerializer(data=request.data, context=context)
        update_seriaizer.is_valid(raise_exception=True)
        instance = self.get_object()
        update_seriaizer.update(instance, update_seriaizer.validated_data)
        serializer = ServerSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
