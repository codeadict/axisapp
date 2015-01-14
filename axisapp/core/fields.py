__author__ = 'codeadict'

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CharField as BaseCharField, DecimalField
from django.forms.fields import CharField, MultipleChoiceField
from django.utils.translation import ugettext_lazy as _



class PercentageField(DecimalField):
    """
    Database field for storing percentage values.
    Validates that value is a Decimal in the range 0 - 100.
    """
    description = _("Percentage (between %(min_value)s and %(max_value)s)")

    MIN_VALUE = 0
    MAX_VALUE = 100
    ERROR_MSG = _(u'The value must be between 0 and 100.')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 6)
        kwargs.setdefault('decimal_places', 3)
        super(PercentageField, self).__init__(*args, **kwargs)

    default_error_messages = {
        'invalid': ERROR_MSG,
        'min_value': ERROR_MSG,
        'max_value': ERROR_MSG,
    }

    default_validators = [
        MinValueValidator(MIN_VALUE),
        MaxValueValidator(MAX_VALUE),
    ]

    def formfield(self, **kwargs):
        defaults = {'min_value': self.MIN_VALUE, 'max_value': self.MAX_VALUE}
        defaults.update(kwargs)
        return super(PercentageField, self).formfield(**defaults)


class MoneyField(DecimalField):
    """
    Custom database field for storing money.
    """
    description = _(u'Monetary Amount')

    default_error_messages = {
        'invalid': _(u'The value is not a valid monetary amount.'),
        'min_value': _(u'Please enter only positive amounts.'),
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 20)
        kwargs.setdefault('decimal_places', 2)
        super(MoneyField, self).__init__(*args, **kwargs)


class PositiveMoneyField(MoneyField):
    """
    Custom database field for storing money.
    It makes sure that value is not negative.
    """
    default_validators = [
        MinValueValidator(0),
    ]

    def formfield(self, **kwargs):
        return super(PositiveMoneyField, self).formfield(min_value=0)
