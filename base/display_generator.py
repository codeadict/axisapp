import copy
import datetime
from cached_property import cached_property
from decimal import Decimal
import logging

from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, NoReverseMatch

logger = logging.getLogger('django')


class BasicPage(object):
    _ATTR_NOT_FOUND = '__ATTR_NOT_FOUND__'
    title = None
    button_menu = []
    active_page = -1

    def _get_attr(self, name):
        v = getattr(self, name, self._ATTR_NOT_FOUND)
        if v == self._ATTR_NOT_FOUND and getattr(self, 'object', False):
            v = getattr(self.object, name, self._ATTR_NOT_FOUND)
        if v == self._ATTR_NOT_FOUND:
            raise Exception(u'%s not found on %s instance or self.object' % (name, self.__class__.__name__))
        if hasattr(v, '__call__'):
            return v()
        return v

    def _show_button(self, button):
        if not isinstance(button, dict):
            return True
        if 'show_if' not in button:
            return True
        return self._get_attr(button['show_if'])

    def _process_buttons(self, button_group):
        if not isinstance(button_group, dict):
            return [self._process_buttons(button) for button in button_group if self._show_button(button)]
        return self._process_button(button_group)

    def _process_button(self, button):
        if 'urlfunc' in button:
            button['url'] = self._get_attr(button['urlfunc'])
        elif 'dropdown' in button:
            if isinstance(button['dropdown'], basestring) and button['dropdown'].startswith('func:'):
                fname = button['dropdown'].split(':', 1)[1]
                button['dropdown'] = list(getattr(self, fname)())
            for drop in button['dropdown']:
                if 'urlfunc' in drop:
                    drop['url'] = self._get_attr(drop['urlfunc'])
        return button

    def get_buttons(self):
        return self.button_menu

    def get_process_buttons(self):
        return self._process_buttons(self.get_buttons())

    def _object_url(self, rev):
        """
        try to generate url for object from reverse string and object pk
        """
        try:
            return reverse(rev)
        except NoReverseMatch, e:
            if getattr(self, 'object', False):
                return reverse(rev, kwargs={'pk': self.object.pk})
            raise e

    def convert_to_string(self, value, field=None):
        if hasattr(value, '__call__'):
            value = value()
        if value in (None, ''):
            return mark_safe('&mdash;')
        if field and len(field.choices) > 0:
            cdict = dict(field.choices)
            if value in cdict:
                return cdict[value]
        # not being used as it confuses people, might get replaced in time with a link to send a TC2 message
        # if isinstance(field, models.EmailField):
        #     return u'<a href="mailto:%s" target="blank">%s</a>' % (value, value)
        if isinstance(field, models.URLField):
            return mark_safe(u'<a href="%s" target="blank">%s</a>' % (value, value))
        if isinstance(field, models.EmailField):
            return mark_safe(u'<a href="mailto:%s" target="blank">%s</a>' % (value.lower(), value))
        if isinstance(value, bool):
            icon = value and 'ok' or 'remove'
            return mark_safe(u'<span class="glyphicon glyphicon-%s"></span>' % icon)
        if isinstance(value, (list, tuple, QuerySet)):
            return u', '.join(self.convert_to_string(v) for v in value)
        if isinstance(value, (long, int, float, Decimal)):
            return self._find_base(value)
        return value

    def get_context_data(self, **kwargs):
        context = super(BasicPage, self).get_context_data(**kwargs)
        context['title'] = self.title or ''
        context['button_menu'] = self.get_process_buttons()
        context['obj_url'] = self._object_url
        self.request.active_page = self.active_page
        return context


def display_cash(amount, currency_symbol, none_value='0'):
    """
    Return formatted string on float or decimal with currency
    :param amount: float or decimal
    :param none_value: string to return if amount is None
    :return: amount formatted as a string with currency_symbol
    """
    if amount is None:
        return none_value
    return u'%s%0.2f' % (currency_symbol or '', amount)


class TCDisplayMixin(object):
    """
    General purpose mixin for displaying either lists or item details, can be used in views or non view classes
    eg. PDF renders.
    """
    currency_symbol = None
    request = None

    def get_context_data(self, **kwargs):
        context = {}
        sup = super(TCDisplayMixin, self)
        if hasattr(sup, 'get_context_data'):
            context = sup.get_context_data(**kwargs)
        return context

    @staticmethod
    def _find_base(value):
        if value > 1e3:
            return u'{:,}'.format(value)
        elif isinstance(value, float):
            return u'%0.2f' % value
        else:
            return u'%d' % value


