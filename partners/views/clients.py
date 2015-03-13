import copy
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from base.default_views import EditModelView
from base.display_generator import BasicPage, ItemDisplayMixin
from censo.models import Cliente
from partners.view_utils import PartnerListView, PartnerMapView, PartnerDetailView, _GenericRoleMixin
from censo.forms import ClientSearchForm, CreateClientForm, UpdateClientForm, ClientsMapFilterForm
from partners.partner_form_helper import DeletePartner


class ClientList(PartnerListView):
    active_page = 'client-list'
    model = Cliente
    perms = []
    detail_view = 'client-details'
    display_items = [
        'func|identificacion',
        'email',
        'celular',
        'direccion',
        'convencional',
        'func|location',
    ]
    button_menu = [
        {'name': _('Agregar Cliente'), 'rurl': 'client-add'},
        {'name': _('Filtrar'), 'rurl': 'client-filter'}
    ]
    search_form = ClientSearchForm

    def get_queryset(self):
        return super(ClientList, self).get_queryset()


client_list = ClientList.as_view()


class ClientMap(PartnerMapView):
    active_page = 'client-map'
    geometry_field = 'coordenadas'
    paginate_by = None  # we get all the results no pagination
    model = Cliente
    perms = []
    detail_view = 'client-details'
    display_items = [
        'func|identificacion',
        'email',
        'celular',
        'direccion',
        'convencional',
        'func|location',
    ]
    button_menu = [
        {'name': _('Agregar Cliente'), 'rurl': 'client-add'},
        {'name': _('FullScreen Map'), 'urlfunc': 'fullscreen_url', 'classes': 'map-go-fullscreen'},
    ]
    search_form = ClientSearchForm

    def fullscreen_url(self):
        return 'javascript:void(0);'

    def get_queryset(self):
        qs = super(ClientMap, self).get_queryset().only('coordenadas', 'nombres', 'apellidos').order_by().cache()
        search_form = self.get_search_form()
        search_form.full_clean()
        search_form_data = search_form.clean()
        return qs

    def get_search_form(self):
        return ClientsMapFilterForm(data=self.request.GET, request=self.request)

    def get_context_data(self, **kwargs):
        context = super(ClientMap, self).get_context_data(**kwargs)
        context['search_form'] = self.get_search_form()
        context['full_width'] = True
        return context


client_map = ClientMap.as_view()


class ClientFilter(PartnerListView):
    template_name = 'partners/filter.jinja'
    active_page = 'client-list'
    model = Cliente
    perms = []
    display_items = []
    search_form = ClientSearchForm
    related_fields = ['user', 'country', 'category']

    def get_context_data(self, **kwargs):
        context = super(ClientFilter, self).get_context_data(**kwargs)
        context['rurl'] = 'client-list'
        return context


client_filter = ClientFilter.as_view()


class ClientDetails(PartnerDetailView):
    active_page = 'client-list'
    model = Cliente
    perms = ClientList.perms
    display_items = [
        'func|identificacion',
        'email',
        'celular',
        'direccion',
        'convencional',
        'func|location',
        'cumple',
        'especial',
        'razon_social',
        'estatal',
        'nombre_comercial',
        'website',
    ]
    extra_content = 'partners/client/extra_details.jinja'
    button_menu = [
        [
            {'name': _('Editar'), 'urlfunc': 'edit_url'},
            {'name': _('Eliminar'), 'urlfunc': 'delete_url', 'classes': 'confirm-follow', 'method': 'POST',
             'msg': _('Seguro que desea eliminar este Cliente?')},
        ],
        [
            {'name': _('Verificar en SRi'), 'urlfunc': 'edit_url'},
            {'name': _('Ver en el mapa'), 'urlfunc': 'map_url'},
        ],
        [
            {'name': _('Cambiar Estado'), 'dropdown':
                [
                    {
                       'name': display_name,
                       'urlfunc': 'set_status_url',
                       'classes': 'submit-post client-set-status',
                       'data': {'status': value}
                    } for value, display_name in Cliente.ESTADOS
                ]
            }
        ],
        [
            {'name': _('Etiquetar'), 'dropdown': 'func:labels_dropdown'}
        ]
    ]

    def edit_url(self):
        return reverse('client-edit', kwargs={'pk': self.object.pk})

    def delete_url(self):
        return reverse('client-delete', kwargs={'pk': self.object.pk})

    def set_status_url(self):
        return reverse('client-set-status', kwargs={'pk': self.object.pk})

    def map_url(self):
        url = reverse('client-map')
        return url + '#19/%s/%s' % (self.object.coordenadas.y, self.object.coordenadas.x)

    def get_context_data(self, **kwargs):
        context = super(ClientDetails, self).get_context_data(**kwargs)
        con_type = ContentType.objects.get_for_model(Cliente)
        context['status_choices'] = dict(Cliente.ESTADOS)
        return context


client_details = ClientDetails.as_view()


class ClientCreate(EditModelView, CreateView):
    template_name = 'partners/client/form.jinja'
    form_class = CreateClientForm
    active_page = 'client-list'
    title = 'Agregar Cliente'
    perms = []

    def get_success_url(self):
        return reverse('client-details', kwargs={'pk': self.object.pk})

client_create = ClientCreate.as_view()


class ClientUpdate(EditModelView, UpdateView):
    template_name = 'partners/client/form.jinja'
    perms = []
    form_class = UpdateClientForm
    model = Cliente
    active_page = 'client-list'
    title = _('Editar Cliente')

    def get_success_url(self):
        return reverse('client-details', kwargs={'pk': self.object.pk})


client_update = ClientUpdate.as_view()


class ClientDelete(DeletePartner):
    model = Cliente
    reverse_name = 'client-list'
    perms = []


client_delete = ClientDelete.as_view()


class ClientSetStatus(ClientDetails):
    template_name = 'partners/set_role_status.jinja'
    perms = []

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        clients = Cliente.objects.request_qs(self.request)
        client = get_object_or_404(clients, pk=pk)
        status = int(self.request.POST['status'])
        assert status in dict(Cliente.ESTADOS), 'unknown client status %d' % status
        client.status = status
        client.save()
        return redirect('client-details', pk=pk)

client_set_status = ClientSetStatus.as_view()

