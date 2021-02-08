from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        Model = Game
        fields = ['name']
