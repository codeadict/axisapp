__author__ = 'codeadict'
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

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
)


# urlpatterns = patterns('',
#     url(r'v1/auth/login/', 'rest_framework_jwt.views.obtain_jwt_token'),
#     url(r'v1/users/', views.UserListAPIView.as_view()),
#     url(r'v1/user_areas/', views.UserAreasList.as_view()),
#     url(r'v1/clientes/(?P<area>\d+)', views.ClientesAreaList.as_view()),
# )
