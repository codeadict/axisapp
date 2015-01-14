from axisapp.core.models import Partner
from django.utils.translation import ugettext as _


class Provider(Partner):

    @property
    def is_provider(self):
        return True

    class Meta:
        verbose_name = _('Is Provider')
        verbose_name_plural = _('Are Providers')


class Customer(Partner):

    @property
    def is_custumer(self):
        return True

    class Meta:
        verbose_name = _('Is Provider')
        verbose_name_plural = _('Are Providers')
