from rest_framework import serializers

from games.models import Game, GameVersion, Mod


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Game"""
    class Meta:
        model = Game
        fields = ['id', 'name']


class GameVersionSerializer(serializers.ModelSerializer):
    """Serializer for GameVersion."""
    class Meta:
        model = GameVersion
        fields = ['id', 'version']


class ModSerializer(serializers.ModelSerializer):
    """Serializer for Mods"""
    class Meta:
        model = Mod
        fields = ['id', 'name', 'game']