class ItemDisplayMixin(TCDisplayMixin, BasicPage):
    """
    ItemDisplayMixin works with ListView and DetailView to simplify the process of listing and displaying a model.

    This class should be "mixed in" before ListView or DetailView so it can override their attributes.
    """

    #: an instance of django.db.models.Model to be displayed, this is already required for ListView or DetailView
    model = None

    #: list of references to attributes of instances of the model, items maybe
    #: * field names
    #: * references to related fields either using Django's "thing__related_ob" syntax or "thing.related_ob" syntax
    #: * references to functions in the class, they should be identified by "func|name_of_function" the function
    #:   should take an instance of the model as it's only argument as in "def name_of_function(self, obj):..."
    #: * pattern for a reverse link to a page in the form at "rev|view-name|field_or_func" field_or_func
    #:   may be any of the above options eg. "thing__related_ob", "thing.related_ob" or "func|name_of_function"
    #: * any of the above may be the second value in a tuple where the first value is a verbose name
    #:   to use for the field if you don't like it's standard verbose name.
    display_items = []

    #: subset of display_items which are considered "long" eg. TextField's which should be displayed
    #: full width not in columns, if in long_items an attribute will be yielded by gen_object_long
    #: otherwise by gen_object_short
    long_items = []

    #: whether or not to search for AttributeValues associated with the model
    find_attributes = False

    #: field to order the model by, if None no ordering is performed here
    order_by = None

    #: number of items to show on each each page
    paginate_by = 20

    #: name of view showing details of the model suitable for passing to reverse
    #: this is passed to the template and may be left blank when this actually is a detail view
    detail_view = None

    #: whether to filter AttributeValue's on list_show = True
    filter_show_list = False

    _LOCAL_FUNCTION = 'func!'

    def __init__(self):
        self._model_meta = self.model._meta
        self._field_names = [f.name for f in self._model_meta.fields]
        self._item_info_cache = None
        self._extra_attrs = []

    def get_context_data(self, **kwargs):
        """
        Overrides standard the standard get_context_data to provide the following in the context:
            gen_object_short: generator for short attributes of each item
            gen_object_long: generator for long attributes of each item
            get_item_title: returns the title of any object
            plural_name: the plural name of the model
            title: if not already set is set to plural_name
            detail_view: from above

        :param kwargs: standard get_context_data kwargs
        :return: the context
        """
        context = super(ItemDisplayMixin, self).get_context_data(**kwargs)
        context['gen_object_short'] = self.gen_object_short
        context['gen_object_long'] = self.gen_object_long
        context['get_item_title'] = self.get_item_title
        context['plural_name'] = self._model_meta.verbose_name_plural.title()
        if not context['title']:
            context['title'] = context['plural_name']
        context['detail_view'] = getattr(self, 'get_detail_view_url', lambda: self.detail_view)()
        return context

    def get_queryset(self):
        """
        Overrides standard the standard get_queryset to order the qs and call select_related.
        :return:
        """
        queryset = super(ItemDisplayMixin, self).get_queryset()
        if self.order_by:
            queryset = queryset.order_by(*self.order_by)
        return self.select_related(self._prefetch_attr_values(queryset))

    def _prefetch_attr_values(self, queryset):
        """
        Prefetch AttributeValues if find_attributes is true.

        You shouldn't need to override this, use select_related instead.

        :param queryset: the queryset from get_queryset
        :return: the queryset from get_queryset
        """
        if self.find_attributes:
            queryset = queryset.prefetch_related('extra_attrs__definition')
        return queryset

    def select_related(self, queryset):
        """
        By default ItemDisplayMixin attempts to reduce the number of queries required to render a list of items
        or a single item by calling qs.select_related(). However this may not fetch all required fields
        and may fetch unneeded fields, therefore this function can be overridden to extend the query with
        custom select_related and prefetch_related calls.

        Note AttributeValues are prefetch separately by prefetch_attr_values so you can override this without
        worrying about that

        :param queryset: the queryset from get_queryset
        :return: the queryset from get_queryset
        """
        return queryset.select_related()

    def gen_object_short(self, obj):
        """
        Generator of (name, value) pairs which are short for a given object.

        Will return AttributeValues attributes after display_items attributes if find_attributes is true.

        :param obj: the object to to find generate attributes for
        :return: list of (name, value) pairs which are short.
        """
        for field, attr_name, verbose_name, rev_view_name, is_long in self._item_info:
            if not is_long:
                yield self._display_value(obj, field, attr_name, verbose_name, rev_view_name)
        if self.find_attributes:
            for name_attr in self._obj_attrs(obj, True):
                yield name_attr

    def gen_object_long(self, obj):
        """
        Generator of (name, value) pairs which are long for a given object.

        Will return AttributeValues attributes after display_items attributes if find_attributes is true.

        :param obj: the object to to find generate attributes for
        :return: list of (name, value) pairs which are long.
        """
        for field, attr_name, verbose_name, rev_view_name, is_long in self._item_info:
            if is_long:
                yield self._display_value(obj, field, attr_name, verbose_name, rev_view_name)
        if self.find_attributes:
            for name_attr in self._obj_attrs(obj, False):
                yield name_attr

    def get_item_title(self, obj):
        """
        returns the title of an instance of model, the default is dump and just calls str. But can be
        override to provide more intelligent functionality.

        This is made available in the context to be used in templates.

        :param obj: an instance of model.
        :return: it's title (or name)
        """
        return unicode(obj)

    @cached_property
    def _item_info(self):
        """
        Returns a list of tuples for each item in display_items, each of which contains
            field: the type of the field of the attribute, 'func!' if it's a function
            attr_name: the attribute name from display_items
            verbose_name: the verbose name of that field
            rev_view_name: view name to reverse to get item url, None if no reverse link
            is_long: boolean indicating if the field should be considered "long" (eg. is in long_items)

        After the first call the list is cached to improve performance.
        :return: list of tuples for each item in display_items
        """
        return [self._get_attr_info(vn) for vn in self._all_display_items]

    @cached_property
    def _all_display_items(self):
        """
        all items to show from both display_items and long_items.
        """
        check_disp_items = [item[-1] if isinstance(item, tuple) else item for item in self.display_items]
        return tuple(self.display_items) + tuple(filter(lambda i: i not in check_disp_items, self.long_items))

    def _get_attr_info(self, attr_name):
        """
        Finds the values for each tuple returned by _item_info.

        :param attr_name: value direct from display_items
        :return: tuple see _item_info
        """
        verbose_name = None
        rev_view_name = None
        is_long = lambda at_name: at_name in self.long_items
        if isinstance(attr_name, tuple):
            verbose_name, attr_name = attr_name

        if attr_name.startswith('rev|'):
            parts = attr_name.split('|', 2)
            _, rev_view_name, attr_name = parts

        if attr_name.startswith('func|'):
            func_name = attr_name.split('|')[1]
            if verbose_name is None:
                verbose_name = self._get_short_description(self, func_name) or func_name
            return self._LOCAL_FUNCTION, func_name, verbose_name, rev_view_name, is_long(attr_name)

        model, meta, field_names = self.model, self._model_meta, self._field_names
        attr_name_part = None
        field = None
        for attr_name_part in self._split_attr_name(attr_name):
            if attr_name_part in field_names:
                field = meta.get_field_by_name(attr_name_part)[0]
                if field.rel:
                    model = field.rel.to
                    meta = model._meta
                    field_names = [f.name for f in meta.fields]
        if not verbose_name:
            # priority_short_description has priority over field.verbose_name even when it's on a related model
            verbose_name = self._get_short_description(model, attr_name_part, 'priority_short_description')
            if not verbose_name:
                if field:
                    verbose_name = field.verbose_name
                else:
                    verbose_name = self._get_short_description(model, attr_name_part)
                if not verbose_name:
                    verbose_name = attr_name
        return field, attr_name, verbose_name, rev_view_name, is_long(attr_name)

    @staticmethod
    def _split_attr_name(attr_name):
        """
        split an attribute name either on '__' or '.'
        """
        return attr_name.replace('__', '.').split('.')

    @staticmethod
    def _get_short_description(obj, attr_name, prop_name='short_description'):
        """
        get a property of an object's attribute by name.
        :param obj: object to look at
        :param attr_name: name to get short_description for
        :param prop_name: name of property to get, typically "short_description"
        :return: property value or None
        """
        attr = getattr(obj, attr_name, None)
        if attr:
            return getattr(attr, prop_name, None)

    def _display_value(self, obj, field, attr_name, verbose_name, rev_view_name):
        """
        Generates a value for an attribute, optionally generate it's url and make it a link and returns it
        together with with it's verbose name.

        If the attribute name refers to a function the value is returned raw (after reversing if rev_view_name,
        otherwise it's processed by convert_to_string.

        :param obj: any instance of the model to get the value from.
        :param field: field type, see _item_info
        :param attr_name: attribute name, see _item_info
        :param verbose_name: verbose name, see _item_info
        :param rev_view_name: view name, see _item_info
        :return: tuple containing (verbose_name, value)
        """
        if field == self._LOCAL_FUNCTION:
            value = getattr(self, attr_name)(obj)
        else:
            value = self._get_object_value(obj, attr_name)
        url = None
        if rev_view_name and hasattr(value, 'pk'):
            rev_tries = [
                {'viewname': rev_view_name},
                {'viewname': rev_view_name, 'kwargs': {'pk': value.pk}},
                {'viewname': rev_view_name, 'args': (value.pk,)},
            ]
            for rev_try in rev_tries:
                try:
                    url = reverse(**rev_try)
                except NoReverseMatch:
                    pass
                else:
                    break
            if url is None:
                logger.error(u'No reverse found for "%s"' % rev_view_name)

        if field != self._LOCAL_FUNCTION:
            value = self.convert_to_string(value, field)

        if rev_view_name and url:
            value = u'<a href="%s">%s</a>' % (url, value)
        return verbose_name, value

    def _get_object_value(self, obj, attr_name):
        """
        Chomp through attribute names from display_items to get the attribute or related attribute
        from the object

        :param obj: the object to find the attribute for
        :param attr_name: the attribute name
        :return: the attribute
        """
        for b in self._split_attr_name(attr_name):
            if obj:
                obj = getattr(obj, b)
        return obj