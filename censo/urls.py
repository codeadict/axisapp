from django.conf.urls import patterns, url

urlpatterns = patterns('partners.views',
                       #url(r'^$', 'index', name='index'),

                       url(r'^clients/$', 'client_list', name='client-list'),
                       url(r'^clients/map/$', 'client_map', name='client-map'),
                       url(r'^clients/filter/$', 'client_filter', name='client-filter'),
                       url(r'^clients/add/$', 'client_create', name='client-add'),
                       url(r'^clients/(?P<pk>\d+)/$', 'client_details', name='client-details'),
                       url(r'^clients/(?P<pk>\d+)/edit/$', 'client_update', name='client-edit'),
                       url(r'^clients/(?P<pk>\d+)/delete/$', 'client_delete', name='client-delete'),
                       url(r'^clients/(?P<pk>\d+)/set_status/$', 'client_set_status', name='client-set-status'),
                       #url(r'^search/$', 'search_universal', name='search-universal'),
                       url(r'^partner/(?P<pk>\d+)/set_label/$', 'role_set_label', name='role-set-label'),
)
