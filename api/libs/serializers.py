import geojson

from rest_framework_gis import serializers


def create_feature(instance, geo_field, fields):
    """
    Create a geojson feature from a single instance
    """
    data = instance.json

    if geo_field not in data:
        # Return an empty feature
        return geojson.Feature()

    points = data.get(geo_field).split(';')

    if len(points) == 1:
            # only one set of coordinates -> Point
            point = points[0].split()
            geometry = geojson.Point((float(point[1]), float(point[0])))
    elif len(points) > 1:
        # More than one set of coordinates -> Either LineString or Polyon
        pnt_list = []
        for pnt in points:
            point = pnt.split()
            pnt_list.append((float(point[1]), float(point[0])))

        if pnt_list[0] == pnt_list[len(pnt_list)-1]:
            # First and last point are same -> Polygon
            geometry = geojson.Polygon([pnt_list])
        else:
            # First and last point not same -> LineString
            geometry = geojson.LineString(pnt_list)

    # set the default properties
    properties = {}

    # Add additional parameters added by the user
    if fields:
        for field in fields:
            properties.update({field: data.get(field)})
    else:
        properties.update(data)

    return geojson.Feature(geometry=geometry,
                           id=instance.pk,
                           properties=properties)


def is_polygon(point_list):
    """
    Takes a list of tuples and determines if it is a polygon
    """
    return (len(point_list) > 1 and
            point_list[0] == point_list[len(point_list)-1])


def geometry_from_string(points):
    """
    Takes a string, returns a geometry object
    """

    points = points.split(';')
    pnt_list = [tuple(map(float, reversed(point.split()[:2])))
                for point in points]

    if len(pnt_list) == 1:
        geometry = geojson.GeometryCollection(
            [geojson.Point(pnt_list[0])])
    elif is_polygon(pnt_list):
        # First and last point are same -> Polygon
        geometry = geojson.Polygon([pnt_list])
    else:
        # First and last point not same -> LineString
        geometry = geojson.LineString(pnt_list)

    return geometry