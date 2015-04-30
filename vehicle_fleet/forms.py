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
    color = fields.ColorField(label=_('Color'))
    ownership = forms.CharField(label=_('Ownership'))
    fuel = forms.IntegerField(label=_('Fuel type'))

    fields_mapping = {
        'plate_number': 'plate_number__icontains',
        'chassis_number': 'chassis_number__icontains',
        'year': 'year__eql',
        'color': 'color__eql',
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


class CreateVehicleForm(EditVehicleForm):
    pass


class UpdateVehicleForm(EditVehicleForm):
    pass


class DeleteVehicleForm(DeleteObject):
    class Meta:
        model = models.Vehicles
        exclude = []


#------------------------------------
class VehicleTypeSearchForm(form_helper.GenericFilterForm):
    name = forms.CharField(label=_('Name'))

    fields_mapping = {
        'name': 'name__icontains',
    }

    model = models.VehicleType

    def __init__(self, *args, **kwargs):
        super(VehicleTypeSearchForm, self).__init__(*args, **kwargs)


class EditVehicleTypeForm(form_helper.TCModelForm):
    """
    Form for the VehicleType
    """

    class Meta:
        model = models.VehicleType
        exclude = []


class CreateVehicleTypeForm(EditVehicleTypeForm):
    """
    Form to create the VehicleType
    """
    pass


class UpdateVehicleTypeForm(EditVehicleTypeForm):
    """
    Form to update the VehicleType
    """
    pass


class DeleteVehicleTypeForm(DeleteObject):
    class Meta:
        model = models.VehicleType
        exclude = []


#---------------------------------------------------
class ModelSearchForm(form_helper.GenericFilterForm):
    name = forms.CharField(label=_('Name'))

    fields_mapping = {
        'name': 'name__icontains',
    }

    model = models.Model

    def __init__(self, *args, **kwargs):
        super(ModelSearchForm, self).__init__(*args, **kwargs)


class EditModelForm(form_helper.TCModelForm):
    """
    Form to create the Model
    """

    class Meta:
        model = models.Model
        exclude = []


class CreateModelForm(EditModelForm):
    """
    Form to create the Model
    """
    pass


class UpdateModelForm(EditModelForm):
    """
    Form to update the Model
    """
    pass


class DeleteModelForm(DeleteObject):
    class Meta:
        model = models.Model
        exclude = []


#---------------------------------------------------
class BrandsSearchForm(form_helper.GenericFilterForm):
    name = forms.CharField(label=_('Name'))

    fields_mapping = {
        'name': 'name__icontains',
    }

    model = models.Brands

    def __init__(self, *args, **kwargs):
        super(BrandsSearchForm, self).__init__(*args, **kwargs)


class EditBrandsForm(form_helper.TCModelForm):
    """
    Form to create the Brand
    """

    class Meta:
        model = models.Brands
        exclude = []


class CreateBrandsForm(EditBrandsForm):
    """
    Form to create the Brand
    """
    pass


class UpdateBrandsForm(EditBrandsForm):
    """
    Form to update the Brand
    """
    pass


class DeleteBrandsForm(DeleteObject):
    class Meta:
        model = models.Brands
        exclude = []
