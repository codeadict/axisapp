from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from base import models

from import_export.admin import ImportExportModelAdmin
from import_export import resources


class PresentacionesResource(resources.ModelResource):
    """
    Para Importar Datos
    """
    class Meta:
        model = models.Presentacion

class MarcasResource(resources.ModelResource):
    """
    Para Importar Datos
    """
    class Meta:
        model = models.Marca

class ProvinciasResource(resources.ModelResource):
    """
    Para Importar Datos
    """
    class Meta:
        model = models.Provincia

class CantonResource(resources.ModelResource):
    """
    Para Importar Datos
    """
    class Meta:
        model = models.Canton

class ParroquiaIE(resources.ModelResource):
    """
    Para Importar Datos
    """
    class Meta:
        model = models.Parroquia

class EmpresaActivosIE(resources.ModelResource):
    """
    Para Importar Datos
    """
    class Meta:
        model = models.EmpresaActivos

class EmpresaVisitasIE(resources.ModelResource):
    """
    Para Importar Datos
    """
    class Meta:
        model = models.EmpresaVisitas

class ProvinciaAdmin(ImportExportModelAdmin):
    resource_class = ProvinciasResource
    list_display = ['nombre']

class CantonAdmin(ImportExportModelAdmin):
    resource_class = CantonResource
    list_display = ['nombre']

class ParroquiaAdmin(ImportExportModelAdmin):
    resource_class = ParroquiaIE
    list_display = ['nombre']

class AreaAdmin(admin.GeoModelAdmin):
    search_fields = ['nombre']
    list_display = ['nombre', 'provincia', 'canton', 'parroquia']
    default_zoom = 7
    actions = ['generar_ruta']

    def generar_ruta(self, request, queryset):
        pass
    generar_ruta.short_description = "Generar Rutas"


class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'colour']

class MacroCanalAdmin(ImportExportModelAdmin):
    list_display = ['nombre']

class OcasionConsumoAdmin(ImportExportModelAdmin):
    list_display = ['nombre']

class CanalAdmin(ImportExportModelAdmin):
    list_display = ['nombre']

class SubCanal(ImportExportModelAdmin):
    list_display = ['nombre']

class MacroCatAdmin(ImportExportModelAdmin):
    list_display = ['nombre']

class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['nombre']

class MarcaAdmin(ImportExportModelAdmin):
    resource_class = MarcasResource
    list_display = ['marca']
    search_fields = ['marca']
    list_filter = ['categoria']

class PresentacionAdmin(ImportExportModelAdmin):
    resource_class = PresentacionesResource
    list_display = ['nombre']

class EnvaseAdmin(ImportExportModelAdmin):
    list_display = ['nombre']


class EmpresaActivosAdmin(ImportExportModelAdmin):
    resource_class = EmpresaActivosIE
    list_display = ['nombre']


class EmpresaVisitasAdmin(ImportExportModelAdmin):
    resource_class = EmpresaVisitasIE
    list_display = ['nombre']


admin.site.register(models.Provincia, ProvinciaAdmin)
admin.site.register(models.Canton, CantonAdmin)
admin.site.register(models.Parroquia, ParroquiaAdmin)

admin.site.register(models.Area, AreaAdmin)

admin.site.register(models.MacroCanal, MacroCanalAdmin)
admin.site.register(models.OcasionConsumo, OcasionConsumoAdmin)
admin.site.register(models.Canal, CanalAdmin)
admin.site.register(models.SubCanal, SubCanal)
admin.site.register(models.MacroCat, MacroCatAdmin)
admin.site.register(models.Categoria, CategoriaAdmin)
admin.site.register(models.Marca, MarcaAdmin)
admin.site.register(models.Presentacion, PresentacionAdmin)
admin.site.register(models.Envase, EnvaseAdmin)
admin.site.register(models.EmpresaActivos, EmpresaActivosAdmin)
admin.site.register(models.EmpresaVisitas, EmpresaVisitasAdmin)
admin.site.register(models.Label, LabelAdmin)
