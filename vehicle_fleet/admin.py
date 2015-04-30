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
    list_display = ['name', ]
    fieldsets = [
        (_('Vehicle'), {
            'classes': ('suit-tab', 'suit-tab-category',),
            'fields': ['vehicle', ]}),
    ]


class VehicleTypeAdmin(ImportExportModelAdmin):
    resource_class = VehicleTypeResource
    list_display = ['name', ]
    fieldsets = [
        (_('Vehicle'), {
            'classes': ('suit-tab', 'suit-tab-category',),
            'fields': ['vehicle', ]}),
    ]


class BrandsAdmin(ImportExportModelAdmin):
    resource_class = BrandsResource
    list_display = ['name', ]
    fieldsets = [
        (_('Model'), {
            'classes': ('suit-tab', 'suit-tab-category',),
            'fields': ['model']}),
        (_('Vehicle'), {
            'classes': ('suit-tab', 'suit-tab-category',),
            'fields': ['vehicle', ]}),

    ]


class VehiclesAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'plate_number', 'year']
    list_filter = ['name', 'plate_number', ]
    resource_class = VehiclesResource
    list_display = ['name', 'plate_number', 'year']

# Register your models here.
admin.site.register(models.Vehicles, VehiclesAdmin)
admin.site.register(models.Model, ModelAdmin)
admin.site.register(models.Brands, BrandsAdmin)
admin.site.register(models.VehicleType, VehicleTypeAdmin)
