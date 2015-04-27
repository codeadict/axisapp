from django.conf.urls import patterns, url

urlpatterns = patterns('products.views',
                       #url(r'^$', 'index', name='index'),

                       url(r'^products/$', 'product_list', name='product-list'),
                       url(r'^products/filter/$', 'product_filter', name='product-filter'),
                       url(r'^products/add/$', 'product_create', name='product-add'),
                       url(r'^products/(?P<pk>\d+)/$', 'product_details', name='product-details'),
                       url(r'^products/(?P<pk>\d+)/edit/$', 'product_update', name='product-edit'),
                       url(r'^products/(?P<pk>\d+)/delete/$', 'product_delete', name='product-delete'),

                       url(r'^category/$', 'category_list', name='product-category-details'),
                       url(r'^category/filter/$', 'category_filter', name='product-category-filter'),
                       url(r'^category/add/$', 'category_create', name='product-category-add'),
                       url(r'^category/(?P<pk>\d+)/$', 'category_details', name='product-category-details'),
                       url(r'^category/(?P<pk>\d+)/edit/$', 'category_update', name='product-category-edit'),
                       url(r'^category/(?P<pk>\d+)/delete/$', 'category_delete', name='product-category-delete'),

                       #url(r'^employees/(?P<pk>\d+)/set_status/$', 'employee_set_status', name='employee-set-status'),
                       #url(r'^search/$', 'search_universal', name='search-universal'),
                       #url(r'^partner/(?P<pk>\d+)/set_label/$', 'role_set_label', name='role-set-label'),
                       #url(r'^employees/distribution/$', 'distribution_list', name='presales-client-distribution'),
                       #url(r'^employees/distribution/generate/$', 'distribution_generate', name='generate-distribution'),
                       )
