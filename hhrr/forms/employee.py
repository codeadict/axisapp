__author__ = 'yo'

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm, Select
from suit.widgets import NumberInput

from base.form_helper import GenericFilterForm, TCForm
from base.models import Area
from hhrr.models import Employee
from partners.partner_form_helper import CreatePartnerForm, UpdatePartnerForm


class EmployeeSearchForm(GenericFilterForm):
    name = forms.CharField(label=_(u'Name'))
    lastname = forms.CharField(label=_(u'Last name'))
    email = forms.EmailField(label=_(u'Email'))
    graduation_date = forms.DateTimeField(label=_(u'Graduation date'))
    employment_history = forms.CharField(label=_(u'Company'))
    created_after = forms.DateTimeField(label=_(u'Created After'))
    created_before = forms.DateTimeField(label=_(u'Created Before'))

    fields_mapping = {
        'name': 'name__icontains',
        'lastname': 'lastname__icontains',
        'graduation_date': 'education__graduation_date__gte',
        'email': 'email__eql',
        'employment_history': 'employment_history__name__icontains',
        'created_after': 'user__date_created__gte',
        'created_before': 'user__date_created__lte',
    }
    model = Employee

    def __init__(self, *args, **kwargs):
        super(EmployeeSearchForm, self).__init__(*args, **kwargs)


class CreateEmployeeForm(CreatePartnerForm):
    class Meta:
        model = Employee
        exclude = ['agency', 'user']


class UpdateEmployeeForm(UpdatePartnerForm):
    class Meta:
        model = Employee

    def __init__(self, **kwargs):
        super(UpdateEmployeeForm, self).__init__(**kwargs)
