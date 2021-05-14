from rest_framework import serializers

from games.serializers import GameSerializer, GameVersionSerializer
from servers.models import Server


class ServerSerializer(serializers.ModelSerializer):
    """Serializer for Game"""
    game = GameSerializer()
    version = GameVersionSerializer()

    class Meta:
        model = Server
        fields = ['id', 'game', 'version', 'status', 'port']


class CreateServerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    game = GameSerializer(read_only=True)
    version = GameVersionSerializer(read_only=True)

    game_id = serializers.IntegerField(write_only=True)
    version_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        return Server.objects.create(
            game_id=validated_data.get('game_id'),
            version_id=validated_data.get('version_id'),
            owner=self.context['request'].user,
        )
