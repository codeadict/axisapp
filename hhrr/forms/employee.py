__author__ = 'yo'

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm, Select
from suit.widgets import NumberInput

from base.form_helper import GenericFilterForm, TCForm
from base.models import Area
from hhrr.models import Employee, EmploymentHistory, FamilyRelation, FamilyDependant, \
    Language, EducationArea, Education, EnterpriseDepartment
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
        #exclude = ['agency', 'user']


class UpdateEmployeeForm(UpdatePartnerForm):
    class Meta:
        model = Employee

    def __init__(self, **kwargs):
        super(UpdateEmployeeForm, self).__init__(**kwargs)


class CreateEmploymentHistoryForm(CreatePartnerForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = EmploymentHistory
        exclude = []


class UpdateEmploymentHistoryForm(UpdatePartnerForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = EmploymentHistory

    def __init__(self, **kwargs):
        super(UpdateEmploymentHistoryForm, self).__init__(**kwargs)


class CreateLanguageForm(CreatePartnerForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = Language
        exclude = []


class UpdateLanguageForm(UpdatePartnerForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = Language

    def __init__(self, **kwargs):
        super(UpdateLanguageForm, self).__init__(**kwargs)


class CreateFamilyRelationForm(CreatePartnerForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = FamilyRelation
        exclude = []


class UpdateFamilyRelationForm(UpdatePartnerForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = Language

    def __init__(self, **kwargs):
        super(UpdateFamilyRelationForm, self).__init__(**kwargs)


class CreateFamilyDependantForm(CreatePartnerForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = FamilyDependant
        exclude = []


class UpdateFamilyDependantForm(UpdatePartnerForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = FamilyDependant

    def __init__(self, **kwargs):
        super(UpdateFamilyDependantForm, self).__init__(**kwargs)


class CreateEducationAreaForm(CreatePartnerForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = EducationArea
        exclude = []


class UpdateEducationAreaForm(UpdatePartnerForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = EducationArea

    def __init__(self, **kwargs):
        super(UpdateEducationAreaForm, self).__init__(**kwargs)


class CreateEducationForm(CreatePartnerForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = Education
        exclude = []


class UpdateEducationForm(UpdatePartnerForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = Education

    def __init__(self, **kwargs):
        super(UpdateEducationForm, self).__init__(**kwargs)


class CreateEnterpriseDepartmentForm(CreatePartnerForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = EnterpriseDepartment
        exclude = []


class UpdateEnterpriseDepartmentForm(UpdatePartnerForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = EnterpriseDepartment

    def __init__(self, **kwargs):
        super(UpdateEnterpriseDepartmentForm, self).__init__(**kwargs)