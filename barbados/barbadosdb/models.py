from django.contrib.auth import models as auth_models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models

import uuid
import re
from datetime import date


class PhoneNumberField(models.CharField):
    """Add rules about phone numbers here
    """

    def validate(self, value, instance):
        """Check the value
        """

        super().validate(value, instance)

        if not value.startswith('+'):
            raise ValidationError(_('Use international format with phone numbers'))


class RegistrationNumberField(models.CharField):
    """Add rules about registration numbers here.
    Registration numbers are /[A-Z][0-9]{1-5}/, e.g. H54321.
    People often write them with a space or dash, e.g. H 54321 or H-54321,
    but we will require them in the canonical form.
    """

    def validate(self, value, instance):
        """Check the value
        """

        super().validate(value, instance)

        if len(value) > 0 and not re.match('[A-Z][0-9]{1,5}', value):
            raise ValidationError(_(
                'Registration number must be blank or of form A12345'))


class InspectionYearField(models.IntegerField):
    """Add rules about inspection years here.
    """

    def validate(self, value, instance):
        """Check the value
        """

        super().validate(value, instance)

        if value is not None and \
                (value < 1000 or value > date.today().year):
            raise ValidationError(_(
                'Inspection date must be 4-digit year and not in future'))


# Create your models here.


class User(auth_models.AbstractUser):
    """Corresponds to Member in the spec
    date_joined and some others inherited from AbstractUser
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    birth_date = models.DateField(null=True, blank=True, default=None)

    phone_number = PhoneNumberField(max_length=24, blank=True, default='')

    # Make this pretty free-form for compatibility with different countries
    street_address = models.TextField(null=True, blank=True, default=None)

    city = models.CharField(max_length=64, null=True, blank=True, default=None)

    country_code = models.CharField(max_length=2, null=True, blank=True, default='FI')

    class Meta:
        app_label = 'barbadosdb'


class Boat(models.Model):
    """Boats of the Users
    """
    BOAT_TYPES = (
        ('M', 'Motorboat'),
        ('S', 'Sailboat'),
    )

    MATERIALS = (
        ('F', 'Fibreglass'),
        ('W', 'Wood'),
        ('M', 'Metal'),
        ('O', 'Other'),
    )

    INSPECTION_CLASSES = (
        (1, 'Offshore'),
        (2, 'Coastal'),
        (3, 'Archipelago'),
    )

    EMPTY_CHOICE_DISPLAY_VALUE = '--------'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User)

    name = models.CharField(max_length=64, blank=True, default='', db_index=True)

    boat_type = models.CharField(
        max_length=1,
        blank=True,
        db_column='type',
        choices=[('', EMPTY_CHOICE_DISPLAY_VALUE)] + list(BOAT_TYPES),
        default='')

    model = models.CharField(max_length=64, blank=True, default='')

    manufacturer = models.CharField(max_length=64, blank=True, default='')

    registration_number = RegistrationNumberField(
        max_length=6, blank=True, default='')

    sail_number = models.IntegerField(null=True, blank=True, default=None)

    boat_certificate_number = models.IntegerField(
        null=True, blank=True, default=None)

    length = models.IntegerField(null=True, blank=True, default=None)

    beam = models.IntegerField(null=True, blank=True, default=None)

    height = models.IntegerField(null=True, blank=True, default=None)

    draught = models.IntegerField(null=True, blank=True, default=None)

    weight = models.IntegerField(null=True, blank=True, default=None)

    material = models.CharField(
        max_length=1,
        blank=True,
        choices=[('', EMPTY_CHOICE_DISPLAY_VALUE)] + list(MATERIALS),
        default='')

    colour = models.CharField(max_length=16, blank=True)

    inspection_class = models.IntegerField(
        null=True,
        blank=True,
        choices=[(None, EMPTY_CHOICE_DISPLAY_VALUE)] + list(INSPECTION_CLASSES),
        default=None
    )

    inspection_year = InspectionYearField(null=True, blank=True, default=None)

    hull_inspection_year = InspectionYearField(
        null=True, blank=True, default=None)

    insurance_company = models.CharField(max_length=64, blank=True, default='')

    class Meta:
        app_label = 'barbadosdb'

    def __str__(self):
        return self.name


class Club(models.Model):
    """Members of Harbours, with extra data
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=64, db_index=True)

    class Meta:
        app_label = 'barbadosdb'

    def __str__(self):
        return self.name


class Harbour(models.Model):
    """The topmost model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    club = models.ForeignKey(Club)

    name = models.CharField(max_length=64, db_index=True)

    class Meta:
        app_label = 'barbadosdb'

    def __str__(self):
        return self.name


class Jetty(models.Model):
    """Jetties in the Harbours
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    harbour = models.ForeignKey(Harbour)

    name = models.CharField(max_length=2, db_index=True)

    class Meta:
        app_label = 'barbadosdb'
        unique_together = ('harbour', 'name')

    def __str__(self):
        return self.name


class Berth(models.Model):
    """Berths of the Jetties
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    jetty = models.ForeignKey(Jetty)

    boat = models.OneToOneField(Boat, null=True, blank=True, default=None)

    name = models.CharField(max_length=5, db_index=True)

    class Meta:
        app_label = 'barbadosdb'
        unique_together = ('jetty', 'name')

    def __str__(self):
        return self.name
