from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date


def validate_year(value):
    if value is not None and (value < 0 or value > date.today().year):
        raise ValidationError(
            _('%(value)s cannot be a proper year'),
            params={'value': value},
        )
    return True


def validate_month(value):
    if value is not None and (value < 1 or value > 12):
        raise ValidationError(
            _('%(value)s not a valid month'),
            params={'value': value},
        )
    return True


def validate_day(value):
    if value is not None and (value < 1 or value > 31):
        raise ValidationError(
            _('%(value)s not a valid day'),
            params={'value': value},
        )
    return True
