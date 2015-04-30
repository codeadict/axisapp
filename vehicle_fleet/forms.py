__author__ = 'malbalat85'

from django.utils.translation import ugettext_lazy as _
from django import forms
from vehicle_fleet import models
from base import form_helper
from base.default_views import DeleteObject

from base import fields


class VehicleSearchForm(form_helper.GenericFilterForm):
    plate_number = forms.CharField(label=_('Plate number'))
    chassis_number = forms.CharField(label=_('Chassis number'))
    year = forms.IntegerField(label=_('Model year'))
    ownership = forms.CharField(label=_('Ownership'))
    fuel = forms.IntegerField(label=_('Fuel type'))

    fields_mapping = {
        'plate_number': 'plate_number__icontains',
        'chassis_number': 'chassis_number__icontains',
        'year': 'year__eql',
        'ownership': 'ownership__eql',
        'fuel': 'fuel__eql',
    }

    model = models.Vehicles

    def __init__(self, *args, **kwargs):
        super(VehicleSearchForm, self).__init__(*args, **kwargs)


class EditVehicleForm(form_helper.TCModelForm):
    class Meta:
        model = models.Vehicles
        exclude = []


class DeleteVehicleForm(DeleteObject):
    class Meta:
        model = models.Vehicles
        exclude = []


class EditVehicleTypeForm(form_helper.TCModelForm):
    """
    Form for the VehicleType
    """
    class Meta:
        model = models.VehicleType
        exclude = []


class DeleteVehicleTypeForm(DeleteObject):
    class Meta:
        model = models.VehicleType


class EditModelForm(form_helper.TCModelForm):
    """
    Form to create the Model
    """

    class Meta:
        model = models.Model
        fields = ['name', 'brand']


class DeleteModelForm(DeleteObject):
    class Meta:
        model = models.Model
        exclude = []


class EditBrandsForm(form_helper.TCModelForm):
    """
    Form to create the Brand
    """

    class Meta:
        model = models.Brands
        fields = ['name']

class DeleteBrandsForm(DeleteObject):
    class Meta:
        model = models.Brands
        exclude = []
