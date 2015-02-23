from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from django_jinja import library
from bootstrapform_jinja.templatetags.bootstrap import add_input_classes


TOTAL_COLUMNS = 12

@library.filter
def field_list_columns(fields, columns=3, widths=None, orders=None):
    """
    Like bootstrap_columns but takes a list of fields instead of a form.
    :param fields: list of fields
    :param columns: default column number
    :param widths: dict of field widths for bootstrap grid
    :param orders: dict of fields with orders for sorting
    """
    if widths is None:
        widths = {}
    if orders is None:
        orders = {}

    width = TOTAL_COLUMNS / columns

    def field_add_width(f):
        f.width = widths.get(f.name, width)
        f.place = orders.get(f.name, float('inf'))

        return f

    def construct_rows(fields):
        all_rows = []
        current_row = []
        counter = 0
        for f in fields:
            add_input_classes(f)
            current_row.append(f)

            counter += f.width
            if counter >= TOTAL_COLUMNS:
                all_rows.append(current_row)

                counter = 0
                current_row = []

        if current_row:
            all_rows.append(current_row)

        return all_rows

    fields = map(field_add_width, fields)
    fields.sort(key=lambda f: f.place)

    rows = construct_rows(fields)

    markup_classes = {'label': '', 'value': '', 'single_value': ''}
    context = {'fields': fields, 'classes': markup_classes, 'rows': rows}
    return mark_safe(render_to_string('bootstrapform/field_list_columns.jinja', context))


@library.filter
def bootstrap_columns(form, columns=3, widths=None):
    if widths is None:
        widths = {}

    width = TOTAL_COLUMNS / columns

    def augment_field(f):
        try:
            f.place = form.Columns.order.index(f.name)
        except (AttributeError, ValueError):
            f.place = float('inf')  # Infinity

        f.width = widths.get(f.name, width)

        return f

    visible_fields = form.visible_fields()
    visible_fields = map(augment_field, visible_fields)
    visible_fields.sort(key=lambda f: f.place)

    def construct_rows(fields):
        all_rows = []
        current_row = []
        counter = 0
        for f in fields:
            add_input_classes(f)
            current_row.append(f)

            counter += f.width
            if counter >= TOTAL_COLUMNS:
                all_rows.append(current_row)

                counter = 0
                current_row = []

        if current_row:
            all_rows.append(current_row)

        return all_rows

    form.get_rows = lambda: construct_rows(visible_fields)

    markup_classes = {'label': '', 'value': '', 'single_value': ''}
    context = {'form': form, 'classes': markup_classes}
    return mark_safe(render_to_string('common/bootstrap_form_columns.jinja', context))
