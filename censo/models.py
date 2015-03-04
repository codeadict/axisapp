from datetime import date
import requests
import bs4

from django.conf import settings
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey

from base import models as modelos_maestros


class Cliente(modelos_maestros.Partner):
    """
    Tabla de Clientes
    """
    CEDULA = 0
    RUC = 1
    PASAPORTE = 2

    PROPIO = 0
    ARRENDADO = 1
    COMODATO = 2

    A = 'a'
    B = 'b'
    C = 'c'

    ACTIVO = 0
    PASIVO = 1
    ELIMINADO = 2

    TIPOS_IDS = (
        (CEDULA, 'CEDULA'),
        (RUC, 'RUC'),
        (PASAPORTE, 'PASAPORTE'),
    )

    TIPOS_LOCAL = (
        (PROPIO, 'ARRENDADO'),
        (ARRENDADO, 'PROPIO'),
        (COMODATO, 'COMODATO'),
    )

    ABC = (
        (A, 'A'),
        (B, 'B'),
        (C, 'C'),
    )

    ESTADOS = (
        (ACTIVO, 'ACTIVO'),
        (PASIVO, 'PASIVO'),
        (ELIMINADO, 'ELIMINADO'),
    )
    # Datos del Cliente
    #TODO: en filtros poner uno por categoria de productos, ejemplo solo los que compran licores
    #TODO: Minimo un record en productos y visitas
    #TODO: En las fechas poner un input mask DD/MM/AAAA y que no salga hoy ni lance el calendar
    #Que el link de la APK aparezca solo un dia y se cambie el slug
    nombres = models.CharField(max_length=255, verbose_name='Nombres')
    apellidos = models.CharField(max_length=255, verbose_name='Apellidos')
    tipo_id = models.PositiveIntegerField(choices=TIPOS_IDS, default=0, verbose_name='Tipo ID')
    identif = models.CharField(max_length=13, verbose_name='Identificacion')
    fecha_verificado_sri = models.DateField(verbose_name='Fecha Verificacion SRi', null=True, blank=True)
    email = models.EmailField(max_length=150, verbose_name='Email', null=True, blank=True)
    celular = models.CharField(max_length=10, verbose_name='Celular', null=True, blank=True)
    convencional = models.CharField(max_length=9, verbose_name='Convencional', null=True, blank=True,
                                    help_text='Poner con 9 numeros, Ejemplo: 021234567')
    cumple = models.DateField(verbose_name='Cumpleanos')
    administrador = models.CharField(max_length=255, verbose_name='Administrador', null=True, blank=True)
    foto = models.ImageField(upload_to='fotos/clientes/', null=True,
                             blank=True, verbose_name=u'Foto')

    #Datos del Local
    direccion = models.CharField(max_length=255, blank=True, null=True,
                                 verbose_name='Direccion Local')
    tipo_local = models.PositiveIntegerField(choices=TIPOS_LOCAL, default=0, verbose_name='Local')
    especial = models.BooleanField(verbose_name='Contribuyente Especial', blank=True, default=False)
    estatal = models.BooleanField(verbose_name='Institucion Estado', blank=True, default=False)
    persona_compras = models.CharField(max_length=255, verbose_name='Persona aut. a comprar', null=True, blank=True)
    razon_social = models.CharField(max_length=255, verbose_name='Razon Social', null=True, blank=True)
    nombre_comercial = models.CharField(max_length=255, verbose_name='Nombre Comercial', null=True, blank=True)
    website = models.URLField(verbose_name=u'Pagina Web', max_length=255, blank=True, null=True)

    macro_canal = models.ForeignKey(modelos_maestros.MacroCanal, verbose_name='Macro Canal', blank=True, null=True)
    ocasion_consumo = ChainedForeignKey(modelos_maestros.OcasionConsumo, chained_field="macro_canal",
                                        chained_model_field="macrocanal", blank=True, null=True)
    canal = ChainedForeignKey(modelos_maestros.Canal, chained_field="ocasion_consumo",
                              chained_model_field="ocasion", blank=True, null=True)
    subcanal = ChainedForeignKey(modelos_maestros.SubCanal, chained_field="canal",
                                 chained_model_field="canal", blank=True, null=True)

    medida_frente = models.FloatField(verbose_name='Medida Frente', blank=True, null=True)
    medida_fondo = models.FloatField(verbose_name='Medida Fondo', blank=True, null=True)
    #TODO: Poner horas en formato 24 horas y poner help_text que diga al usuario el formato
    horario_desde = models.TimeField(verbose_name='Desde', help_text='Formato 24 horas: 00:00')
    horario_hasta = models.TimeField(verbose_name='Hasta', help_text='Formato 24 horas: 00:00')
    abc_compras = models.CharField(max_length=1, choices=ABC, verbose_name='ABC Compras', null=True, blank=True)
    abc_industrias = models.CharField(max_length=1, choices=ABC, verbose_name='ABC Industrias', null=True, blank=True)

    #Datos Localizacion
    fecha_ingreso = models.DateField('Fecha Ingreso', null=True, blank=True)
    fecha_retiro = models.DateField('Fecha Retiro', null=True, blank=True)
    #area = models.ForeignKey(modelos_maestros.Area, verbose_name='Area o Poligono')
    codigo = models.CharField(max_length=20, verbose_name='Codigo', null=True, blank=True)
    barrio = models.CharField(max_length=255, verbose_name='Barrio', blank=True, null=True)
    sector = models.CharField(max_length=255, verbose_name='Sector', blank=True, null=True)
    coordenadas = models.PointField(db_column="geom")

    frecuencia = models.CharField(max_length=20, verbose_name='Frecuencia', null=True, blank=True)
    secuencia = models.CharField(max_length=20, verbose_name='Secuencia', null=True, blank=True)
    estado = models.PositiveSmallIntegerField(choices=ESTADOS, verbose_name='Estado', default=ACTIVO)

    #TODO: Foto Local obligatoria en la app movil
    foto_local = models.ImageField(upload_to='fotos/locales/', null=True,
                                   blank=True, verbose_name=u'Foto del Local')

    objects = models.GeoManager()

    def __unicode__(self):
        """
        Representacion del Objeto
        :return: Unicode String
        """
        return self.get_full_name()

    def get_full_name(self):
        return '%s %s' % (self.nombres, self.apellidos)

    def foto_cliente_admin(self):
        if self.foto:
            return '<img src="/media/%s" height="200" with="200" style="height: 200px !important;"/>' % self.foto
        return '<img src="http://placehold.it/200x200&text=Sin Foto del Cliente" height="200" with="200"/>'

    foto_cliente_admin.allow_tags = True
    foto_cliente_admin.short_description = 'Foto del Cliente'

    def foto_local_admin(self):
        if self.foto_local:
            return '<img src="/media/%s" height="400" with="400" style="height: 400px !important;"/>' % self.foto_local
        return '<img src="http://placehold.it/400x400&text=Sin Foto del Local" height="400" with="400"/>'

    foto_local_admin.allow_tags = True
    foto_local_admin.short_description = 'Foto del Local'

    @property
    def popupContent(self):
        return '<img src="{}" height="50" with="50" style="height: 50px !important;"/><p><b>Nombre y Apellidos:</b> {}</p><p><b>Identificacion:</b> {}</p><p><b>Nombre Comercial:</b> {}</p><p style="text-align:right;"><a href="/censo/cliente/{}/">Ver mas Detalles</a></p>'.format(
            self.foto_local.url if self.foto_local else 'http://lorempixel.com/g/100/100/food/',
            self.nombres.encode('ascii', 'ignore').decode(
                'ascii') if self.nombres else 'Sin Nombre' + ' ' + self.apellidos.encode('ascii', 'ignore').decode(
                'ascii') if self.apellidos else ' ', self.identif if self.identif else ' ',
            self.nombre_comercial.encode('ascii', 'ignore').decode('ascii') if self.nombre_comercial else ' ', self.id)

    def verificar_sri(self):
        if self.tipo_id == self.RUC:
            params = {'accion': 'siguiente', 'ruc': self.identif, 'lineasPagina': ''}
            url = 'https://declaraciones.sri.gob.ec/facturacion-internet/consultas/publico/ruc-datos2.jspa'
            sri_page = requests.post(url, params)
            soup = bs4.BeautifulSoup(sri_page.text)

            data = soup.select('table.formulario tr td')

            if not data:
                return
            else:
                self.razon_social = data[0].text.strip(' \n\s')
                self.identif = data[2].text.strip(' \n\s')
                self.tipo_contribuyente = data[11].text.strip(' \n\s')
                self.lleva_contabilidad = True if data[13].text == 'SI' else False

    def save(self, *args, **kwargs):
        """
        Generar Codigo Automatico, autogenerar fechas y guardar mayusculas
        """
        #codigo_prov = self.area.provincia.codigo
        top = Cliente.objects.count()
        #self.codigo = codigo_prov + str(1000 + top + 1)
        if not self.id:
            self.fecha_ingreso = date.today()
        if self.estado and self.estado in [self.PASIVO, self.ELIMINADO]:
            self.fecha_retiro = date.today()

        if not self.persona_compras:
            setattr(self, 'persona_compras', self.apellidos + ' ' + self.nombres)

        if not self.razon_social:
            setattr(self, 'razon_social', self.apellidos + ' ' + self.nombres)

        if not self.nombre_comercial:
            setattr(self, 'nombre_comercial', self.apellidos + ' ' + self.nombres)

        #TODO: Regenerar el administrador para que no sea requerido
        if not self.administrador:
            setattr(self, 'administrador', self.apellidos + ' ' + self.nombres)

        #obtener todos los campos Char sin choices para poner en mayusculas, DRY
        char_fields = [f.name for f in self._meta.fields if
                       isinstance(f, models.CharField) and not getattr(f, 'choices')]
        for f in char_fields:
            val = getattr(self, f, False)
            if val:
                setattr(self, f, val.upper())
        super(Cliente, self).save(*args, **kwargs)


