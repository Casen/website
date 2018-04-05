import datetime
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .serializers import GameSerializer, MoveSerializer

from .models import Game, Move
from .lib.ai import GameSession

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

        gs = GameSession(game)

        next_game_state = gs.make_move()

        if next_game_state.winning_player:
            game.ended_at = datetime.datetime.now()
            game.winner = next_game_state.winning_player
            game.save()
        else:
            ai_played_move = next_game_state.move_made
            ai_played_move.game = game
            ai_played_move.save()

        #Reload the game
        game = self.get_object()
        serializer = self.get_serializer(game)
        return Response(serializer.data)


class MoveViewSet(viewsets.ModelViewSet):
    """
    API for interacting with game moves
    """
    serializer_class = MoveSerializer

    def get_queryset(self):
        return Move.objects.filter(game=self.kwargs['game_pk'])


def play_game(request):
    """Landing page for interactive game"""
    return render(request, 'build/index.html', {})
