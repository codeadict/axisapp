import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.db import connection
from celery import task

from base.default_views import CustomListView, ModalMixin
from censo.models import PresalesDistribution, Cliente
from base.models import Area
from censo.forms import GenerateDistributionForm

log = logging.getLogger(__name__)


class DistributionList(CustomListView):
    """
    View to list and map distribution models as well as generating new ones
    """
    template_name = 'distribution/list.jinja'
    active_page = 'presales-client-distribution'
    model = PresalesDistribution
    perms = []
    # detail_view = ''
    display_items = [
        'name',
        'assigned_seller',
    ]
    button_menu = [
        {
            'name': _('Generate New Distribution'), 'rurl': 'generate-distribution', 'data':
            {'toggle': 'crud-modal', 'title': _('Generate Pre-Sales Distribution')}
        },
    ]

    def get_search_form(self):
        return NotImplementedError

    def get_queryset(self):
        qs = super(DistributionList, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super(DistributionList, self).get_context_data(**kwargs)
        return context


distribution_list = DistributionList.as_view()


class GenerateDistribution(ModalMixin, FormView):
    """
    Launches a modal and generates a distribution based on area_id and number of points per distribution polygon
    """
    form_class = GenerateDistributionForm
    modal_template_name = 'common/modals/generate_distribution_modal.jinja'
    perms = []

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if self.form.is_valid():
            # TODO: Here we generate the distribution
            # Just for test
            #self.get_context_hull_by_areas.delay(2, 50)
            area = request.post['area']
            points_per_polygon = request.post['points_per_polygon']
            self.get_context_hull_by_areas.delay(int(area), int(points_per_polygon))

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('presales-client-distribution')

    @task
    def get_context_hull_by_areas(self, area_id, clients_amount):
        """
        :param area_id:
        :param clients_amount:
        :return: void
        """
        #Get the area if exist
        try:
            area = Area.objects.get(id=area_id)
        except ObjectDoesNotExist:
            return

        #Erase all the previous data about this area
        presales_old_list = PresalesDistribution.objects.filter(polygon__within=area.poligono)
        presales_old_list.delete()

        #Create cursor for the kmeans
        cursor = connection.cursor()

        clients = Cliente.objects.filter(coordenadas__within=area.poligono)

        #We dont need thi, thanks to GeoModel.. ;)
        """cursor.execute('(SELECT censo_cliente.* '
                       'FROM censo_cliente, base_area '
                       'WHERE ST_Contains(base_area.poligono, censo_cliente.geom) '
                       'AND base_area.id = %i)', [area.id])
        clients_per_area = cursor.fetchall()"""

        areas_amount = 0

        if clients:
            try:
                #We need to split the number of client to get the specific amount of areas
                areas_amount = clients.count()/clients_amount
            except ZeroDivisionError:
                # We need to check if the areas_amount is under 0
                # If is it, just set it to 1 (default)
                areas_amount = 1
            else:
                if areas_amount < 0:
                    areas_amount = 1

        #Prepare the query
        cursor.execute('SELECT kmeans, count(*), ST_ConvexHull(ST_Collect(geom)) AS geom '
                       'FROM (SELECT kmeans(ARRAY[ST_X(geom), ST_Y(geom)], %s) OVER (), geom '
                       'FROM censo_cliente WHERE ST_X(geom) IS NOT NULL AND ST_Y(geom) IS NOT NULL ) '
                       'AS ksub GROUP BY kmeans ORDER BY kmeans;', [areas_amount])
        
        #Fetch into list all the kmeans as (id, count of point into, geo)
        result = cursor.fetchall()

        for convex_hull_area in result:
            #Create teh object
            ps_dist_obj = PresalesDistribution()
            # Save the convex hull polygon
            ps_dist_obj.polygon = convex_hull_area[2]
            #Save possible name as Area_name+#Subarea
            ps_dist_obj.name = str(area.nombre) + str(convex_hull_area[0])
            # Get he clients inside the convex hull
            clients_into_area = Cliente.objects.filter(coordenadas__within=convex_hull_area[2])
            # We need to save it first, to save the clients later
            ps_dist_obj.save()
            #Save them into the clients
            ps_dist_obj.clients.add(clients_into_area)
            ps_dist_obj.save()


distribution_generate = GenerateDistribution.as_view()