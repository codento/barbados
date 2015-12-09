from django.db import models

import uuid

# Create your models here.


class Club(models.Model):
    """Members of Harbours, with extra data
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=64, db_index=True)

    class Meta:
        app_label = 'barbadosdb'


class Harbour(models.Model):
    """The topmost model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    club = models.ForeignKey(Club)

    name = models.CharField(max_length=64, db_index=True)

    class Meta:
        app_label = 'barbadosdb'


class Jetty(models.Model):
    """Jetties in the Harbours
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    harbour = models.ForeignKey(Harbour)

    name = models.CharField(max_length=2, db_index=True)

    class Meta:
        app_label = 'barbadosdb'
        unique_together = ('harbour', 'name')


class Berth(models.Model):
    """Berths of the Jetties
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    jetty = models.ForeignKey(Jetty)

    name = models.CharField(max_length=5, db_index=True)

    class Meta:
        app_label = 'barbadosdb'
        unique_together = ('jetty', 'name')

