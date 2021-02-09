from rest_framework import serializers
from games.models import Game


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Game"""
    class Meta:
        model = Game
        fields = ['id', 'name']
