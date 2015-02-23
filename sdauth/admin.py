# This Python file uses the following encoding: utf-8
from account.models import Account, EmailAddress
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse

from .forms import UserChangeForm
from .models import User, History


class SDUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserChangeForm
    list_display = ('id', 'email', 'get_full_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('Credenciales', {'fields': ('email', 'password')}),
        ('Permisos', {'fields': ('is_admin', 'is_active', 'is_deleted')}),
        ('Información Personal', {'fields': (
            'first_name',
            'last_name',
            'mobile',
            'phone',
            'gender',
            'date_of_birth',
            'street'
        )})
    )
    add_fieldsets = fieldsets

    search_fields = ('email', 'last_name')
    ordering = ('-is_admin', 'id')
    filter_horizontal = ()

    def get_queryset(self, request):
        qs = super(SDUserAdmin, self).get_queryset(request)
        return qs


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('timestamp', 'action',)
    search_fields = ('user__email', )

    def get_readonly_fields(self, request, obj=None):
        """
        Make all fields read_only
        """
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


class AccountAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']

    def get_queryset(self, request):
        return super(AccountAdmin, self).get_queryset(request).select_related('user')


class EmailAddressAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']


admin.site.register(User, SDUserAdmin)

admin.site.unregister(Group)

admin.site.register(History, HistoryAdmin)

admin.site.unregister(Account)
admin.site.register(Account, AccountAdmin)

admin.site.unregister(EmailAddress)
admin.site.register(EmailAddress, EmailAddressAdmin)