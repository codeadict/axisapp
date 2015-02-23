from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.db.transaction import atomic

from base.default_views import DeleteObject

from base import form_helper
from sdauth.models import User

NULL_SELECT_VALUE = '---'


class PartnerForm(form_helper.TCModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
        self.process_dt_format()

    def is_valid(self):
        return super(PartnerForm, self).is_valid()

    @atomic
    def save(self, commit=True):
        self.instance = super(PartnerForm, self).save(commit=False)
        if commit:
            self.instance.save()
        return self.instance


class CreatePartnerForm(PartnerForm):
    pass


class UpdatePartnerForm(PartnerForm):
    def __init__(self, *args, **kwargs):
        super(UpdatePartnerForm, self).__init__(*args, **kwargs)


class DeletePartner(DeleteObject):
    def delete(self, pk):
        obj = self.model.objects.get(pk=pk)
        obj.user.is_active = False
        obj.user.is_deleted = True
        obj.user.save()
