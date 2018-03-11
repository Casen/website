from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .serializers import GameSerializer, MoveSerializer

from .models import Game, Move
from .lib.ai import GameState, AlphaBeta

# Create your views here.

class GameViewSet(viewsets.ModelViewSet):
    """
    API for interacting with games
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @detail_route(methods=['post'])
    def ai_move(self, request, pk):
        game = self.get_object()

        gs = GameState(game.to_state())
        ab = AlphaBeta()

        next_game_state = ab.search(gs)

        ai_played_move = next_game_state.moves.pop()
        ai_played_move.game = game
        ai_played_move.save()
        # TODO figure out DRF nonsense. 
        return Response(serializer.data)


class MoveViewSet(viewsets.ModelViewSet):
    """
    API for interacting with game moves
    """
    serializer_class = MoveSerializer

    def get_queryset(self):
        return Move.objects.filter(game=self.kwargs['game_pk'])

