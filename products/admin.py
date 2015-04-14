from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import *

from import_export.admin import ImportExportModelAdmin
from import_export import resources


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        #form = CreateEmploymentHistoryForm


class IceTaxResource(resources.ModelResource):
    class Meta:
        model = IceTax
        #form = CreateEmploymentHistoryForm

class ProductAttributeResource(resources.ModelResource):
    class Meta:
        model = ProductAttribute
        #form = CreateEmploymentHistoryForm


class ProductAttributeValueResource(resources.ModelResource):
    class Meta:
        model = ProductAttributeValue
        #form = CreateEmploymentHistoryForm


class ProductAttributeValueUnitMeasureResource(resources.ModelResource):
    class Meta:
        model = ProductAttributeValueUnitMeasure
        #form = CreateEmploymentHistoryForm


class ProductImageResource(resources.ModelResource):
    class Meta:
        model = ProductImage
        #form = CreateEmploymentHistoryForm


class ProductsCategoryResource(resources.ModelResource):
    class Meta:
        model = ProductsCategory
        #form = CreateEmploymentHistoryForm


class IceTaxAdmin(ImportExportModelAdmin):
    resource_class = IceTaxResource
    list_display = ['name', ]

class ProductAttributeAdmin(ImportExportModelAdmin):
    resource_class = ProductAttributeResource
    list_display = ['name', ]


class ProductAttributeValueAdmin(ImportExportModelAdmin):
    resource_class = ProductAttributeValueResource
    list_display = ['name', 'value', 'unit_measure']


class ProductAttributeValueUnitMeasureAdmin(ImportExportModelAdmin):
    resource_class = ProductAttributeValueUnitMeasureResource
    list_display = ['name', 'representation_sign']


class ProductImageAdmin(ImportExportModelAdmin):
    resource_class = ProductImageResource
    list_display = ['identification', ]


class ProductsCategoryAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'date_created']
    list_filter = ['name', 'description', ]
    resource_class = ProductsCategoryResource
    list_display = ['name', 'description', 'date_created']

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-category',),
            'fields': ['name', 'full_name', 'description',  'parent',
                       'date_created', ]}),
        (_('Image'), {
            'classes': ('suit-tab', 'suit-tab-category',),
            'fields': ['image']}),
        (_('Attributes'), {
            'classes': ('suit-tab', 'suit-tab-category',),
            'fields': ['default_attributes', ]}),

    ]


class ProductAdmin(admin.ModelAdmin):
    """
    Product interface
    """
    search_fields = ['name', 'upc', 'title', 'type', 'active', 'category']
    list_filter = ['name', 'upc']
    resource_class = ProductResource
    list_display = ['name', 'upc', 'category', 'type']

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-product',),
            'fields': ['name', 'description', 'title',  'type',
                       'upc', 'active', 'date_created', 'score', ]}),

        (_('Image'), {
            'classes': ('suit-tab', 'suit-tab-product',),
            'fields': ['image']}),

        (_('Category'), {
            'classes': ('suit-tab', 'suit-tab-local',),
            'fields': ['category', ]}),

        (_('Taxes'), {
            'classes': ('suit-tab', 'suit-tab-local',),
            'fields': ['taxes', 'province', 'parish', 'canton', 'county',
                       'city', 'postcode', 'nationality', ]}),

        (_('Attributes'), {
            'classes': ('suit-tab', 'suit-tab-product',),
            'fields': ['attributes', ]}),

        (_('Related products'), {
            'classes': ('suit-tab', 'suit-tab-local',),
            'fields': ['related_products', ]}),
        ]


class ProductStockAdmin(admin.ModelAdmin):
    """
    Product interface
    """
    search_fields = ['date_created', 'date_updated', 'is_low_stock']
    list_filter = ['date_created', 'date_updated', 'is_low_stock']
    resource_class = ProductResource
    list_display = ['product', 'price_excl_tax', 'items_number', 'date_created']

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-stock',),
            'fields': ['product', 'price_excl_tax', 'cost_price',  'price_currency',
                       'items_number', 'low_stock_threshold', 'date_created', ]}),
    ]

# Register your models here.
admin.site.register(IceTax, IceTaxAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductAttributeValue, ProductAttributeValueAdmin)
admin.site.register(ProductAttributeValueUnitMeasure, ProductAttributeValueUnitMeasureAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductsCategory, ProductsCategoryAdmin)