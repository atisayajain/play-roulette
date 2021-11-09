from rest_framework import serializers
from django.db.models import Sum

from .. import models
import payments.models


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = '__all__'


class GameTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GameTime
        fields = '__all__'


class BallThrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BallThrow
        fields = '__all__'


class BetSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Bet
        fields = '__all__'
        extra_kwargs = {'transaction': {'required': False, 'read_only': True}}

    def validate(self, data):
        total_bets_amount = models.Bet.objects.filter(
            game__dealer__casino=data['game'].dealer.casino).aggregate(
                Sum('transaction__amount'))['transaction__amount__sum'] or 0

        if hasattr(data['game'], 'ballthrow'):
            raise serializers.ValidationError(
                {"error": "Can\'t place a bet after the ball has "
                          "been thrown."})

        elif data['amount'] > data['player'].account.balance:
            raise serializers.ValidationError(
                {"error": "Can\'t place a bet of more than player's"
                          " account balance."})

        elif ((total_bets_amount + data['amount']) * models.Game.WIN_RATIO 
              > data['game'].dealer.casino.account.balance):
            raise serializers.ValidationError(
                {"error": "Can\'t place a bet for more than half of "
                          "casino's account balance due to buffer balance "
                          "for all potential wins."})

        return super().validate(data)

    def create(self, validated_data):
        casino_account = validated_data['game'].dealer.casino.account
        player_account = validated_data['player'].account
        amount = validated_data.pop('amount')

        transaction = payments.models.Transaction.objects.create(
            from_account=player_account,
            to_account=casino_account,
            amount=amount)

        bet = models.Bet.objects.create(
            transaction=transaction, **validated_data)
        return bet