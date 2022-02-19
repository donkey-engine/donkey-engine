from django.contrib.auth.models import User
from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignupSerializer(serializers.Serializer):
    """Serializer for Signup"""
    email = serializers.EmailField()
    username = serializers.CharField(trim_whitespace=False)
    password = serializers.CharField()


class ConfirmEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
    username = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username')


class ResendEmailSerializer(serializers.Serializer):
    username = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username')


class DiscordRedirectSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
