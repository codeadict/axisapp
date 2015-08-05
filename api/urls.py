__author__ = 'codeadict'
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView


from rest_framework.authtoken import views as rf_views
from rest_framework_nested import routers

from api.routers import NamespaceRouter
from api import v1 as views


router = NamespaceRouter()

router.register(r'users', views.UserViewSet)
router.register(r'areas', views.UserAreasViewSet)
router.register(r'customers', views.CustomersViewSet)
router.register(r'macrochannels', views.MacroChannelViewSet, base_name='macrochannels')
router.register(r'marketassetcompanies', views.MarketAssetsCompanies)
router.register(r'visitscompanies', views.VisitsCompaniesViewSet)
router.register(r'packages', views.PackagesViewSet)
router.register(r'macrocategories', views.MacroCategoryViewSet)
router.register(r'locations', views.TrackingViewSet)

ocassions_router = routers.NestedSimpleRouter(router, r'macrochannels', lookup='macrochannel')
ocassions_router.register(r'ocassions', views.OcassionsViewSet, base_name='ocassions')

channels_router = routers.NestedSimpleRouter(ocassions_router, r'ocassions', lookup='ocassion')
channels_router.register(r'channels', views.ChannelsViewSet, base_name='channels')

subchannels_router = routers.NestedSimpleRouter(channels_router, r'channels', lookup='channel')
subchannels_router.register(r'subchannels', views.SubChannelsViewSet, base_name='subchannels')

categories_router = routers.NestedSimpleRouter(router, r'macrocategories', lookup='macrocategory')
categories_router.register(r'categories', views.CategoryViewSet, base_name='categories')

brands_router = routers.NestedSimpleRouter(categories_router, r'categories', lookup='category')
brands_router.register(r'brands', views.MakeViewSet, base_name='brands')



# Wire up our API using automatic URL routing.
# Additionally, we include token URL
urlpatterns = patterns('api.views',
    url(r'^', include(router.urls)),
    url(r'^', include(ocassions_router.urls)),
    url(r'^', include(channels_router.urls)),
    url(r'^', include(subchannels_router.urls)),
    url(r'^', include(categories_router.urls)),
    url(r'^', include(brands_router.urls)),
    url(r'^api-token-auth/', rf_views.obtain_auth_token),
    url(r'^clientes/(?P<area>\d+)', views.ClientesAreaList.as_view()),
)
