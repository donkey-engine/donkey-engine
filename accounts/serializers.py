from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignupSerializer(serializers.Serializer):
    """Serializer for Signup"""
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()


class ConfirmEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
