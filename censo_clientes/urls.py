from django.conf.urls import patterns, include, url
from django_jinja import views
from django.views.generic import RedirectView

from django.contrib import admin
from django.conf import settings
from djgeojson.views import GeoJSONLayerView
from djgeojson.views import TiledGeoJSONLayerView
from base.site import SitePlus

from base.models import Area
from censo.models import Cliente


urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'base.default_views.not_built', name='index'),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^api/', include('api.urls')),

    url(r'^', include('sdauth.urls', namespace='auth')),
    url(r'^', include('censo.urls')),
    #url(r'^censo/mapa/$', 'censo.views.map_view', name='mapa'),
    url(r'^poligonos.geojson$', GeoJSONLayerView.as_view(model=Area, geometry_field = 'poligono', properties=(
            ['nombre', 'id', 'total_clientes']
        )),  name='poligonos_data'),
    url(r'^clientes.geojson$', GeoJSONLayerView.as_view(model=Cliente, geometry_field = 'coordenadas', properties=(
            ['popupContent', 'id',]
        )), name='clients_data'),
    url(r'^clientes/(\d+)/(\d+)/(\d+).geojson$',
        TiledGeoJSONLayerView.as_view(model=Cliente, geometry_field = 'coordenadas', properties=(
            ['popupContent', 'id',]
        )), name='tiled_clients_data'),
    url(r'^mobil/apk/$', 'censo.views.descargar_apk', name='apkdown'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = views.PermissionDenied.as_view()
handler404 = views.PageNotFound.as_view()
handler500 = views.ServerError.as_view()