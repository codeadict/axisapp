from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from celery import task

from censo.models import PresalesDistribution, Cliente
from base.models import Area


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

    #Erase all the previous data about this area
    presales_old_list = PresalesDistribution.objects.all()
    presales_old_list.delete()

    #Create cursor for the kmeans
    cursor = connection.cursor()

    clients = Cliente.objects.filter(coordenadas__within=area.poligono)
    print clients.count()

    #We don't need this, thanks to GeoModel.. ;)
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

    print areas_amount

    #Prepare the query
    cursor.execute('SELECT kmeans, count(*), ST_ConvexHull(ST_Collect(geom)) AS geom '
                   'FROM (SELECT kmeans(ARRAY[ST_X(geom), ST_Y(geom)], %s) OVER (), geom '
                   'FROM %s WHERE ST_X(geom) IS NOT NULL AND ST_Y(geom) IS NOT NULL '
                   'AND ST_Contains(%s, %s.geom)) '
                   'AS ksub GROUP BY kmeans ORDER BY kmeans;',
                   [areas_amount, 'censo_cliente', area.poligono, 'censo_cliente', ])

    #Fetch into list all the kmeans as (id, count of point into, geo)
    result = cursor.fetchall()
    result.pop(0)

    for convex_hull_area in result:
        #Create teh object
        try:
            ps_dist_obj = PresalesDistribution()
            # Save the convex hull polygon
            ps_dist_obj.polygon = convex_hull_area[2]
            #Save possible name as Area_name+#Subarea
            ps_dist_obj.name = str(area.nombre) + str(convex_hull_area[0])
            # Get he clients inside the convex hull
            clients_into_area = Cliente.objects.filter(coordenadas__within=convex_hull_area[2])
            # We need to save it first, to save the clients later
            ps_dist_obj.save()
        except TypeError:
            continue
        #for client in clients_into_area:
            #print client
            #ps_dist_obj.clients.add(client)
            #ps_dist_obj.save()
