from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm, Select
from suit.widgets import NumberInput

from base.form_helper import GenericFilterForm, TCForm
from base.models import Area
from censo.models import Cliente
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
            'presentacion': Select(attrs={'class': 'input-mini'}),
            'envase': Select(attrs={'class': 'input-mini'}),
        }


class ClientSaveMixin(object):
    #class Columns(object):
        #order = ['title', 'first_name', 'last_name', 'category', 'street', 'postcode', 'town', 'country',
         #        'date_of_birth', 'phone', 'mobile', 'gender', 'photo', 'timezone', 'user_email', 'agent']

    def __init__(self, *args, **kwargs):
        super(ClientSaveMixin, self).__init__(*args, **kwargs)


class CreateClientForm(ClientSaveMixin, CreatePartnerForm):
    class Meta:
        model = Cliente
        exclude = ['agency', 'user']


class UpdateClientForm(ClientSaveMixin, UpdatePartnerForm):
    class Meta:
        model = Cliente

    def __init__(self, **kwargs):
        super(UpdateClientForm, self).__init__(**kwargs)


class ProfileClientForm(ClientSaveMixin, UpdatePartnerForm):
    class Meta:
        model = Cliente
        #exclude = ['agency', 'user', 'qualifications', 'skills', 'calendar_colour', 'status']


class ClientSearchForm(GenericFilterForm):
    recipient = forms.CharField(label=_(u'Service Recipient name'))
    created_after = forms.DateTimeField(label=_(u'Created After'))
    created_before = forms.DateTimeField(label=_(u'Created Before'))

    fields_mapping = {
        'recipient': 'paid_recipients__user__first_name__icontains',
        'created_after': 'user__date_created__gte',
        'created_before': 'user__date_created__lte'
    }
    model = Cliente

    def __init__(self, *args, **kwargs):
        super(ClientSearchForm, self).__init__(*args, **kwargs)


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
