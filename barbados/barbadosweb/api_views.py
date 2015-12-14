from rest_framework import viewsets
from barbados.barbadosdb import models
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class BoatViewSet(viewsets.ModelViewSet):
    queryset = models.Boat.objects.all()
    serializer_class = serializers.BoatSerializer


class ClubViewSet(viewsets.ModelViewSet):
    queryset = models.Club.objects.all()
    serializer_class = serializers.ClubSerializer


class HarbourViewSet(viewsets.ModelViewSet):
    queryset = models.Harbour.objects.all()
    serializer_class = serializers.HarbourSerializer


class JettyViewSet(viewsets.ModelViewSet):
    queryset = models.Jetty.objects.all()
    serializer_class = serializers.JettySerializer


class BerthViewSet(viewsets.ModelViewSet):
    queryset = models.Berth.objects.all()
    serializer_class = serializers.BerthSerializer
