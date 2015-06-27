__author__ = 'codeadict'
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from rest_framework.authtoken import views as rf_views

from api import v1 as views

from django.conf.urls import url, include, patterns

from api.routers import NamespaceRouter

router = NamespaceRouter()

router.register(r'users', views.UserViewSet)
router.register(r'areas', views.UserAreasViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include token URL
urlpatterns = patterns('api.views',
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', rf_views.obtain_auth_token),
    url(r'^clientes/(?P<area>\d+)', views.ClientesAreaList.as_view()),
)
