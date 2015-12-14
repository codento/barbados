from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _
from django.db import models

from . import fields

import uuid


# Create your models here.


class User(auth_models.AbstractUser):
    """Corresponds to Member in the spec
    date_joined and some others inherited from AbstractUser
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    birth_date = models.DateField(null=True, blank=True, default=None)

    phone_number = fields.PhoneNumberField(max_length=24, blank=True, default='')

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

    registration_number = fields.RegistrationNumberField(
        max_length=6, blank=True, default='')

    sail_number = models.IntegerField(null=True, blank=True, default=None)

    boat_certificate_number = models.IntegerField(
        null=True, blank=True, default=None)

    length = models.IntegerField(help_text=_('Centimetres'), null=True, blank=True, default=None)

    beam = models.IntegerField(help_text=_('Centimetres'), null=True, blank=True, default=None)

    height = models.IntegerField(help_text=_('Centimetres'), null=True, blank=True, default=None)

    draught = models.IntegerField(help_text=_('Centimetres'), null=True, blank=True, default=None)

    weight = models.IntegerField(help_text=_('Kilograms'), null=True, blank=True, default=None)

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

    inspection_year = fields.InspectionYearField(null=True, blank=True, default=None)

    hull_inspection_year = fields.InspectionYearField(
        null=True, blank=True, default=None)

    insurance_company = models.CharField(max_length=64, blank=True, default='')

    class Meta:
        app_label = 'barbadosdb'

    def __str__(self):
        return self.name


class Membership(models.Model):
    """Membership (not the sailable) in club
    """

    user = models.ForeignKey(User)
    club = models.ForeignKey('Club')

    # This would be dependent on having paid the membership fee etc
    # It would also be default=False, I guess, but keep it easy for us
    is_valid = models.BooleanField(default=True)


class Club(models.Model):
    """Members of Harbours, with extra data
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=64, db_index=True)

    user = models.ManyToManyField(User, symmetrical=True, through=Membership)

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
        verbose_name_plural = _('Jetties')

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
        permissions = (
            ('assign_berth_boat', 'Can assign a berth to a boat'),
            ('deny_berth_boat', 'Can deny a berth from a boat'),
        )

    def __str__(self):
        return self.name

