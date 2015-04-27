from django.conf.urls import patterns, url

urlpatterns = patterns('hhrr.views',
                       #url(r'^$', 'index', name='index'),

                       url(r'^employees/$', 'employee_list', name='employee-list'),
                       #url(r'^employees/map/$', 'client_map', name='client-map'),
                       url(r'^employees/filter/$', 'employee_filter', name='employee-filter'),
                       url(r'^employees/add/$', 'employee_create', name='employee-add'),
                       url(r'^employees/(?P<pk>\d+)/$', 'employee_details', name='employee-details'),
                       url(r'^employees/(?P<pk>\d+)/edit/$', 'employee_update', name='employee-edit'),
                       url(r'^employees/(?P<pk>\d+)/delete/$', 'employee_delete', name='employee-delete'),
                       #url(r'^employees/(?P<pk>\d+)/set_status/$', 'employee_set_status', name='employee-set-status'),
                       #url(r'^search/$', 'search_universal', name='search-universal'),
                       #url(r'^partner/(?P<pk>\d+)/set_label/$', 'role_set_label', name='role-set-label'),
                       #url(r'^employees/distribution/$', 'distribution_list', name='presales-client-distribution'),
                       #url(r'^employees/distribution/generate/$', 'distribution_generate', name='generate-distribution'),
                       )
