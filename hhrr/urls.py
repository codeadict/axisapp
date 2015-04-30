from django.conf.urls import patterns, url

urlpatterns = patterns('hhrr.views',
                       #url(r'^$', 'index', name='index'),

                       url(r'^employees/$', 'employee_list', name='employee-list'),
                       url(r'^employees/map/$', 'employee_map', name='employee-map'),
                       url(r'^employees/filter/$', 'employee_filter', name='employee-filter'),
                       url(r'^employees/add/$', 'employee_create', name='employee-add'),
                       url(r'^employees/(?P<pk>\d+)/$', 'employee_details', name='employee-details'),
                       url(r'^employees/(?P<pk>\d+)/edit/$', 'employee_update', name='employee-edit'),
                       url(r'^employees/(?P<pk>\d+)/delete/$', 'employee_delete', name='employee-delete'),
                       )
