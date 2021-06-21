from rest_framework import serializers, exceptions

from games.serializers import (GameSerializer, GameVersionSerializer,
                               ModVersionsSerializer)
from games.models import Game
from servers.models import Server
from servers.helpers.adapters import get_configurator
from servers.helpers.exceptions import ConfigurationValidationError


class ServerSerializer(serializers.ModelSerializer):
    """Serializer for Game"""
    game = GameSerializer()
    version = GameVersionSerializer()
    mods = ModVersionsSerializer(many=True)
    config = serializers.SerializerMethodField(method_name='get_config')

    def get_config(self, obj):
        configurator = get_configurator(obj.game.build_key)
        return configurator().public_config(obj.config)

    class Meta:
        model = Server
        fields = ['id', 'name', 'game', 'version', 'status', 'port', 'mods', 'config']


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
    config = serializers.DictField()

    def validate_game_id(self, value):
        try:
            Game.objects.get(id=value)
        except Game.DoesNotExist:
            raise exceptions.ValidationError('Game does not exist')
        return value

    def validate_config(self, value):
        game = Game.objects.get(id=self.initial_data['game_id'])
        configurator = get_configurator(game.build_key)
        try:
            validated_value = configurator().validate(value)
        except ConfigurationValidationError as exc:
            raise exceptions.ValidationError(exc)
        return validated_value

    def create(self, validated_data):
        server = Server.objects.create(
            owner=self.context['request'].user,
            name=validated_data.get('name', 'New server'),
            game_id=validated_data['game_id'],
            version_id=validated_data['version_id'],
            config=validated_data['config'],
        )
        server.mods.set(validated_data.get('mods', []))
        server.save()
        return server
