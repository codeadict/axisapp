from django.shortcuts import render
import copy
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from base.default_views import EditModelView
from base.display_generator import BasicPage, ItemDisplayMixin
from hhrr.models import Employee
from partners.view_utils import PartnerListView, PartnerMapView, PartnerDetailView, _GenericRoleMixin
from censo.forms import ClientSearchForm, CreateClientForm, UpdateClientForm
from partners.partner_form_helper import DeletePartner

from hhrr.forms import EmployeeSearchForm, CreateEmployeeForm, UpdateEmployeeForm


class EmployeeList(PartnerListView):
    """
    CLass to list all the Employees
    """
    template_name = 'distribution/list.jinja'
    active_page = 'employee-list'
    model = Employee
    perms = []
    detail_view = 'employee-details'
    display_items = [
        'func|identificacion',
        'email',
        'cellphone',
        'address',
    ]
    button_menu = [
        {'name': _('Add Employee'), 'rurl': 'employee-add'},
        {'name': _('Filter'), 'rurl': 'employee-filter'}
    ]
    #search_form = EmployeeSearchForm
    related_fields = ['employment_history', 'family_dependants', 'education', 'language_skill']

    def get_queryset(self):
        return super(EmployeeList, self).get_queryset()

    def identificacion(self, obj):
        return '%s (%s)' % (obj.identification, obj.id_type())
    identificacion.short_description = _('Identificacion')

employee_list = EmployeeList.as_view()


class EmployeeFilter(PartnerListView):
    template_name = 'hhrr/filter.jinja'
    active_page = 'employee-list'
    model = Employee
    perms = []
    display_items = []
    search_form = EmployeeSearchForm
    related_fields = ['user', 'country', 'category']

    def get_context_data(self, **kwargs):
        context = super(EmployeeFilter, self).get_context_data(**kwargs)
        context['rurl'] = 'employee-list'
        return context

employee_filter = EmployeeFilter.as_view()


class EmployeeDetails(PartnerDetailView):
    active_page = 'employee-list'
    model = Employee
    perms = EmployeeList.perms
    display_items = [
        'func|identification',
        'email',
        'cellphone',
        'address',
        'birthday',
        'nationality',
        'status',
        'ethnic_race',
    ]
    extra_content = 'hhrr/employee/extra_details.jinja'
    button_menu = [
        [
            {'name': _('Edit'), 'urlfunc': 'edit_url'},
            {'name': _('Delete'), 'urlfunc': 'delete_url', 'classes': 'confirm-follow', 'method': 'POST',
             'msg': _('Are you going to delete this Employee?')},
        ],
        [
            {'name': _('Change state'), 'dropdown':
                [
                    {
                       'name': display_name,
                       'urlfunc': 'set_status_url',
                       'classes': 'submit-post client-set-status',
                       'data': {'status': value}
                    } for value, display_name in Employee.STATUS_TYPE
                ]
            }
        ],
        [
            {'name': _('Label it'), 'dropdown': 'func:labels_dropdown'}
        ]
    ]

    def edit_url(self):
        return reverse('employee-edit', kwargs={'pk': self.object.pk})

    def delete_url(self):
        return reverse('employee-delete', kwargs={'pk': self.object.pk})

    def set_status_url(self):
        return reverse('employee-set-status', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetails, self).get_context_data(**kwargs)
        con_type = ContentType.objects.get_for_model(Employee)
        context['status_choices'] = dict(Employee.STATUS_TYPE)
        return context


employee_details = EmployeeDetails.as_view()


class EmployeeCreate(EditModelView, CreateView):
    template_name = 'hhrr/employee/form.jinja'
    form_class = CreateEmployeeForm
    active_page = 'employee-list'
    title = _('Add Employee')
    perms = []

    def get_success_url(self):
        return reverse('employee-details', kwargs={'pk': self.object.pk})

employee_create = EmployeeCreate.as_view()


class EmployeeUpdate(EditModelView, UpdateView):
    template_name = 'hhrr/employee/form.jinja'
    perms = []
    form_class = UpdateEmployeeForm
    model = Employee
    active_page = 'employee-list'
    title = _('Edit Employee')

    def get_success_url(self):
        return reverse('employee-details', kwargs={'pk': self.object.pk})


employee_update = EmployeeUpdate.as_view()


class EmployeeDelete(DeletePartner):
    model = Employee
    reverse_name = 'employee-list'
    perms = []

employee_delete = EmployeeDelete.as_view()


