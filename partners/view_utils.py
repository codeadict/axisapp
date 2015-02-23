from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.utils.translation import ugettext_lazy as _

from djgeojson.views import GeoJSONLayerView

from base.models import Label
from base.default_views import CustomListView, CustomDetailView, EditModelView


class _GenericRoleMixin():
    """
    for use here only.

    Used as mixin for RoleListView and RoleDetailView for common
    functions.
    """
    extra_items = ['nombres', 'apellidos', 'tipo_id', 'identif', 'direccion', 'nombre_comercial']
    # TODO: Add support for custom attributes
    # find_attributes = True
    order_by = ['apellidos', 'nombres', 'identif']

    def identificacion(self, obj):
        return '%s (%s)' % (obj.identif, obj.get_tipo_id_display())
    identificacion.short_description = _('Identificacion')

    def location(self, obj):
        parts = []
        if obj.barrio:
            parts.append(obj.barrio)
        if obj.sector:
            parts.append(obj.sector)
        return ', '.join(parts)

    location.short_description = _('Localizacion')


class ListFilterMixin(object):
    """
    Mixin for filtering and sorting lists
    """
    search_form = None

    def get_filter_form(self):
        if not self.search_form:
            return None

        return self.search_form(request=self.request, data=self.request.GET or None)

    def get_queryset(self):
        queryset = super(ListFilterMixin, self).get_queryset()
        form = self.get_filter_form()
        if form and form.data:
            if form.is_valid():
                queryset = form.apply(queryset)
            else:
                queryset = queryset.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListFilterMixin, self).get_context_data(**kwargs)
        context['search_form'] = self.get_filter_form()
        return context


class PartnerListView(_GenericRoleMixin, ListFilterMixin, CustomListView):
    """
    Base class for lists of partners (eg. clients, providers etc.)

    """
    template_name = 'partners/partner_list.jinja'
    related_fields = []  # for select-related prefetch
    m2m_fields = []  # for prefetch-related prefetch

    def get_queryset(self):
        qs = super(PartnerListView, self).get_queryset()
        return qs.select_related(*self.related_fields).prefetch_related(*self.m2m_fields)

    def get_item_title(self, obj):
        return u'%s' % obj.get_full_name()


class PartnerMapView(PartnerListView):
    """
    Base view for partners map
    """
    template_name = 'partners/partner_map.jinja'


class PartnerDetailView(_GenericRoleMixin, CustomDetailView):
    """
    equivalent of PartnerListView but for detail views, eg. one item.
    """
    template_name = 'partners/partner_details.jinja'
    filter_show_list = False

    def get_context_data(self, **kwargs):
        context = super(PartnerDetailView, self).get_context_data(**kwargs)
        context['title'] = self.object.get_full_name()
        return context

    def labels_dropdown(self):
        classes = 'submit-post role-set-label'
        current_labels = self.object.get_labels()
        labels = Label.objects.available_for_obj(self.object)
        for label in labels:
            color_class = ' colour_%s' % label.colour.replace('#', '')
            c = classes
            c += color_class
            if label in current_labels:
                c += ' checked_label'
            yield {
                'name': label.name,
                'url': reverse('role-set-label', kwargs={'pk': self.object.pk}),
                'classes': c,
                'color': label.colour,
                'data': {'label': label.pk}
            }