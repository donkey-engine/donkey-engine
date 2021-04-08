from rest_framework import serializers

from servers.models import Server


class ServerSerializer(serializers.ModelSerializer):
    """Serializer for Game"""
    class Meta:
        model = Server
        fields = ['game', 'version']
