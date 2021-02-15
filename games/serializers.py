from rest_framework import serializers

from games.models import Game
from games.models import Mods


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Game"""
    class Meta:
        model = Game
        fields = ['id', 'name', 'version']


class ModsSerializer(serializers.ModelSerializer):
    """Serializer for Mods"""
    class Meta:
        model = Mods
        fields = ['id', 'name', 'game', 'version']
