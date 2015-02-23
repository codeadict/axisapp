import itertools
import operator
import logging
from bootstrap3_datetime.widgets import DateTimePicker

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.views.generic.base import RedirectView

import watson

from .fields import CSIMultipleChoiceField

logger = logging.getLogger('django')


# everything should relapse to the same valid date format: '%Y-%m-%d %H:%M:%S'
# the "datetime" formats are generated afterwards.
# dj_date and dj_time related to django formatting (in the order they are tried),
# mt_date and mt_time related to moment.js/bootstrap datepicker formatting
DATETIME_FORMATS = {
    # Input and output
    1: {
        'date_name': 'dd/mm/yyyy',
        'dj_date': ['%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d'],
        'mt_date': 'DD/MM/YYYY',
        'tpl_date': '%d/%m/%Y',
        'time_name': 'HH:MM',
        'dj_time': ['%H:%M', '%H:%M:%S'],
        'mt_time': 'HH:mm',
        'tpl_time': '%H:%M',
        'tpl_datetime': '%d/%m/%Y %H:%M',
        'day_first': True
    },
    2: {
        'date_name': 'dd/mm/yyyy',
        'dj_date': ['%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d'],
        'mt_date': 'DD/MM/YYYY',
        'tpl_date': '%d/%m/%Y',
        'time_name': 'HH:MM am/pm',
        'dj_time': ['%I:%M %p', '%I:%M:%S %p', '%H:%M:%S'],
        'mt_time': 'hh:mm a',
        'tpl_time': '%I:%M %p',
        'tpl_datetime': '%d/%m/%Y %I:%M %p',  # TODO: Not sure dj_time is correct here
        'day_first': True
    },
    3: {
        'date_name': 'mm/dd/yyyy',
        'dj_date': ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d'],
        'mt_date': 'MM/DD/YYYY',
        'tpl_date': '%m/%d/%Y',
        'time_name': 'HH:MM',
        'mt_time': 'HH:mm',
        'dj_time': ['%H:%M', '%H:%M:%S'],
        'tpl_time': '%H:%M',
        'tpl_datetime': '%m/%d/%Y %H:%M',
        'day_first': False
    },
    4: {
        'date_name': 'mm/dd/yyyy',
        'dj_date': ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d'],
        'mt_date': 'MM/DD/YYYY',
        'tpl_date': '%m/%d/%Y',
        'time_name': 'HH:MM am/pm',
        'dj_time': ['%I:%M %p', '%I:%M:%S %p', '%H:%M:%S'],
        'mt_time': 'hh:mm a',
        'tpl_time': '%I:%M %p',
        'tpl_datetime': '%m/%d/%Y %I:%M %p',  # TODO: Not sure dj_time is correct here
        'day_first': False
    },
    5: {
        'date_name': 'yyyy-mm-dd',
        'dj_date': ['%Y-%m-%d', '%y-%m-%d'],
        'mt_date': 'YYYY-MM-DD',
        'tpl_date': '%Y-%m-%d',
        'time_name': 'HH:MM',
        'dj_time': ['%H:%M', '%H:%M:%S'],
        'mt_time': 'HH:mm',
        'tpl_time': '%H:%M',
        'tpl_datetime': '%Y-%m-%d %H:%M',
        'day_first': True
    },

    # Output only
    100: {
        'tpl_date': '%d %B %Y, %a',
        'tpl_time': '%H:%M',
        'tpl_datetime': '%d %B %Y, %a %H:%M',
        'day_first': True
    },
    101: {
        'tpl_date': '%d %B %Y, %A',
        'tpl_time': '%H:%M',
        'tpl_datetime': '%d %B %Y, %A %H:%M',
        'day_first': True
    },
}

for dfid, df in DATETIME_FORMATS.items():
    if 'dj_date' in df:
        DATETIME_FORMATS[dfid]['dj_datetime'] = [' '.join(v) for v in itertools.product(df['dj_date'], df['dj_time'])]
        DATETIME_FORMATS[dfid]['mt_datetime'] = '%(mt_date)s %(mt_time)s' % df
        DATETIME_FORMATS[dfid]['datetime_name'] = '%(date_name)s %(time_name)s' % df


def get_dt_format(request):
    """
    gets the DATETIME_FORMATS info from user on a request.
    """
    return DATETIME_FORMATS[1]


class GroupedChoiceField(forms.ModelChoiceField):
    group_lookup = None
    value_lookup = 'name'

    def _invalidate_choices(self):
        assert self.group_lookup, 'You should not use GroupedChoiceField directly'
        # Black magic works here
        choices = map(self._construct_choice, self.queryset.order_by(self.group_lookup))
        grouped = itertools.groupby(choices, key=operator.itemgetter(2))
        grouped_choices = [(g[0], map(lambda l: l[:2], g[1])) for g in grouped]
        # End of black magic (actually, pretty similar to Django's {% regroup %} filter
        self.choices = grouped_choices

    def _set_queryset(self, queryset):
        super(GroupedChoiceField, self)._set_queryset(queryset)
        self._invalidate_choices()

    def _construct_choice(self, s):
        return s.pk, self._deep_getattr(s, self.value_lookup), self._deep_getattr(s, self.group_lookup)

    @staticmethod
    def _deep_getattr(obj, attr_name, splitter='__'):
        for i in attr_name.split(splitter):
            obj = getattr(obj, i)
        return obj


