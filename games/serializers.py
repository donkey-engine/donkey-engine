from rest_framework import serializers

from games.models import Game, GameVersion, Mod, ModVersion


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Game"""
    
    class Meta:
        model = Game
        fields = ['id', 'name', 'icon', 'description']

    def to_representation(self, instance):
        response = super(GameSerializer, self).to_representation(instance)
        if instance.icon:
            response['icon'] = instance.icon.url
        return response


class GameVersionSerializer(serializers.ModelSerializer):
    """Serializer for GameVersion."""
    class Meta:
        model = GameVersion
        fields = ['id', 'version']


class ModSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mod
        fields = ['id', 'name', 'icon', 'description']

    def to_representation(self, instance):
        response = super(ModSerializer, self).to_representation(instance)
        if instance.icon:
            response['icon'] = instance.icon.url
        return response


class ModVersionsSerializer(serializers.ModelSerializer):
    """Serializer for Mods"""
    mod = ModSerializer()

    class Meta:
        model = ModVersion
        fields = ['id', 'name', 'mod']
