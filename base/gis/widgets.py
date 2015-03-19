from django.contrib.gis.forms import widgets

__all__ = ('BaseGMapWidget',)


class BaseGMapWidget(widgets.BaseGeometryWidget):
    """A Google Maps base widget"""
    map_srid = 3857
    template_name = 'common/gis/google.html'

    class Media:
        js = (
            'http://openlayers.org/api/2.13/OpenLayers.js',
            'gis/js/OLMapWidget.js',
            'https://maps.google.com/maps/api/js?sensor=false',
        )
