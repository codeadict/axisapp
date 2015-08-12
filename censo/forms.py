from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm, Select
from django.contrib.gis.forms import GeometryField, PointField
from suit.widgets import NumberInput

from base.form_helper import GenericFilterForm, TCForm
from base.fields import CSIMultipleChoiceField
from base import widgets
from base import gis as gisform
from base.gis.widgets import SelectRelatedWithGeo
from base.models import Area, Provincia, MacroCat, Categoria, Marca, Presentacion
from censo.models import Cliente, PresalesDistribution, ActivosMercado
from partners.partner_form_helper import CreatePartnerForm, UpdatePartnerForm


class ActivosForm(ModelForm):
    class Meta:
        widgets = {
            'p': NumberInput,
            'm': NumberInput,
            'g': NumberInput,

            # Optionally you specify attrs too
            'p': NumberInput(attrs={'class': 'input-mini'}),
            'm': NumberInput(attrs={'class': 'input-mini'}),
            'g': NumberInput(attrs={'class': 'input-mini'})

        }


class InvForm(ModelForm):
    class Meta:
        widgets = {
            # Optionally you specify attrs too
            'presentacion': NumberInput(attrs={'class': 'input-mini'}),
            'envase': Select(attrs={'class': 'input-mini'}),
        }


class ClientSaveMixin(object):
    coordenadas = PointField(widget=gisform.BaseGMapWidget)

    #class Columns(object):
        #order = ['title', 'first_name', 'last_name', 'category', 'street', 'postcode', 'town', 'country',
         #        'date_of_birth', 'phone', 'mobile', 'gender', 'photo', 'timezone', 'user_email', 'agent']

    class Meta:
        exclude = ['estado',]

    def __init__(self, *args, **kwargs):
        super(ClientSaveMixin, self).__init__(*args, **kwargs)


class CreateClientForm(ClientSaveMixin, CreatePartnerForm):
    coordenadas = PointField(widget=gisform.BaseGMapWidget)
    foto = forms.ImageField(widget=widgets.SDImageWidget)

    class Meta:
        model = Cliente
        exclude = ['estado',]


class UpdateClientForm(ClientSaveMixin, UpdatePartnerForm):
    coordenadas = PointField(widget=gisform.BaseGMapWidget)
    foto = forms.ImageField(widget=widgets.SDImageWidget)

    class Meta:
        model = Cliente
        exclude = ['estado',]

    def __init__(self, **kwargs):
        super(UpdateClientForm, self).__init__(**kwargs)


class ProfileClientForm(ClientSaveMixin, UpdatePartnerForm):
    class Meta:
        model = Cliente


class ClientSearchForm(GenericFilterForm):
    created_after = forms.DateTimeField(label=_(u'Created After'))
    created_before = forms.DateTimeField(label=_(u'Created Before'))
    first_name = forms.CharField(label=_(u'Names'))
    last_name = forms.CharField(label=_(u'Last Names'))
    email = forms.EmailField(label=_(u'Email'))

    generic_fields_mapping = {
        'first_name': 'nombres__icontains',
        'last_name': 'apellidos__icontains',
        'email': 'email',
    }

    fields_mapping = {
        'created_after': 'user__date_created__gte',
        'created_before': 'user__date_created__lte'
    }
    model = Cliente

    def __init__(self, *args, **kwargs):
        super(ClientSearchForm, self).__init__(*args, **kwargs)


class ClientsMapFilterForm(TCForm):
    province = forms.ModelChoiceField(Provincia.objects.none(), required=False)
    macro_categ = forms.ModelChoiceField(MacroCat.objects.none(), required=False, label=_('Macro Category'))
    category = forms.ModelChoiceField(Categoria.objects.none(), required=False)
    brand = forms.ModelChoiceField(Marca.objects.none(), required=False)
    presentation = forms.ModelChoiceField(Presentacion.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        super(ClientsMapFilterForm, self).__init__(*args, **kwargs)
        self.fields['province'].queryset = Provincia.objects.all()
        self.fields['macro_categ'].queryset = MacroCat.objects.all()
        self.fields['category'].queryset = Categoria.objects.all()
        self.fields['brand'].queryset = Marca.objects.all()
        self.fields['presentation'].queryset = Presentacion.objects.all()


class MarketAssetsForm(forms.ModelForm):

    def __init__(self, request, client, *args, **kwargs):
        self.request = request
        self.contractor = client
        super(MarketAssetsForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.instance.pk:
            self.client.market_assets.remove(self.instance)
        ma, _ = ActivosMercado.objects.get_or_create(empresa=self.instance.empresa,
                                                      p=self.instance.p,
                                                      m=self.instance.m,
                                                      g=self.instance.g,
                                                      congelador=self.instance.congelador,
                                                      exhibidor=self.instance.exhibidor,
                                                      estante=self.instance.estante,
                                                      rotulo=self.instance.rotulo,
                                                      mesas=self.instance.mesas,
                                                      sillas=self.instance.sillas)
        self.client.market_assets.add(ma)

    class Meta:
        model = ActivosMercado
        fields = ['empresa', 'p', 'm', 'g', 'congelador', 'exhibidor', 'estante', 'rotulo', 'mesas', 'sillas']


class GenerateDistributionForm(TCForm):
    """
    Form used to give params to generate distribution view
    """
    area = forms.ChoiceField(label=_('Area'), help_text=_('Area where you want to perform the distribution'))
    points_per_polygon = forms.IntegerField(label=_('Clients per Polygon'), required=True,
                                            help_text=_('The amount of clients in each generated polygon'))

    def __init__(self, *args, **kwargs):
        super(GenerateDistributionForm, self).__init__(*args, **kwargs)
        self.fields['area'].choices = [(o.id, str(o)) for o in Area.objects.all()]


class UpdateDistributionForm(UpdatePartnerForm):
    frequency = CSIMultipleChoiceField(label=_('Visit Days'), choices=PresalesDistribution.WEEKDAYS, required=False)
    polygon = GeometryField(widget=gisform.BaseGMapWidget)

    class Meta:
        model = PresalesDistribution
        fields = ['name', 'route_type', 'assigned_seller', 'frequency', 'initial_client', 'final_client', 'polygon']
        exclude = ['clients']

    def __init__(self, **kwargs):
        super(UpdateDistributionForm, self).__init__(**kwargs)
        self.clients_qs = self.instance.clients.all()
        geo_select_widget_objects = []
        for client in self.clients_qs:
            if client.coordenadas:
                element = {
                    'id': client.id,
                    'lat': client.coordenadas.x,
                    'lon': client.coordenadas.y,
                    'title': client.get_full_name()
                }
                geo_select_widget_objects.append(element)

        self.fields['initial_client'].widget = SelectRelatedWithGeo(objects=geo_select_widget_objects)
        self.fields['final_client'].widget = SelectRelatedWithGeo(objects=geo_select_widget_objects)
        self.fields['initial_client'].qs = self.clients_qs
        self.fields['final_client'].qs = self.clients_qs
