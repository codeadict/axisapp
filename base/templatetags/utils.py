import json
import decimal
import datetime as _datetime
from time import mktime
from django_jinja import library
from django.utils.safestring import mark_safe
from django.utils import formats


class UniversalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return u'%0.2f' % obj
        if isinstance(obj, _datetime.datetime):
            return obj.isoformat()
        if obj.__class__.__name__ == '__proxy__':  # FIXME is there a better way of doing this?
            return obj.encode('utf8')
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            print type(obj)
            return u'%s: %r' % (obj.__class__.__name__, obj)


@library.filter
def tojson(obj):
    return mark_safe(json.dumps(obj, indent=2, cls=UniversalEncoder))


@library.filter
def tojsonpre(obj):
    return mark_safe(u'<pre>\n%s\n</pre>' % tojson(obj))


@library.filter
def tostr(obj):
    return unicode(obj)


@library.filter
def formfields(form):
    return mark_safe(u'<div style="margin: 10px 0"><pre>Form Fields:\n%s\n</pre></div>' %
                     u'\n'.join(u'%s (%s) required: %r' % (n, v.__class__.__name__, v.required)
                               for n, v in form.fields.items()))


@library.filter
def is_iter(obj):
    return hasattr(obj, '__iter__')


@library.global_function
def add_field_attrs(field, extra_attrs):
    for k, v in extra_attrs.items():
        new_val = field.field.widget.attrs.get(k, '') + ' ' + v
        field.field.widget.attrs[k] = new_val.strip()
    return mark_safe(field)


@library.global_function
def curtail(string, max_len=80):
    if len(string) < (max_len - 3):
        return string
    return u'%s...' % string[:(max_len - 3)]


@library.filter
def date(dt, d_format=None):
    """
    Formats a datetime as a date according 
    to the browsers locale.
    """
    if dt in (None, ''):
        return ''
    if d_format:
        return dt.strftime(d_format)
    return formats.date_format(dt, 'SHORT_DATE_FORMAT')


@library.filter
def time(dt, t_format=None):
    """
    Formats a datetime as a time according 
    to the browsers locale.
    """
    if dt in (None, ''):
        return ''
    if t_format:
        return dt.strftime(t_format)
    return formats.time_format(dt, 'TIME_FORMAT')


@library.filter
def datetime(dt, dt_format=None):
    """
    Formats a datetime as a full datetime according 
    to the browsers locale.
    """
    if dt in (None, ''):
        return ''
    if dt_format:
        return dt.strftime(dt_format)
    return u'%s %s' % (time(dt), date(dt))


@library.filter
def timestamp(dt):
    """
    Formats a datetime as a timestamp
    """
    return int(mktime(dt.timetuple()))
