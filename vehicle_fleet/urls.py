from django.conf.urls import patterns, url

urlpatterns = patterns('vehicle_fleet.views',
                       url(r'^vehicles/$', 'vehicles_list', name='vehicles-list'),
                       url(r'^vehicles/filter/$', 'vehicles_filter', name='vehicles-filter'),
                       url(r'^vehicles/add/$', 'vehicles_create', name='vehicles-add'),
                       url(r'^vehicles/(?P<pk>\d+)/$', 'vehicles_details', name='vehicles-details'),
                       url(r'^vehicles/(?P<pk>\d+)/edit/$', 'vehicles_update', name='vehicles-edit'),
                       url(r'^vehicles/(?P<pk>\d+)/delete/$', 'vehicles_delete', name='vehicles-delete'),
                       )
