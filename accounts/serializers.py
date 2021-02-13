from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    """Serializer for Signup"""
    email = serializers.EmailField()
    username = serializers.CharField(max_length=200)
    password = serializers.DateTimeField()
