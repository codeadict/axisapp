__author__ = 'codeadict'
from sdauth.models import User
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework import status
from rest_framework import generics

from api import serializers
from base.models import Area, Canal, MacroCanal, OcasionConsumo, SubCanal
from censo.models import Cliente

"""
Chasqui API

* `/api/users/` - Users collection
* `/api/users/1/` - User data
"""


class _ChasquiRequestMixin(object):
    """
    Base class that uses the request object in context
    """

    def get_serializer_context(self):
        return {'request': self.request}


class _ChasquiModelViewMixin(_ChasquiRequestMixin, viewsets.ModelViewSet):
    pass


class _CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Allow Model creation only
    """

    def get_serializer_context(self):
        return {'request': self.request}


class _CreateListRetrieveViewSet(_ChasquiRequestMixin,
                                 mixins.CreateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    def get_serializer_context(self):
        return {'request': self.request}


class ChasquiModelViewSet(_ChasquiModelViewMixin, viewsets.ModelViewSet):
    """
    Chasqui-specific CRUD with `request` in context
    """


class UserViewSet(ChasquiModelViewSet):
    """
    API Users CRUD endpoint.

    JSON does not support images uploading, so photo uploads only work with multipart REST.
    Empty photo upload does not change model field.
    """
    model = User
    serializer_class = serializers.UserSerializer
    filter_fields = ['email', 'last_name', 'first_name']


class UserAreasViewSet(ChasquiModelViewSet):
    model = Area

    serializer_class = serializers.AreasSerializer

    def get_queryset(self):
        user = self.request.user
        return Area.objects.filter(censador=user)


class ClientesAreaList(generics.ListAPIView):
    """
    Lista todos los clientes de determinada area
    """
    model = Cliente
    serializer_class = serializers.ClientsSerialier

    def get_queryset(self):
        queryset = Cliente.objects.all()
        area = self.kwargs.get('area', None)
        if area is not None:
            area_obj = Area.objects.get(pk=area)
            queryset = queryset.filter(coordenadas__within=area_obj.poligono)
        return queryset


class CustomersViewSet(ChasquiModelViewSet):
    """
    Lista todos los clientes de determinada area
    """
    model = Cliente

    serializer_class = serializers.ClientsSerialier


class MacroChannelViewSet(ChasquiModelViewSet):
    """
    Macro Canales
    """
    model = MacroCanal


class OcassionsViewSet(ChasquiModelViewSet):
    """
    Ocasiones de Consumo
    """
    model = OcasionConsumo
    serializer_class = serializers.OcassionsSerializer

    def list(self, request, macrochannel_pk=None):
        queryset = OcasionConsumo.objects.filter(macrocanal=macrochannel_pk)
        serializer = serializers.OcassionsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, macrochannel_pk=None):
        queryset = OcasionConsumo.objects.filter(pk=pk, macrocanal=macrochannel_pk)
        ocassion = get_object_or_404(queryset, pk=pk)
        serializer = serializers.OcassionsSerializer(ocassion)
        return Response(serializer.data)


class ChannelsViewSet(ChasquiModelViewSet):
    """
    Canales
    """
    model = Canal
    serializer_class = serializers.ChannelsSerializer

    def list(self, request, macrochannel_pk=None, ocassion_pk=None):
        queryset = self.model.objects.filter(ocasion=ocassion_pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, macrochannel_pk=None, ocassion_pk=None):
        queryset = self.model.objects.filter(pk=pk, ocasion=ocassion_pk)
        channel = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(channel)
        return Response(serializer.data)


class SubChannelsViewSet(ChasquiModelViewSet):
    """
    Sub-Canales
    """
    model = SubCanal
    serializer_class = serializers.SubChannelSerializer

    def list(self, request, macrochannel_pk=None, ocassion_pk=None, channel_pk=None):
        queryset = self.model.objects.filter(canal=channel_pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, macrochannel_pk=None, ocassion_pk=None, channel_pk=None):
        queryset = self.model.objects.filter(pk=pk, canal=channel_pk)
        subchannel = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(subchannel)
        return Response(serializer.data)