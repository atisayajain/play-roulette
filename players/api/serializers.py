from rest_framework import serializers

from .. import models
import payments.api.serializers
import payments.models


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Player
        fields = '__all__'
        extra_kwargs = {'account': {'required': False, 'read_only': True}}

    def create(self, validated_data):
        account = payments.models.Account.objects.create(
            type=payments.models.Account.PLAYER)

        player = models.Player.objects.create(
            account=account, **validated_data)

        return player


class PlayerCasinoMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PlayerCasinoMap
        fields = '__all__'