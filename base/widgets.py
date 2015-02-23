from __future__ import unicode_literals
import json
from django.contrib.staticfiles.storage import staticfiles_storage
import pytz

from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.exceptions import FieldError

COLOR_WIDGET_JS = '''<script type="text/javascript">
                    (function($){
                        $(document).ready(function(){
                            $('#%s').each(function(i, elm){
                                $(elm).colorPicker({pickerDefault: '#FFFFFF'});
                            });
                        });
                    })('django' in window ? django.jQuery: jQuery);
                </script>
                '''


class ColorPickerWidget(widgets.TextInput):
    """
    Color Chooser Widget
    """

    class Media:
        css = {
            'all': (
                staticfiles_storage.url('css/colorPicker.css'),
            )
        }
        js = (
            staticfiles_storage.url('js/jquery.colorPicker.js'),
        )

    @staticmethod
    def render_script(id):
        return COLOR_WIDGET_JS % id

    def render(self, name, value, attrs={}):
        attrs['class'] = 'color form-control'
        if 'id' not in attrs:
            attrs['id'] = "id_%s" % name
        render = u'<div class="input-group">%s</div>' % (
            super(ColorPickerWidget, self).render(name, value, attrs))
        return mark_safe("%s%s" % (render, self.render_script(attrs['id'])))

class TCM2MCheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    """
    Multiple checkbox widget for many to many fields
    """
    title = ''

    def __init__(self, *args, **kwargs):
        if kwargs and ("attrs" in kwargs):
            self.title = kwargs["attrs"].get('title', '')
            self.checked_all = bool(kwargs['attrs'].get('checked'))
        super(TCM2MCheckboxSelectMultiple, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        empty = False
        if not self.choices:
            empty = True
        has_id = kwargs and ("attrs" in kwargs) and ("id" in kwargs["attrs"])
        label = self.title
        if not has_id:
            raise FieldError("id required")
        select_all_id = kwargs["attrs"]["id"] + "_all"
        select_all_name = args[0] + "_all"
        original = super(TCM2MCheckboxSelectMultiple, self).render(*args, **kwargs)
        original = original.replace(u'<ul id="%s">' % kwargs["attrs"]["id"], u'<ul class="list-group">') \
            .replace(u'<li>', u'<li class="list-group-item">')

        context = {'original_widget': mark_safe(original),
                   'select_all_id': select_all_id,
                   'label': label,
                   'select_all_name': select_all_name,
                   'empty': empty,
                   'checked_all': 'Checked' if self.checked_all else ''}
        return mark_safe(render_to_string('common/widgets/TCM2MCheckboxSelectMultiple.jinja', context))


class CSICheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    """
    Widget for comma separated integer
    """
    def render(self, name, value, attrs=None, choices=()):
        """
        Convert comma separated integer string to a list, since the checkbox
        rendering code expects a list (not a string)
        """
        if isinstance(value, basestring):
            value = value.split(',')
        return super(CSICheckboxSelectMultiple, self).render(name, value, attrs=attrs, choices=choices)
