from rest_framework import serializers
from django.conf import settings


class SignupSerializer(serializers.ModelSerializer):
    """Serializer for Signup"""
    class Meta():
        model = settings.AUTH_USER_MODEL
        fields = ['username', 'password', 'email']
