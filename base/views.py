import json

from django.contrib import messages
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta
from django.utils import timezone
from django.views.generic import TemplateView
from django.db.models import Count

from censo.models import Cliente
from base import display_generator
from base.data_import import TemplateSheet, trigger_import


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context=context)

    def get_context_data(self, **kwargs):
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        monday_of_this_week = monday_of_last_week + timedelta(days=7)
        clientes_x_dia = Cliente.objects.filter(fecha_ingreso__gte=monday_of_last_week,
                                                fecha_ingreso__lt=monday_of_this_week).values('fecha_ingreso').annotate(
            Count('id'))
        print clientes_x_dia
        context = super(Dashboard, self).get_context_data()
        context['data_grafico'] = clientes_x_dia
        return context


def import_template(request):
    """
    Generates XSLX template suitable for data import
    """
    doc = TemplateSheet.create(request)

    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(doc, content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="disribucion_importar.xlsx"'
    return response


class ImportForm(display_generator.BasicPage, TemplateView):
    """
    Form for importing data from Excel
    """
    template_name = 'common/import/consolidated.jinja'
    active_page = 'import'
    perms = []
    title = _('Import Data')

    def post(self, request, *args, **kwargs):
        try:
            f = request.FILES['xlsx']
        except KeyError:
            messages.error(request, _(u'Please upload a Excel file'))
            return
        trigger_import(request, f)
        return redirect('.')

    def get(self, request, **kwargs):
        return super(ImportForm, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ImportForm, self).get_context_data(**kwargs)
        return context


import_form = ImportForm.as_view()