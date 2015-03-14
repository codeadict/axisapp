from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from celery import task

from censo.models import PresalesDistribution, Cliente
from base.models import Area
from django.contrib.gis.geos import GEOSGeometry


def get_context_hull_by_areas(area_id, clients_amount):
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

    # Fuck Geomodel!!!
    #Create cursor for the kmeans
    cursor = connection.cursor()

    #Prepare the query
    cursor.execute('SELECT generate_subareas(%s, %s);',
                   [str(clients_amount), str(area.id)])

    #Fetch into list all the kmeans as (id, count of point into, geo)
    result = cursor.fetchall()