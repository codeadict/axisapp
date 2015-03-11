from django.conf.urls import patterns, url

urlpatterns = patterns('base.views',
                       url(r'^import/$', 'import_form', name='import'),
                       url(r'^import/template.xlsx$', 'import_template', name='import-template'),
)
