from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import status, views
from random import randrange

import payments.models
import casinos.models

from .. import models
from . import serializers


def get_game_object(pk):
    try:
        return models.Game.objects.get(pk=pk)
    except:
        raise Http404


def get_dealer_object(pk):
    try:
        return casinos.models.Dealer.objects.get(pk=pk)
    except:
        raise Http404


class BetAPIView(views.APIView):
    """
    Views Class for placing bets on the games.
    Provides ability to create bet on a certain game.
    """

    def post(self, request, pk, format=None):
        game = get_game_object(pk)
        
        request.data['game'] = game.id
        serializer = serializers.BetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class GameStartAPIView(views.APIView):
    """
    Views Class for starting a game.
    """

    def get(self, request, pk, format=None):
        dealer = get_dealer_object(pk)

        if (models.GameTime.objects.filter(
                game__dealer=dealer).count() % 2 == 0):
            game = models.Game.objects.create(dealer=dealer)

            data = {
                'type': models.GameTime.START,
                'game': game.pk
            }

            serializer = serializers.GameTimeSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializers.GameSerializer(game).data,
                                status=status.HTTP_201_CREATED)

            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Dealer is already in a game."},
                        status=status.HTTP_400_BAD_REQUEST)


class GameEndAPIView(views.APIView):
    """
    Views Class to end a game.
    """

    def get(self, request, pk, format=None):
        dealer = get_dealer_object(pk)

        game = models.Game.objects.filter(dealer=dealer)\
                     .order_by('-id').first()

        if (models.GameTime.objects.filter(
                game__dealer=dealer).count() % 2 != 0
            and game and hasattr(game, 'ballthrow')):
            data = {
                'type': models.GameTime.END,
                'game': game.pk
            }
            serializer = serializers.GameTimeSerializer(data=data)

            if serializer.is_valid():
                successful_bets = models.Bet.objects.filter(
                    game=game, bet_number=game.ballthrow.number)

                for bet in successful_bets:
                    win_amount = bet.transaction.amount * game.WIN_RATIO

                    payments.models.Transaction.objects.create(
                        from_account=game.dealer.casino.account,
                        to_account=bet.player.account,
                        amount=win_amount)

                serializer.save()
                return Response({"successful_bets": successful_bets.count()},
                                status=status.HTTP_201_CREATED)

            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Either ball hasn't been thrown or "
                                  "the game has already ended."},
                        status=status.HTTP_400_BAD_REQUEST)


class BallThrowAPIView(views.APIView):
    """
    Views Class for throwing the ball to generate a random number
    and store it as the result.
    """

    def get(self, request, pk, format=None):
        dealer = get_dealer_object(pk)

        game = models.Game.objects.filter(dealer=dealer)\
                     .order_by('-id').first()

        if (models.GameTime.objects.filter(
                game__dealer=dealer).count() % 2 != 0
            and game and not hasattr(game, 'ballthrow')):
            data = {
                'game': game.pk,
                'number': randrange(models.Game.MIN_NUMBER,
                                    models.Game.MAX_NUMBER + 1)
            }
            serializer = serializers.BallThrowSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "No active game for the dealer or "
                                  "the game has already ended."},
                        status=status.HTTP_400_BAD_REQUEST)
