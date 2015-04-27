from django.contrib import admin
from hhrr import models
from hhrr.forms import *
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

from import_export.admin import ImportExportModelAdmin
from import_export import resources


class EmploymentHistoryResource(resources.ModelResource):
    class Meta:
        model = EmploymentHistory
        #form = CreateEmploymentHistoryForm


class LanguageResource(resources.ModelResource):
    class Meta:
        model = models.Language
        #form = CreateLanguageForm


class FamilyRelationResource(resources.ModelResource):
    class Meta:
        model = models.FamilyRelation
        #form = CreateFamilyRelationForm


class FamilyDependantResource(resources.ModelResource):
    class Meta:
        model = models.FamilyDependant
        #form = CreateFamilyDependantForm


class EducationAreaResource(resources.ModelResource):
    class Meta:
        model = models.EducationArea
        #form = CreateEducationAreaForm


class EducationResource(resources.ModelResource):
    class Meta:
        model = models.Education
        #form = CreateEducationForm


class EnterpriseDepartmentResource(resources.ModelResource):
    class Meta:
        model = models.EnterpriseDepartment
        #form = CreateEnterpriseDepartmentForm


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = models.Employee
        exclude = []


class EmploymentHistoryAdmin(ImportExportModelAdmin):
    resource_class = EmploymentHistoryResource
    list_display = ['company', 'position', 'date_in', 'time_worked']


class LanguageAdmin(ImportExportModelAdmin):
    resource_class = LanguageResource
    list_display = ['name', ]


class FamilyRelationAdmin(ImportExportModelAdmin):
    resource_class = FamilyRelationResource
    list_display = ['name', ]


class FamilyDependantAdmin(ImportExportModelAdmin):
    resource_class = FamilyDependantResource
    list_display = ['name', 'last_name', 'relationship']


class EducationAreaAdmin(ImportExportModelAdmin):
    resource_class = EducationAreaResource
    list_display = ['name', ]


class EducationAdmin(ImportExportModelAdmin):
    resource_class = EducationResource
    list_display = ['institution', 'country', 'education_area', ]


class EnterpriseDepartmentAdmin(ImportExportModelAdmin):
    resource_class = EnterpriseDepartmentResource
    list_display = ['name', 'manager', 'parent', ]


class EmployeeAdmin(admin.ModelAdmin):
    """
    Interfaz para clientes
    """
    #inlines = (EducationAreaInline, EmploymentHistoryInline, EnterpriseDepartmentInline,
    #           FamilyDependantInline, EducationInline, FamilyRelationInline, LanguageInline)
    #readonly_fields = ('photo',)
    search_fields = ['name', 'last_name', 'identification', 'email', 'department', ]
    list_filter = ['email', 'name', 'last_name', ]
    resource_class = EmployeeResource
    list_display = ['email', 'name', 'last_name', 'identification', 'marital_status']

    #suit_form_tabs = (('cliente', 'Datos Cliente'), ('local', 'Datos Local'), ('localizacion', 'Localizacion'),
    #                  ('activo', 'Activos Mercado'), ('visita', 'Visitas'), ('inventario', 'Cat. Productos'),
    #                  ('foto_local', 'Foto'))

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-employee',),
            'fields': ['email', 'name', 'last_name', 'id_type',  'identification',
                       'phone', 'cellphone', 'sex', 'skype', 'birthday', 'ethnic_race',
                       'status', ]}),

        (_('Photo'), {
            'classes': ('suit-tab', 'suit-tab-employee',),
            'fields': ['photo']}),

        (_('Address'), {
            'classes': ('suit-tab', 'suit-tab-local',),
            'fields': ['address', 'province', 'parish', 'canton', 'county',
                       'city', 'postcode', 'nationality', ]}),

        (_('Medical information'), {
            'classes': ('suit-tab', 'suit-tab-employee',),
            'fields': ['blood_type', 'handicapped', 'handicap_percent', 'handicap_type',
                       'handicap_card_number', 'emergency_person', 'emergency_phone', ]}),

        (_('Status'), {
            'classes': ('suit-tab', 'suit-tab-local',),
            'fields': ['marital_status', ]}),

        (_('Economics'), {
            'classes': ('suit-tab', 'suit-tab-local',),
            'fields': ['maintain_reserve_funds', ]}),
        ]

# Register your models here.
admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.Education, EducationAdmin)
admin.site.register(models.EducationArea, EducationAreaAdmin)
admin.site.register(models.EmploymentHistory, EmploymentHistoryAdmin)
admin.site.register(models.EnterpriseDepartment, EnterpriseDepartmentAdmin)
admin.site.register(models.FamilyDependant, FamilyDependantAdmin)
admin.site.register(models.FamilyRelation, FamilyRelationAdmin)
admin.site.register(models.Language, LanguageAdmin)

