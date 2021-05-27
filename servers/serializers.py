from rest_framework import serializers

from games.serializers import (GameSerializer, GameVersionSerializer,
                               ModSerializer)
from games.models import Mod
from servers.models import Server


class ServerSerializer(serializers.ModelSerializer):
    """Serializer for Game"""
    game = GameSerializer()
    version = GameVersionSerializer()
    mods = ModSerializer(many=True)

    class Meta:
        model = Server
        fields = ['id', 'name', 'game', 'version', 'status', 'port', 'mods']


class UpdateServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ['name']


class CreateServerSerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True, required=False)
    game_id = serializers.IntegerField(write_only=True)
    version_id = serializers.IntegerField(write_only=True)
    mods = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
    )

    def create(self, validated_data):
        server = Server.objects.create(
            owner=self.context['request'].user,
            name=validated_data.get('name', 'New server'),
            game_id=validated_data['game_id'],
            version_id=validated_data['version_id'],
        )
        server.mods.set(validated_data.get('mods',[]))
        server.save()
        return server
