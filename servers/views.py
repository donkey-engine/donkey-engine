from rest_framework import permissions, viewsets

from servers.models import Server
from servers.serializers import ServerSerializer


class ServersViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows games to be viewed."""
    serializer_class = ServerSerializer

    def get_queryset(self):
        return Server.objects.filter(owner=self.request.user)
