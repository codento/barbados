from rest_framework import viewsets, filters
from barbados.barbadosdb import models
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class BoatViewSet(viewsets.ModelViewSet):
    queryset = models.Boat.objects.all()
    serializer_class = serializers.BoatSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('berth', 'user')


class ClubViewSet(viewsets.ModelViewSet):
    queryset = models.Club.objects.all()
    serializer_class = serializers.ClubSerializer


class HarbourViewSet(viewsets.ModelViewSet):
    queryset = models.Harbour.objects.all()
    serializer_class = serializers.HarbourSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('club',)


class JettyViewSet(viewsets.ModelViewSet):
    queryset = models.Jetty.objects.all()
    serializer_class = serializers.JettySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('harbour',)


class BerthViewSet(viewsets.ModelViewSet):
    queryset = models.Berth.objects.all()
    serializer_class = serializers.BerthSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('jetty',)
