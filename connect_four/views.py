from django.shortcuts import render
from rest_framework import viewsets

from .serializers import GameSerializer, MoveSerializer

from .models import Game, Move

# Create your views here.

class GameViewSet(viewsets.ModelViewSet):
    """
    API for interacting with games
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class MoveViewSet(viewsets.ModelViewSet):
    """
    API for interacting with game moves
    """
    serializer_class = MoveSerializer

    def get_queryset(self):
        return Move.objects.filter(game=self.kwargs['game_pk'])