class ActivosMercado(models.Model):
    """
    Modelos de mercado
    """
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente')
    empresa = models.ForeignKey(modelos_maestros.EmpresaActivos, verbose_name='Competencia')
    p = models.PositiveIntegerField('P')
    m = models.PositiveIntegerField('M')
    g = models.PositiveIntegerField('G')
    congelador = models.BooleanField('Cong.', default=False)
    exhibidor = models.BooleanField('Exhib.', default=False)
    estante = models.BooleanField('Estan.', default=False)
    rotulo = models.BooleanField('Rotu.', default=False)
    mesas = models.BooleanField('Mesas', default=False)
    sillas = models.BooleanField('Sillas', default=False)

    class Meta:
        verbose_name = 'Activo de Mercado'
        verbose_name_plural = 'Activos de Mercado'

    def __unicode__(self):
        return '%s - %s' % (self.cliente.nombres + ' ' + self.cliente.apellidos, self.empresa.nombre)


class Visita(models.Model):
    """
    Visita Clientes
    """
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente', default=0)
    empresa = models.ForeignKey(modelos_maestros.EmpresaVisitas, verbose_name='Competencia')
    lunes = models.BooleanField('Lun', default=False)
    martes = models.BooleanField('Mar', default=False)
    miercoles = models.BooleanField('Mie', default=False)
    jueves = models.BooleanField('Jue', default=False)
    viernes = models.BooleanField('Vie', default=False)
    sabado = models.BooleanField('Sab', default=False)
    domingo = models.BooleanField('Dom', default=False)
    preventa = models.BooleanField('Preventa', default=False)
    autoventa = models.BooleanField('Autoventa', default=False)
    televenta = models.BooleanField('Televenta', default=False)


    class Meta:
        verbose_name = 'Visita del Cliente'
        verbose_name_plural = 'Visitas del Cliente'

    def __unicode__(self):
        return '%s - %s' % (self.cliente.nombres + ' ' + self.cliente.apellidos, self.empresa.nombre)


