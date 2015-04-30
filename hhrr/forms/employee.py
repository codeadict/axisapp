__author__ = 'yo'

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.gis.forms import PointField

from base import gis as gisform
from base import form_helper
from hhrr.models import Employee, EmploymentHistory, FamilyRelation, FamilyDependant, \
    Language, EducationArea, Education, EnterpriseDepartment
from partners.partner_form_helper import UpdatePartnerForm, CreatePartnerForm, DeletePartner


class EmployeeSearchForm(form_helper.GenericFilterForm):
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
    coordinates = PointField(widget=gisform.BaseGMapWidget)

    class Meta:
        model = Employee
        exclude = ['status']


class UpdateEmployeeForm(UpdatePartnerForm):
    coordinates = PointField(widget=gisform.BaseGMapWidget)

    class Meta:
        model = Employee
        exclude = ['status']

    def __init__(self, **kwargs):
        super(UpdateEmployeeForm, self).__init__(**kwargs)


class DeleteEmployeeForm(DeletePartner):
    class Meta:
        model = Employee
        exclude = []


class CreateEmploymentHistoryForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = EmploymentHistory
        exclude = []


class UpdateEmploymentHistoryForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = EmploymentHistory

    def __init__(self, **kwargs):
        super(UpdateEmploymentHistoryForm, self).__init__(**kwargs)


class CreateLanguageForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = Language
        exclude = []


class UpdateLanguageForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = Language

    def __init__(self, **kwargs):
        super(UpdateLanguageForm, self).__init__(**kwargs)


class CreateFamilyRelationForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = FamilyRelation
        exclude = []


class UpdateFamilyRelationForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = Language

    def __init__(self, **kwargs):
        super(UpdateFamilyRelationForm, self).__init__(**kwargs)


class CreateFamilyDependantForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = FamilyDependant
        exclude = []


class UpdateFamilyDependantForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = FamilyDependant

    def __init__(self, **kwargs):
        super(UpdateFamilyDependantForm, self).__init__(**kwargs)


class CreateEducationAreaForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = EducationArea
        exclude = []


class UpdateEducationAreaForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = EducationArea

    def __init__(self, **kwargs):
        super(UpdateEducationAreaForm, self).__init__(**kwargs)


class CreateEducationForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = Education
        exclude = []


class UpdateEducationForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = Education

    def __init__(self, **kwargs):
        super(UpdateEducationForm, self).__init__(**kwargs)


class CreateEnterpriseDepartmentForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = EnterpriseDepartment
        exclude = []


class UpdateEnterpriseDepartmentForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = EnterpriseDepartment

    def __init__(self, **kwargs):
        super(UpdateEnterpriseDepartmentForm, self).__init__(**kwargs)