# vim: fenc=utf-8

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.db import models

from datetime import date

import re


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

