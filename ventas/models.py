from datetime import datetime
from django.contrib.gis.db import models
from jsonfield import JSONField


class RutaPrevendedor(models.Model):
    """
    Clase para distribucion de clientes para prevendedores
    """
    nombre = models.CharField(max_length=255, verbose_name='Nombre de Ruta')
    fecha_creado = models.DateField(default=datetime.now, auto_now=False, editable=False,
                                    verbose_name='Fecha de creacion')
    poligono = models.GeometryField(null=True, blank=True)
    ruta = models.LineStringField
    datos_filtro = JSONField('Datos para busqueda')

    objects = models.GeoManager()