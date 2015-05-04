from django.contrib import admin

from tracking.models import UserTracking


class TrackingAdmin(admin.ModelAdmin):
    """
    Administer users activity
    """
    list_display = ['user', 'date_time', 'lat', 'lgn']
    list_filter = ['user', 'date_time',]


admin.site.register(UserTracking, TrackingAdmin)
