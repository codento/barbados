from django.contrib.auth import models as auth_models
from django.db import models

import uuid


class PhoneNumberField(models.CharField):
    """Add rules about phone numbers here
    """

    def validate(self, value, instance):
        """Check the value
        """

        super().validate(value, instance)

        if not value.startswith('+'):
            raise ValueError('Use international format with phone numbers')


# Create your models here.


class User(auth_models.AbstractUser):
    """Corresponds to Member in the spec
    date_joined and some others inherited from AbstractUser
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    birth_date = models.DateField(null=True, blank=True, default=None)

    phone_number = PhoneNumberField(max_length=24)

    # Make this pretty free-form for compatibility with different countries
    street_address = models.TextField(null=True, blank=True, default=None)

    city = models.CharField(max_length=64, null=True, blank=True, default=None)
    country_code = models.CharField(max_length=2, null=True, blank=True, default='FI')

    class Meta:
        app_label = 'barbadosdb'


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