class _TCFormMix(object):
    required_css_class = 'required'
    exclude_from_request_qs = {ContentType}
    apply_request_qs = False

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.view_kwargs = kwargs.pop('view_kwargs', None)
        super(_TCFormMix, self).__init__(*args, **kwargs)

        self._dt_format = None
        self.process_dt_format()
        self.process_select_multiple()
        if self.apply_request_qs:
            self.model_choice_request_qs()

    def process_dt_format(self):
        for f in self.fields:
            if isinstance(self.fields[f], forms.DateField):
                self.fields[f].widget = DateTimePicker(attrs={'data-format': self.dt_format['mt_date']},
                                                       options={'format': self.dt_format['mt_date'],
                                                                'pickTime': False, 'startDate': '1/1/1900'})
                self.fields[f].input_formats = self.dt_format['dj_date']
            elif isinstance(self.fields[f], forms.DateTimeField):
                self.fields[f].widget = DateTimePicker(attrs={'data-format': self.dt_format['mt_datetime']},
                                                       options={'format': self.dt_format['mt_datetime'],
                                                                'pickSeconds': False, 'startDate': '1/1/1900'})
                self.fields[f].input_formats = self.dt_format['dj_datetime']

    def process_select_multiple(self):
        for f in self.fields:
            if isinstance(self.fields[f], CSIMultipleChoiceField):
                # we don't change the widget on these fields
                continue
            if isinstance(self.fields[f].widget, forms.SelectMultiple):
                self.fields[f].widget = forms.CheckboxSelectMultiple(choices=self.fields[f].choices)
                self.fields[f].empty_label = None
                wrong_help = u'Hold down "Control", or "Command" on a Mac, to select more than one.'
                self.fields[f].help_text = self.fields[f].help_text.replace(wrong_help, '')

    def model_choice_request_qs(self):
        for f in self.fields:
            if isinstance(self.fields[f], forms.ModelChoiceField):
                if self.fields[f].queryset is None:
                    # FIXME why does this happen?
                    continue
                if self.fields[f].queryset.model in self.exclude_from_request_qs:
                    continue
                if hasattr(self.fields[f].queryset, 'request_qs'):
                    self.fields[f].queryset = self.fields[f].queryset.request_qs(self.request)
                else:

                    logger.error('Queryset has not method "request_qs": %s', self.fields[f].queryset)

    @property
    def dt_format(self):
        if not self._dt_format:
            self._dt_format = get_dt_format(self.request)
        return self._dt_format


class TCForm(_TCFormMix, forms.Form):
    """
    Descendant of forms.Form which
    * accepts request as a kwargs and makes it available as a class attribute
    * accepts view_kwargs as kwarg and adds that as a class attribute
    * converts any DateField or DateTimeField to use DateTimePicker honouring branch date format
    """
    pass


class TCModelForm(_TCFormMix, forms.ModelForm):
    """
    descendant of forms.ModelForm which
    * accepts request as a kwargs and makes it available as a class attribute
    * accepts view_kwargs as kwarg and adds that as a class attribute
    * converts any DateField or DateTimeField to use DateTimePicker honouring branch date format
    """
    pass


class GenericFilterForm(TCForm):
    required_css_class = 'required'
    search = forms.CharField(label=_(u'Buscar'))

    first_name = forms.CharField(label=_(u'Nombres'))
    last_name = forms.CharField(label=_(u'Apellidos'))
    email = forms.EmailField(label=_(u'Email'))

    generic_fields_mapping = {
        'first_name': 'nombres__icontains',
        'last_name': 'apellidos__icontains',
        'email': 'email',
    }
    fields_mapping = {}

    model = None
    attributes = []
    # list or set of fields which won't be processed by default apply, these can be used on an extended apply method
    fields_ignore = set()

    def __init__(self, *args, **kwargs):
        super(GenericFilterForm, self).__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].required = False
            if isinstance(self.fields[f], forms.CharField):
                self.fields[f].widget.attrs.update(placeholder=self.fields[f].label)
                self.fields[f].label = ''

    def apply(self, qs):
        for k, v in self.cleaned_data.items():
            if not v or k in self.fields_ignore:
                continue
            mapping = self.generic_fields_mapping.copy()
            mapping.update(self.fields_mapping)

            lookup = mapping.get(k)
            if lookup:
                qs = qs.filter(**{lookup: v})
            elif k == 'search':
                qs = watson.filter(qs, v)

        return qs


