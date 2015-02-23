__author__ = 'codeadict'
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from api import v1 as views

urlpatterns = patterns('',
    url(r'v1/auth/login/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'v1/users/', views.UserListAPIView.as_view()),
    url(r'v1/user_areas/', views.UserAreasList.as_view()),
    url(r'v1/clientes/(?P<area>\d+)', views.ClientesAreaList.as_view()),
)
