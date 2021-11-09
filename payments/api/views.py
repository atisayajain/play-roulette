from django.http.response import Http404
from rest_framework import status, views
from rest_framework.response import Response

from .. import models
from . import serializers

import casinos.models
import players.models


def get_account_object(account_model, pk):
    try:
        return account_model.objects.get(pk=pk).account
    except:
        raise Http404


class RechargeAPIView(views.APIView):
    """
    Views Class to recharge accounts both of Casino and Player.
    """

    def post(self, request, account_type, pk, format=None):
        if (models.Account.objects.get(pk=request.data['from_account']).type !=
            models.Account.PAYMENT_GATEWAY):
            return Response(
                {"error": "Can only recharge from a Payment Gateway."},
                status=status.HTTP_400_BAD_REQUEST)

        to_account = None

        if account_type == 'casino':
            to_account = get_account_object(casinos.models.Casino, pk)
        elif account_type == 'player':
            to_account = get_account_object(players.models.Player, pk)
        else:
            return Response({"error": "Invalid URL"},
                            status=status.HTTP_400_BAD_REQUEST)

        request.data['to_account'] = to_account.id

        serializer = serializers.TransactionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CashoutAPIView(views.APIView):
    """
    Views Class to cash out balance of both Casino and Player.
    """

    def post(self, request, account_type, pk, format=None):
        if (models.Account.objects.get(pk=request.data['to_account']).type != 
            models.Account.PAYMENT_GATEWAY):
            return Response(
                {"error": "Can only cash out to a Payment Gateway."},
                status=status.HTTP_400_BAD_REQUEST)

        from_account = None

        if account_type == 'casino':
            from_account = get_account_object(casinos.models.Casino, pk)
        elif account_type == 'player':
            from_account = get_account_object(players.models.Player, pk)
        else:
            return Response({"error": "Invalid URL"},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.data['amount'] > from_account.balance:
            return Response(
                {"error": "Cannot cash out more than the current account balance."},
                status=status.HTTP_400_BAD_REQUEST)

        request.data['from_account'] = from_account.id

        serializer = serializers.TransactionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BalanceAPIView(views.APIView):
    """
    Views Class to view balance of account of both Casino and Player.
    """

    def get(self, request, account_type, pk, format=None):
        
        account = None

        if account_type == 'casino':
            account = get_account_object(casinos.models.Casino, pk)
        elif account_type == 'player':
            account = get_account_object(players.models.Player, pk)
        else:
            return Response({"error": "Invalid URL"},
                            status=status.HTTP_400_BAD_REQUEST)

        if account:
            data = {'balance': account.balance}
            return Response(data, status=status.HTTP_200_OK)

        return Response({"error": "Account does not exist."},
                        status=status.HTTP_400_BAD_REQUEST)
