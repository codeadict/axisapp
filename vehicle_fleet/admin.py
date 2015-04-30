from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from vehicle_fleet import models
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class VehiclesResource(resources.ModelResource):
    class Meta:
        model = models.Vehicles


class BrandsResource(resources.ModelResource):
    class Meta:
        model = models.Brands


class ModelResource(resources.ModelResource):
    class Meta:
        model = models.Model


class VehicleTypeResource(resources.ModelResource):
    class Meta:
        model = models.VehicleType


class ModelAdmin(ImportExportModelAdmin):
    resource_class = ModelResource
    list_display = ['name', 'brand',]


class VehicleTypeAdmin(ImportExportModelAdmin):
    resource_class = VehicleTypeResource
    list_display = ['name', ]


class BrandsAdmin(ImportExportModelAdmin):
    resource_class = BrandsResource
    list_display = ['name',]


class VehiclesAdmin(ImportExportModelAdmin):
    search_fields = ['plate_number', 'year']
    list_filter = ['plate_number', ]
    resource_class = VehiclesResource
    list_display = ['driver_name', 'plate_number', 'year']

# Register your models here.
admin.site.register(models.Vehicles, VehiclesAdmin)
admin.site.register(models.Model, ModelAdmin)
admin.site.register(models.Brands, BrandsAdmin)
admin.site.register(models.VehicleType, VehicleTypeAdmin)
