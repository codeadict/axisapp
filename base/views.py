from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from django.views.generic import TemplateView
from django.db.models import Count
from censo.models import Cliente


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context=context)

    def get_context_data(self, **kwargs):
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        monday_of_this_week = monday_of_last_week + timedelta(days=7)
        clientes_x_dia = Cliente.objects.filter(fecha_ingreso__gte=monday_of_last_week, fecha_ingreso__lt=monday_of_this_week).values('fecha_ingreso').annotate(Count('id'))
        print clientes_x_dia
        context =  super(Dashboard, self).get_context_data()
        context['data_grafico'] = clientes_x_dia
        return context