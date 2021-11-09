from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import mixins, views

from .. import models
from . import serializers


class CasinoAPIView(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ 
    Views Class for Casino Model. Provides ability to create, list and
    retrieve casinos.
    """

    queryset = models.Casino.objects.all()
    serializer_class = serializers.CasinoSerializer


class CasinoDealerAPIView(views.APIView):
    """
    Views Class for Dealers associated with Casino.
    Provides ability to create and list dealers of a certain Casino.
    """

    def get(self, request, pk, format=None):
        casino = models.Casino.objects.filter(pk=pk)

        if casino.exists():
            dealers = models.Dealer.objects.filter(casino=casino.first())
            serializer = serializers.DealerSerializer(dealers, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "Casino does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        casino = models.Casino.objects.filter(pk=pk)

        if casino.exists():
            serializer = serializers.DealerSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(casino=casino.first())
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error": "Casino does not exist."}, status=status.HTTP_400_BAD_REQUEST)
