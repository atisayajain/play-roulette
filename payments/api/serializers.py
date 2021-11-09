from rest_framework import serializers

from .. import models


class PaymentGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentGateway
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = '__all__'