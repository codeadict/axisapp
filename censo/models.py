from datetime import date
import requests
import bs4

from django.conf import settings
from django.contrib.gis.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey

from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType

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
    #Que el link de la APK aparezca solo un dia y se cambie el slug
    nombres = models.CharField(max_length=255, verbose_name='Nombres')
    apellidos = models.CharField(max_length=255, verbose_name='Apellidos')
    tipo_id = models.PositiveIntegerField(choices=TIPOS_IDS, default=0, verbose_name='Tipo ID')
    identif = models.CharField(max_length=16, verbose_name='Identificacion')
    fecha_verificado_sri = models.DateField(verbose_name='Fecha Verificacion SRi', null=True, blank=True)
    email = models.EmailField(max_length=150, verbose_name='Email', null=True, blank=True)
    celular = models.CharField(max_length=10, verbose_name='Celular', null=True, blank=True)
    convencional = models.CharField(max_length=9, verbose_name='Convencional', null=True, blank=True,
                                    help_text='Poner con 9 numeros, Ejemplo: 021234567')
    cumple = models.DateField(verbose_name='Cumpleanos', null=True, blank=True)
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
    horario_desde = models.TimeField(verbose_name='Horario Desde', help_text='Formato 24 horas: 00:00')
    horario_hasta = models.TimeField(verbose_name='Horario Hasta', help_text='Formato 24 horas: 00:00')
    abc_compras = models.CharField(max_length=1, choices=ABC, verbose_name='ABC Compras', null=True, blank=True)
    abc_industrias = models.CharField(max_length=1, choices=ABC, verbose_name='ABC Industrias', null=True, blank=True)

    #Datos Localizacion
    fecha_ingreso = models.DateField('Fecha Ingreso', null=True, blank=True)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Registrado Por'), null=True, blank=True)
    fecha_retiro = models.DateField('Fecha Retiro', null=True, blank=True)
    #area = models.ForeignKey(modelos_maestros.Area, verbose_name='Area o Poligono')
    codigo = models.CharField(max_length=20, verbose_name='Codigo', null=True, blank=True)
    barrio = models.CharField(max_length=255, verbose_name='Barrio', blank=True, null=True)
    sector = models.CharField(max_length=255, verbose_name='Sector', blank=True, null=True)

    estado = models.PositiveSmallIntegerField(choices=ESTADOS, verbose_name='Estado', default=ACTIVO)
    #TODO: Foto Local obligatoria en la app movil
    foto_local = models.ImageField(upload_to='fotos/locales/', null=True,
                                   blank=True, verbose_name=u'Foto del Local')
    coordenadas = models.PointField(db_column="geom", null=True, blank=True)

    objects = models.GeoManager()

    class Meta:
        ordering = ['nombres']

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return self.get_full_name()

    @models.permalink
    def get_absolute_url(self):
        return ('client-details', [self.pk])

    def get_full_name(self):
        if "'" in self.nombres:
            return ugettext('Names not present on DataBase')
        return '%s %s' % (self.nombres, self.apellidos)

    def get_identif(self):
        if "'" in self.identif:
            return ugettext('Identification not present on DataBase')
        return '%s' % (self.identif)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

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

    def verify(self):
        """
        Verify the client with government institutions to check that data is updated and correct
        """
        verification_data = {}
        if self.tipo_id == self.RUC:
            params = {'accion': 'siguiente', 'ruc': self.identif, 'lineasPagina': ''}
            url = 'https://declaraciones.sri.gob.ec/facturacion-internet/consultas/publico/ruc-datos2.jspa'
            sri_page = requests.post(url, params)
            soup = bs4.BeautifulSoup(sri_page.text)
            form = soup.select('table.formulario')
            data = soup.select('table.formulario tr td')
            resp = str(form[0]) if form else ''

            if data:
                verification_data = {
                    'response': resp.decode('utf-8'),
                    'social_reason': data[0].text.strip(' \n\s'),
                    'identification': data[2].text.strip(' \n\s'),
                    'contributor_type': data[11].text.strip(' \n\s'),
                    'accounting_obligation': True if data[13].text == 'SI' else False,
                }
        return verification_data

    def save(self, *args, **kwargs):
        """
        Generar Codigo Automatico, autogenerar fechas y guardar mayusculas
        """
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

        if not self.administrador:
            setattr(self, 'administrador', self.apellidos + ' ' + self.nombres)

        # Find localization toponyms based on coordinates
        if self.coordenadas:
            province = modelos_maestros.Provincia.objects.filter(geom__contains=self.coordenadas)
            canton = modelos_maestros.Canton.objects.filter(geom__contains=self.coordenadas)
            parish = modelos_maestros.Parroquia.objects.filter(geom__contains=self.coordenadas )

        #obtener todos los campos Char sin choices para poner en mayusculas, DRY
        char_fields = [f.name for f in self._meta.fields if isinstance(f, models.CharField) and not isinstance(f, models.EmailField) and not isinstance(f, models.URLField) and not getattr(f, 'choices')]
        for f in char_fields:
            val = getattr(self, f, False)
            if val and isinstance(val, basestring):
                setattr(self, f, val.upper())
        super(Cliente, self).save(*args, **kwargs)


class ActivosMercado(models.Model):
    """
    Modelos de mercado
    """
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente', related_name='market_assets')
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
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente', related_name='visits')
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
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente', related_name='products')
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
    presentacion = models.PositiveIntegerField(verbose_name='Presentacion(ML)')
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
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    WEEKDAYS = (
        (MONDAY, _('Monday')),
        (TUESDAY, _('Tuesday')),
        (WEDNESDAY, _('Wednesday')),
        (THURSDAY, _('Thursday')),
        (FRIDAY, _('Friday')),
        (SATURDAY, _('Saturday')),
        (SUNDAY, _('Sunday')),
    )

    PRESALE = 0
    AUTOSALE = 1
    TELESALE = 2

    ROUTE_TYPES = (
        (PRESALE, _('Pre Sale')),
        (AUTOSALE, _('Auto Sale')),
        (TELESALE, _('Tele Sale'))
    )

    name = models.CharField(max_length=255, verbose_name=_('Polygon Name'), null=True, blank=True)
    clients = models.ManyToManyField(Cliente, verbose_name=_('Clients'), related_name='distributions', blank=True)
    polygon = models.PolygonField(verbose_name=_('Polygon'))
    frequency = models.CommaSeparatedIntegerField(_('Visit Days'), max_length=32, null=True, blank=True)
    route_type = models.PositiveSmallIntegerField(_('Route Type'), choices=ROUTE_TYPES, null=True, blank=True)
    assigned_seller = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Assigned Pre-seller',
                                        related_name='areas_preseller', null=True, blank=False)
    initial_client = models.ForeignKey(Cliente, null=True, blank=True, related_name='presales_initial',
                                       help_text=_('Select the initial client from where you will start selling'))
    final_client = models.ForeignKey(Cliente, null=True, blank=True, related_name='presales_final',
                                     help_text=_('Select the final client from where you will finish selling'))
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Distribution Area')
        verbose_name_plural = _('Distribution Areas')

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return ''

    @property
    def clients_count(self):
        """
        Rerurns the ammount of clients per polygon
        :return: integer
        """
        pass