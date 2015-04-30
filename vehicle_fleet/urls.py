from django.conf.urls import patterns, url

urlpatterns = patterns('vehicle_fleet.views',
                       #url(r'^$', 'index', name='index'),

                       url(r'^vehicles/$', 'vehicles_list', name='vehicles-list'),
                       url(r'^vehicles/filter/$', 'vehicles_filter', name='vehicles-filter'),
                       url(r'^vehicles/add/$', 'vehicles_create', name='vehicles-add'),
                       url(r'^vehicles/(?P<pk>\d+)/$', 'vehicles_details', name='vehicles-details'),
                       url(r'^vehicles/(?P<pk>\d+)/edit/$', 'vehicles_update', name='vehicles-edit'),
                       url(r'^vehicles/(?P<pk>\d+)/delete/$', 'vehicles_delete', name='vehicles-delete'),

                       #url(r'^category/$', 'category_list', name='product-category-details'),
                       #url(r'^category/filter/$', 'category_filter', name='product-category-filter'),
                       #url(r'^category/add/$', 'category_create', name='product-category-add'),
                       #url(r'^category/(?P<pk>\d+)/$', 'category_details', name='product-category-details'),
                       #url(r'^category/(?P<pk>\d+)/edit/$', 'category_update', name='product-category-edit'),
                       #url(r'^category/(?P<pk>\d+)/delete/$', 'category_delete', name='product-category-delete'),

                       #url(r'^employees/(?P<pk>\d+)/set_status/$', 'employee_set_status', name='employee-set-status'),
                       #url(r'^search/$', 'search_universal', name='search-universal'),
                       #url(r'^partner/(?P<pk>\d+)/set_label/$', 'role_set_label', name='role-set-label'),
                       #url(r'^employees/distribution/$', 'distribution_list', name='presales-client-distribution'),
                       #url(r'^employees/distribution/generate/$', 'distribution_generate', name='generate-distribution'),
                       )
