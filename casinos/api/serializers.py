from rest_framework import serializers

from .. import models
import payments.api.serializers
import payments.models


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dealer
        fields = '__all__'
        extra_kwargs = {'casino': {'required': False, 'read_only': True}}


class CasinoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Casino
        fields = '__all__'
        extra_kwargs = {'account': {'required': False, 'read_only': True}}

    def create(self, validated_data):
        account = payments.models.Account.objects.create(type=0)
        casino = models.Casino.objects.create(account=account, **validated_data)

        return casino
