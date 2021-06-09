from rest_framework import serializers

from games.models import Game, GameVersion, Mod, ModVersion


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
    class Meta:
        model = Mod
        fields = ['id', 'name']


class ModVersionsSerializer(serializers.ModelSerializer):
    """Serializer for Mods"""
    mod = ModSerializer()

    class Meta:
        model = ModVersion
        fields = ['id', 'name', 'mod']
