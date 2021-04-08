from rest_framework import serializers

from games.models import Game, Mod


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Game"""
    class Meta:
        model = Game
        fields = ['id', 'name']


class ModSerializer(serializers.ModelSerializer):
    """Serializer for Mods"""
    class Meta:
        model = Mod
        fields = ['id', 'name', 'game', 'version']
