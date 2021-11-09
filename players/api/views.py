from django.http.response import Http404
from rest_framework import viewsets, status, mixins, views
from rest_framework.response import Response

from .. import models
from . import serializers

import casinos.api.serializers
import casinos.models
import games.api.serializers
import games.models


def get_player_object(pk):
    try:
        return models.Player.objects.get(pk=pk)
    except:
        raise Http404


class PlayerAPIView(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Views Class to create, list and retrieve Players.
    """

    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer


class PlayerCasinoAPIView(views.APIView):
    """
    Views Class to map Player with a Casino.
    """

    def get(self, request, pk, format=None):
        casino = models.PlayerCasinoMap.objects.filter(
            player_id=pk).order_by('-id').first()

        if casino:
            serializer = casinos.api.serializers\
                                .CasinoSerializer(casino.casino)

            return Response(serializer.data,
                            status=status.HTTP_200_OK)

        return Response({"error": "Player doesn't belong to any casino."},
                        status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        player = get_player_object(pk)

        request.data['player'] = player.pk
        serializer = serializers.PlayerCasinoMapSerializer(
            data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class BettableGamesAPIView(views.APIView):
    """
    Views Class to list the bettable games in a casino.
    """

    def get(self, request, pk, format=None):
        obj = models.PlayerCasinoMap.objects.filter(
            player_id=pk).order_by('-id').first()

        if obj:
            bettable_games = games.models.Game.objects.filter(
                dealer__casino=obj.casino, ballthrow=None)

            serializer = games.api.serializers\
                                .GameSerializer(bettable_games, many=True)

            return Response(serializer.data,
                            status=status.HTTP_200_OK)

        return Response({"error": "Player doesn't belong to any casino."},
                        status=status.HTTP_400_BAD_REQUEST)
