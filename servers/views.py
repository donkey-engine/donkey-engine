from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from common.tasks import server_build_task, server_run_task, server_stop_task
from servers.helpers.adapters import delete_server
from servers.models import Server, ServerBuild
from servers.serializers import (CreateServerSerializer, ServerSerializer,
                                 UpdateServerSerializer)
from servers.throttling import CreateServerRateThrottle


class ServersViewSet(viewsets.ModelViewSet):

    serializer_class = ServerSerializer

    def get_throttles(self):
        if self.action == 'create':
            return [CreateServerRateThrottle()]
        return []

    def get_queryset(self):
        return Server.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        delete_server(instance.id)

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

    @action(methods=['get'], detail=True)
    def logs(self, request: Request, pk: str):
        server = self.get_object()
        if server.status not in ('RUNNING', 'STOPPED'):
            return Response(
                {'detail': 'У этого сервера еще нет логов'},
                status=400,
            )
        build_instance = ServerBuild.objects.filter(
            server_id=server.id,
            kind='RUN',
        ).order_by('finished').last()
        if not build_instance:
            return Response(
                {'detail': 'У этого сервера еще нет логов'},
                status=400,
            )
        return Response({
            'build': build_instance.id,
            'logs': build_instance.logs,
        })
