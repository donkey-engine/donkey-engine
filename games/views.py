from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import GameSerializer
from .models import Game

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
