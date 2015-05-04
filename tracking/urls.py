from django.conf.urls import patterns, url

urlpatterns = patterns('tracking.views',
                       url(r'^employee/tracking/$', 'tracking_view', name='employee-tracking'),
)