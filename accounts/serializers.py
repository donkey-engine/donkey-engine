from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    """Serializer for Signup"""
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
