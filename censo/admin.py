from django.contrib.gis import admin
from django.contrib.admin import SimpleListFilter
from censo import models
from censo import forms
from base.models import Marca

from leaflet.admin import LeafletGeoAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class ProductosFilter(SimpleListFilter):
    title = 'Tiene Producto'
    parameter_name = 'producto'

    def lookups(self, request, model_admin):
        productos = set([c for c in Marca.objects.all()])
        return [(c.id, c.marca) for c in productos]

    def queryset(self, request, queryset):
        # if self.value():
        #     return queryset.filter(country__id__exact=self.value())
        # else:
        return queryset


class ClienteResource(resources.ModelResource):
    """
    Para Importar Datos
    """


    class Meta:
        model = models.Cliente
        exclude = ('ocasion_consumo', 'canal', 'subcanal', 'parroquia', 'canton' )


class ActivosInline(admin.TabularInline):
    model = models.ActivosMercado
    form = forms.ActivosForm
    suit_classes = 'suit-tab suit-tab-activo'

class VisitaInline(admin.TabularInline):
    model = models.Visita
    suit_classes = 'suit-tab suit-tab-visita'

class InventarioInline(admin.TabularInline):
    model = models.InvProductos
    form = forms.InvForm
    suit_classes = 'suit-tab suit-tab-inventario'


class ClientesAdmin(admin.GeoModelAdmin, ImportExportModelAdmin):
    """
    Interfaz para clientes
    """
    inlines = (ActivosInline, VisitaInline, InventarioInline,)
    readonly_fields = ('foto_local_admin', 'foto_cliente_admin',)
    search_fields = ['nombres', 'apellidos', 'identif', 'nombre_comercial']
    list_filter = [ProductosFilter, 'barrio', 'sector',]
    resource_class = ClienteResource
    list_display = ['nombres', 'apellidos', 'identif', 'direccion', 'nombre_comercial']
    suit_form_tabs = (('cliente', 'Datos Cliente'), ('local', 'Datos Local'), ('localizacion', 'Localizacion'), ('activo', 'Activos Mercado'), ('visita', 'Visitas'), ('inventario', 'Cat. Productos'), ('foto_local', 'Foto'))
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-cliente',),
            'fields': ['nombres', 'apellidos', 'tipo_id', 'identif', 'email', 'celular', 'convencional', 'cumple', 'administrador',]
        }),
        ('Foto', {
            'classes': ('suit-tab', 'suit-tab-cliente',),
            'fields': ['foto_cliente_admin', 'foto']}),
        (None, {
            'classes': ('suit-tab', 'suit-tab-local',),
            'fields': ['direccion', 'tipo_local', 'especial', 'estatal', 'persona_compras', 'razon_social', 'nombre_comercial', 'website', 'macro_canal', 'ocasion_consumo', 'canal', 'subcanal', 'medida_frente', 'medida_fondo', 'horario_desde', 'horario_hasta', 'abc_compras', 'abc_industrias',]}),
        (None, {
            'classes': ('suit-tab', 'suit-tab-localizacion',),
            'fields': ['fecha_ingreso', 'fecha_retiro', 'codigo', 'estado']}),
        ('Ubicacion del Local', {
            'classes': ('suit-tab', 'suit-tab-localizacion',),
            'fields': ['barrio', 'sector', 'coordenadas',]}),
        (None, {
            'classes': ('suit-tab', 'suit-tab-foto_local',),
            'fields': ['foto_local_admin', 'foto_local', ]}),
    ]


admin.site.register(models.Cliente, ClientesAdmin)


