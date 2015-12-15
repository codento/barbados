from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class PhoneNumberValidator(RegexValidator):
    regex = '^\+[0-9/ .()]+$'
    message = _('Use international format with phone numbers')


class RegistrationNumberValidator(RegexValidator):
    regex = '[A-Z][0-9]{1,5}'
    message = 'Registration number must be blank or of form A12345'
