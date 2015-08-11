from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django.contrib.gis.db import models as gismodel
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey

from base.querysets import BaseRequestQueryset
from base import fields

# TODO: and providers and employers and sellers
PARTNER_TYPES = models.Q(app_label='censo', model='cliente')


class NombreMayusculasModel(models.Model):
    """
    Modelo abstracto que retorna el nombre en mayusculas
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        nombre = getattr(self, 'nombre', False)
        if nombre:
            setattr(self, 'nombre', nombre.upper())
        super(NombreMayusculasModel, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(getattr(self, 'nombre').upper())


class LabelQueryset(BaseRequestQueryset):
    def available_for_obj(self, obj):
        return self.filter(applicable_partner_types__model=obj.partner_type.lower())


class Label(models.Model):
    """
    A label to tag an object
    """
    objects = LabelQueryset.as_manager()
    name = models.CharField(verbose_name=_('Nombre'), max_length=100)
    colour = fields.ColorField(_('Color'), max_length=20, default='#ADF')
    partners = models.ManyToManyField('Partner', verbose_name=_('Asociados'), related_name='labels', blank=True)
    applicable_partner_types = models.ManyToManyField(ContentType, verbose_name=_('Aplicable a'),
                                                   related_name='labels', limit_choices_to=PARTNER_TYPES)

    class Meta:
        verbose_name = _('Etiqueta')
        verbose_name_plural = _('Etiquetas')
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Partner(models.Model):

    # These flags are being used in Partner selection dropdown
    is_current = True  # This is currently selected role

    partner_type = models.CharField(_('Tipo de Asociado'), max_length=20, editable=False, db_index=True)
    priority = models.PositiveSmallIntegerField(_('Orden de Prioridad'), default=0, editable=False, db_index=True)

    partner_type_name = property(lambda self: self.partner_model())

    class Meta:
        ordering = ['-priority']

    def save(self, *args, **kw):
        if not self.partner_type:
            self.partner_type = self.__class__.__name__
        if not self.priority:
            self.priority = self.get_priority()
        return super(Partner, self).save(*args, **kw)

    def get_priority(self):
        priorities = {
            'Cliente': 10,
            'Proveedor': 20,
            'Employee': 30,
        }
        return priorities[self.partner_type]

    @property
    def partner_type_verbose_name(self):
        return self.partner_obj()._meta.verbose_name

    def partner_model(self):
        return self.partner_type

    def partner_obj(self):
        return getattr(self, self.partner_type.lower())

    @staticmethod
    def get_instance_sys_partner_name(instance=None, model=None):
        if instance:
            # works on partner as well as inheritors.
            partner_name = instance.partner_type.lower()
        else:
            partner_name = model.__name__.lower()
        if partner_name == 'cliente':
            partner_name = 'cliente'
        return partner_name

    def get_sys_partner_name(self):
        return self.get_instance_sys_partner_name(self)

    @staticmethod
    def get_instance_url(instance=None, instance_pk=None, model=None):
        """
        Get absolute url of a role instance eg. Either instance or instance_pk
        must be specified. Instance must be specified if it's a Role

        :param instance: Role, Cliente, Proveedor, Empleado
        :param instance_pk: pk of role, ignored if instance is supplies unless instance is unsaved.
        :param model: the model class, only used with instance_pk
        :return: url
        """
        assert instance or (instance_pk and model), 'Either instance or instance_pk and model must be specified.'
        if instance:
            instance_pk = instance.pk or instance_pk
        role_name = Partner.get_instance_sys_partner_name(instance, model)
        if role_name == 'cliente':
            role_name = 'client'
        return reverse(u'%s-details' % role_name, kwargs={'pk': instance_pk})

    def get_absolute_url(self):
        return self.get_instance_url(self)

    def get_labels(self):
        return Label.objects.filter(partners=self)

    def is_client(self):
        return self.partner_type == 'Cliente'

    def _get_partner_id(self):
        # make sure we always use the role id even if this method is called on child instances.
        return getattr(self, 'partner_ptr_id', self.id)

class Provincia(gismodel.Model):
    codigo = gismodel.CharField(max_length=10, verbose_name='Codigo de Provincia', unique=True)
    nombre = gismodel.CharField(max_length=45, verbose_name='Nombre de la Provincia')
    geom = gismodel.MultiPolygonField(null=True) # we want our model in a different SRID

    objects = gismodel.GeoManager()


    def __unicode__(self):
        return self.nombre


class Canton(gismodel.Model):
    provincia = gismodel.ForeignKey(Provincia, to_field='codigo')
    codigo = gismodel.CharField(max_length=10, verbose_name='Codigo del Canton', default='', unique=True, db_index=True)
    nombre = gismodel.CharField(max_length=45, verbose_name='Nombre del Canton')
    geom = gismodel.MultiPolygonField(null=True)

    objects = gismodel.GeoManager()

    class Meta:
        verbose_name_plural = 'Cantones'


    def __unicode__(self):
        return self.nombre


class Parroquia(gismodel.Model):
    canton = gismodel.ForeignKey(Canton, to_field='codigo')
    codigo = gismodel.CharField(max_length=10, verbose_name='Codigo de la Parroquia', default='', unique=True, db_index=True)
    nombre = models.CharField(max_length=255, verbose_name='Nombre de la Parroquia')
    geom = gismodel.MultiPolygonField(null=True)

    objects = gismodel.GeoManager()

    def __unicode__(self):
        return unicode(self.nombre)


class Area(NombreMayusculasModel):
    """
    Modelo de Areas o regiones a censar
    """
    #TODO: poner fechas y horas que solo se pueden modificar los datos.
    nombre = gismodel.CharField(max_length=255, verbose_name='Nombre del poligono', null=False, blank=False)
    agencia = models.CharField(max_length=20, verbose_name='Agencia', null=True, blank=True)
    tipo_ruta = models.CharField(max_length=20, verbose_name='Tipo Ruta', null=True, blank=True)
    ruta = models.CharField(max_length=20, verbose_name='Ruta', null=True, blank=True)
    poligono = gismodel.PolygonField()
    censador = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Censador Asignado', related_name='areas_censador', null=True,
                                 blank=False)
    prevendedor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Prevendedor Asignado', related_name='areas_prevendedor',
                                    null=True, blank=False)

    objects = gismodel.GeoManager()

    def __unicode__(self):
        return self.nombre

    @property
    def total_clientes(self):
        total = self.cliente_set.all().count()
        return total


class MacroCanal(NombreMayusculasModel):
    """
    Tabla de MacroCanales
    """
    nombre = models.CharField(max_length=150, verbose_name='Macro Canal')

    class Meta:
        verbose_name = 'Macro Canal'
        verbose_name_plural = 'Macro Canales'

    def __unicode__(self):
        return self.nombre


class OcasionConsumo(NombreMayusculasModel):
    """
    Ocasiones de Consumo
    """
    macrocanal = models.ForeignKey(MacroCanal)
    nombre = models.CharField(max_length=100, verbose_name='Ocasion de Consumo')


    class Meta:
        verbose_name = 'Ocasion de Consumo'
        verbose_name_plural = 'Ocasiones de Consumo'

    def __unicode__(self):
        return self.nombre


class Canal(NombreMayusculasModel):
    """
    Tabla de Canales
    """
    ocasion = models.ForeignKey(OcasionConsumo, verbose_name='Ocacion de Consumo')
    nombre = models.CharField(max_length=100, verbose_name='Canal')

    class Meta:
        verbose_name = 'Canal'
        verbose_name_plural = 'Canales'

    def __unicode__(self):
        return self.nombre


class SubCanal(NombreMayusculasModel):
    """
    Sub Canales
    """
    canal = models.ForeignKey(Canal, verbose_name='Canal')
    nombre = models.CharField(max_length=255, verbose_name='Sub Canal')

    class Meta:
        verbose_name = 'SubCanal'
        verbose_name_plural = 'SubCanales'

    def __unicode__(self):
        return self.nombre


# Productos

class MacroCat(NombreMayusculasModel):
    """
    Macro Categorizacion
    """
    nombre = models.CharField(max_length=150, verbose_name='Macro Categoria')

    class Meta:
        verbose_name = 'Macro Categoria'
        verbose_name_plural = 'Macro Categorias'

    def __unicode__(self):
        return self.nombre


class Categoria(NombreMayusculasModel):
    """
    Categorias de Productos
    """
    macro = models.ForeignKey(MacroCat, verbose_name='Macro Categorizacion')
    nombre = models.CharField(max_length=255, verbose_name='Categorizacion')

    def __unicode__(self):
        return self.nombre


class Marca(models.Model):
    """
    Marcas de Productos
    """
    categoria = models.ForeignKey(Categoria, verbose_name='Categorizacion')
    marca = models.CharField(max_length=255, verbose_name='Marca')

    def __unicode__(self):
        return self.marca

    def save(self, *args, **kwargs):
        marca = getattr(self, 'marca', False)
        if marca:
            setattr(self, 'marca', marca.upper())
        super(Marca, self).save(*args, **kwargs)


class Presentacion(NombreMayusculasModel):
    marca = models.ForeignKey(Marca, verbose_name='Marca', null=True)
    nombre = models.CharField(max_length=100, verbose_name='Presentacion')

    class Meta:
        verbose_name = 'Presentacion'
        verbose_name_plural = 'Presentaciones'

    def __unicode__(self):
        return self.nombre


class Envase(NombreMayusculasModel):
    """
    Tipos de Envase
    """
    nombre = models.CharField(max_length=255, verbose_name='Tipo de Envase')

    def __unicode__(self):
        return self.nombre


class EmpresaActivos(NombreMayusculasModel):
    """
    Empresas Activos de Mercado
    """
    nombre = models.CharField(max_length=255, verbose_name='Nombre Empresa')

    class Meta:
        verbose_name = 'Empresa Activos de Mercado'
        verbose_name_plural = 'Empresas Activos de Mercado'

    def __unicode__(self):
        return self.nombre


class EmpresaVisitas(NombreMayusculasModel):
    """
    Empresas Visitas Cliente
    """
    nombre = models.CharField(max_length=255, verbose_name='Nombre Empresa')

    class Meta:
        verbose_name = 'Empresa Visita Cliente'
        verbose_name_plural = 'Empresas Visitas Clientes'

    def __unicode__(self):
        return self.nombre
