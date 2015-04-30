from itertools import chain
import json

from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.contrib.gis.forms import widgets as giswidgets

__all__ = ('BaseGMapWidget',)


class BaseGMapWidget(giswidgets.BaseGeometryWidget):
    """A Google Maps base widget"""
    map_srid = 3857
    template_name = 'common/gis/google.html'

    class Media:
        js = (
            'http://openlayers.org/api/2.13/OpenLayers.js',
            'gis/js/OLMapWidget.js',
            'https://maps.google.com/maps/api/js?sensor=false',
        )


class SelectRelatedWithGeo(widgets.Select):
    """
    A different kind of select to choose related from a map
    """
    def __init__(self, *args, **kwargs):
        self.objects = []
        if kwargs and ("objects" in kwargs):
            self.objects = kwargs.pop("objects")
        super(SelectRelatedWithGeo, self).__init__(*args, **kwargs)

    @staticmethod
    def render_script(id):
        js_code = '''
                    <script type="text/javascript">
                        var myCenter=new google.maps.LatLng(53, -1.33);

                        function initialize(markers) {
                          var map;
                          var markerList = {};

                          var mapProp = {
                                mapTypeControl: true,
                                navigationControl: true,
                                streetViewControl: false,
                                scaleControl: false,
                                zoomControl: true,
                                panControl: false,
                                zoomControlOptions: {
                                  style: google.maps.ZoomControlStyle.SMALL
                                },
                                mapTypeId: google.maps.MapTypeId.ROADMAP,
                                zoom: 14
                          };

                          map = new google.maps.Map(document.getElementById("map-canvas_%s"), mapProp);
                          var bounds = new google.maps.LatLngBounds();

                          $.each(markers, function(i, item){
                            var object_pos = new google.maps.LatLng(item.lon, item.lat);
                            var marker = new google.maps.Marker({ id: item.id, map: map,
                                                                  title: item.title , position: object_pos,
                                                                  icon: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"});

                            markerList[marker.id] = marker;
                            google.maps.event.addListener(marker, 'click', function() {
                                console.log(marker.title);
                                if (marker.getAnimation() != null) {
                                   marker.setAnimation(null);
                                   marker.setIcon("http://maps.google.com/mapfiles/ms/icons/green-dot.png");
                                } else {
                                   marker.setAnimation(google.maps.Animation.BOUNCE);
                                   marker.setIcon("http://maps.google.com/mapfiles/ms/icons/red-dot.png");
                                }
                            });
                            bounds.extend(object_pos);
                            map.fitBounds(bounds);

                          });


                        };

                        $('#%s').on('shown.bs.modal', function(e) {
                            var element = $(e.relatedTarget);
                            var data = element.data("markers");
                            initialize(data);
                            google.maps.event.trigger(map, 'resize');
                        });
                    </script>
                  '''
        return js_code % (id, id)

    def render(self, name, value, attrs={}, choices=()):
        attrs['class'] = 'form-control hidden'
        if 'id' not in attrs:
            attrs['id'] = "id_%s" % name
        display = ugettext('None')
        for option_value, option_label in chain(self.choices, choices):
            if str(option_value) == (value):
                display = option_label
        tpl = '''
              <div class="input-group" id="%s_chooser">
                  <input type="text" class="form-control" placeholder="%s" value="%s" disabled>
                  <span class="input-group-btn" data-toggle="tooltip" title="%s">
                    <a class="btn btn-default" data-toggle="modal" data-target="#%s_map_modal" data-markers='%s'>
                        <span class="glyphicon glyphicon-map-marker"></span>
                    </a>
                  </span>
                  %s
              </div>

              <div class="modal fade" id="%s_map_modal">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-body">
                            <div class="container">
                                <div class="row">
                                    <div id="map-canvas_%s_map_modal" class="map-canvas"></div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-default" data-dismiss="modal">%s</button>
                            <button type="button" class="btn btn-primary">%s</button>
                        </div>
                    </div>
                </div>
                </div>
              '''
        render = tpl % (
            attrs['id'],
            ugettext('Select a point...'),
            display,
            ugettext('Click to choose...'),
            name,
            json.dumps(self.objects),
            super(SelectRelatedWithGeo, self).render(name, value, attrs, choices),
            name,
            name,
            ugettext('Cancel'),
            ugettext('Select')
        )
        return mark_safe("%s%s" % (render, self.render_script('%s_map_modal' % name)))
