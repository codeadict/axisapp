__author__ = 'malbalat85'
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView
from django.core.urlresolvers import reverse

from base.default_views import CustomListView, CustomDetailView, EditModelView, DeleteObject
from vehicle_fleet import models
from vehicle_fleet import forms
from vehicle_fleet.view_utils import ListFilterMixin


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
        'driver_name',
        'brand',
        'model',
        'color',
        'fuel',
        'ownership',
        'people_capacity',
    ]
    button_menu = [
        {'name': _('Add Vehicle'), 'rurl': 'vehicles-add'},
        {'name': _('Filter'), 'rurl': 'vehicles-filter'}
    ]

    def get_queryset(self):
        return super(VehicleList, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(VehicleList, self).get_context_data(**kwargs)
        context['full_width'] = True
        return context

vehicles_list = VehicleList.as_view()


class VehicleFilter(ListFilterMixin, CustomListView):
    template_name = 'vehicle_fleet/filter.jinja'
    active_page = 'vehicles-list'
    model = models.Vehicles
    perms = []
    display_items = []
    search_form = forms.VehicleSearchForm

    def get_context_data(self, **kwargs):
        context = super(VehicleFilter, self).get_context_data(**kwargs)
        context['rurl'] = 'vehicles-list'
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
        return reverse('vehicles-edit', kwargs={'pk': self.object.pk})

    def delete_url(self):
        return reverse('vehicles-delete', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(VehicleDetails, self).get_context_data(**kwargs)
        context['title'] = '%s %s (%s)' %(self.object.brand, self.object.model, self.object.plate_number)
        context['full_width'] = True
        return context

vehicles_details = VehicleDetails.as_view()


class VehicleCreate(EditModelView, CreateView):
    template_name = 'vehicle_fleet/form.jinja'
    form_class = forms.EditVehicleForm
    active_page = 'vehicles-list'
    title = _('Add Vehicle')
    perms = []

    def get_success_url(self):
        return reverse('vehicles-details', kwargs={'pk': self.object.pk})

vehicles_create = VehicleCreate.as_view()


class VehicleUpdate(EditModelView, UpdateView):
    template_name = 'vehicle_fleet/form.jinja'
    perms = []
    form_class = forms.EditVehicleForm
    model = models.Vehicles
    active_page = 'vehicles-list'
    title = _('Edit Vehicle')

    def get_success_url(self):
        return reverse('vehicles-details', kwargs={'pk': self.object.pk})

vehicles_update = VehicleUpdate.as_view()


class VehicleDelete(DeleteObject):
    model = models.Vehicles
    reverse_name = 'vehicles-list'
    perms = []

vehicles_delete = VehicleDelete.as_view()