class InvProductos(models.Model):
    """
    Inventario de Productos
    """
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente')
    macro_categ = models.ForeignKey(modelos_maestros.MacroCat, verbose_name='Macro Cat.')
    categ = ChainedForeignKey(
        modelos_maestros.Categoria,
        verbose_name='Categorizacion',
        chained_field="macro_categ",
        chained_model_field="macro",
        show_all=False, auto_choose=True
    )
    marca = ChainedForeignKey(
        modelos_maestros.Marca,
        verbose_name='Marca',
        chained_field="categ",
        chained_model_field="categoria",
        show_all=False, auto_choose=True
    )
    presentacion = models.ForeignKey(modelos_maestros.Presentacion, verbose_name='Presentacion')
    envase = models.ForeignKey(modelos_maestros.Envase, verbose_name='Envase')

    class Meta:
        verbose_name = 'Inventario Producto'
        verbose_name_plural = 'Inventario Productos'

    def __unicode__(self):
        return '%s - %s' % (self.cliente.nombres + ' ' + self.cliente.apellidos, self.marca.marca)


class PresalesDistribution(models.Model):
    """
    Distribution of clients for pre-sales.
    We need to separate an area on clusters containing N clients, each cluster will be stored on this table
    with the required data:
        name: the generated polygon name that can be e.g QP001, Q for Quito, P for Preventa, and consecutive number
        clients: foreign key 1 to Clients referencing all the points generated on kmeans.
        polygon: postgis polygon field that encloses all the points(clients) inside it using ConvexHull.
        assigned_seller: the seller assigned to work on this polygon, nullable, by default it takes seller on Area.
    """
    name = models.CharField(max_length=255, verbose_name=_('Polygon Name'), null=True, blank=True)
    clients = models.ManyToManyField(Cliente, verbose_name=_('Clients'), related_name='distributions', blank=True)
    polygon = models.PolygonField(verbose_name=_('Polygon'))
    assigned_seller = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Assigned Pre-seller',
                                        related_name='areas_preseller', null=True, blank=False)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Distribution Area')
        verbose_name_plural = _('Distribution Areas')

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return ''