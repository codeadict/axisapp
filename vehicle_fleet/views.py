__author__ = 'malbalat85'

from django.shortcuts import render
from base.default_views import CustomListView, CustomDetailView
from view_utils import ListFilterMixin
from vehicle_fleet import forms
from vehicle_fleet import models
from django.utils.translation import ugettext_lazy as _
from base.default_views import EditModelView, DeleteObject
from django.views.generic import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType


class VehicleList(CustomListView):
    """
    CLass to list all the Vehicles
    """
    template_name = 'vehicle_fleet/list.jinja'
    active_page = 'vehicles-list'
    model = models.Vehicles
    perms = []
    detail_view = 'vehicles-details'
    display_items = [
        'plate_number',
        'chassis_number',
        'year',
        'color',
        'ownership',
    ]
    button_menu = [
        {'name': _('Add Vehicle'), 'rurl': 'vehicles-add'},
        {'name': _('Filter'), 'rurl': 'vehicles-filter'}
    ]
    #search_form = ProductSearchForm
    #related_fields = ['image', 'category', 'ice_tax', 'attributes']

    def get_queryset(self):
        return super(VehicleList, self).get_queryset()

vehicles_list = VehicleList.as_view()


class VehicleFilter(ListFilterMixin, CustomListView):
    template_name = 'vehicle_fleet/filter.jinja'
    active_page = 'vehicles-list'
    model = models.Vehicles
    perms = []
    display_items = []
    search_form = forms.VehicleSearchForm
    #related_fields = ['image', 'category', 'ice_tax', 'attributes']

    def get_context_data(self, **kwargs):
        context = super(VehicleFilter, self).get_context_data(**kwargs)
        context['rurl'] = 'vehicles-list'
        #context['search_form'] = forms.VehicleSearchForm
        return context

vehicles_filter = VehicleFilter.as_view()


class VehicleDetails(CustomDetailView):
    active_page = 'vehicle-list'
    model = models.Vehicles
    perms = VehicleList.perms
    display_items = [
        'plate_number',
        'chassis_number',
        'year',
        'color',
        'ownership',
        'driver_name',
        'transmission',
        'power',
        'vehicle_usage',
        'doors',
        'people_capacity',
    ]
    button_menu = [
        [
            {'name': _('Edit'), 'urlfunc': 'edit_url'},
            {'name': _('Delete'), 'urlfunc': 'delete_url', 'classes': 'confirm-follow', 'method': 'POST',
             'msg': _('Are you going to delete this Vehicle?')},
        ],
    ]

    def edit_url(self):
        return reverse('vehicle-edit', kwargs={'pk': self.object.pk})

    def delete_url(self):
        return reverse('vehicle-delete', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(VehicleDetails, self).get_context_data(**kwargs)
        cont_type = ContentType.objects.get_for_model(models.Vehicles)
        return context

vehicles_details = VehicleDetails.as_view()


class VehicleCreate(EditModelView, CreateView):
    template_name = 'vehicle_fleet/form.jinja'
    form_class = forms.CreateVehicleForm
    active_page = 'vehicles-list'
    title = _('Add Vehicle')
    perms = []

    def get_success_url(self):
        return reverse('vehicles-details', kwargs={'pk': self.object.pk})

vehicles_create = VehicleCreate.as_view()


class VehicleUpdate(EditModelView, UpdateView):
    template_name = 'vehicle_fleet/form.jinja'
    perms = []
    form_class = forms.UpdateVehicleForm
    model = models.Vehicles
    active_page = 'vehicles-list'
    title = _('Edit Product')

    def get_success_url(self):
        return reverse('vehicles-details', kwargs={'pk': self.object.pk})

vehicles_update = VehicleUpdate.as_view()


class VehicleDelete(DeleteObject):
    model = models.Vehicles
    reverse_name = 'vehicles-list'
    perms = []

vehicles_delete = VehicleDelete.as_view()

