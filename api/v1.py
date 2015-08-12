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
from rest_framework.decorators import action
from rest_framework import generics

from api import serializers
from api.libs import tools
from base.models import Area, Canal, MacroCanal, OcasionConsumo, SubCanal, EmpresaActivos, EmpresaVisitas, Envase,\
    MacroCat, Categoria, Marca
from censo.models import Cliente, Visita, InvProductos, ActivosMercado
from tracking.models import UserTracking

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
    queryset = Cliente.objects.all()
    lookup_field = 'pk'
    model = Cliente
    paginate_by = 100
    serializer_class = serializers.ClientsSerialier


    @action(methods=['DELETE', 'GET', 'POST'])
    def visits(self, request, *args, **kwargs):
        """
        Agregar o listar visitas a un cliente
        """
        cliente = self.object = self.get_object()
        data = {}
        status_code = status.HTTP_200_OK

        if request.method.upper() in ['DELETE', 'POST']:
            pk = request.DATA.get('pk') or request.QUERY_PARAMS.get('pk')

            if pk:
                try:
                    visita = Visita.objects.filter(cliente=cliente).get(pk=pk)
                except Visita.DoesNotExist:
                    status_code = status.HTTP_400_BAD_REQUEST
                    data['pk'] = [_(u"La visita `%(pk)s` no existe para este cliente." % {'pk': pk})]
                else:
                    if request.method == 'POST':
                        if isinstance(visita, Visita):
                            serializer = serializers.VisitasSerializer(visita, context={'request': request})
                            data = serializer.data
                    elif request.method == 'DELETE':
                        tools.remove_visit_from_client(cliente, visita)
                    status_code = status.HTTP_201_CREATED
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                data['pk'] = [_(u"Debe especificar un id de visita.")]

            return Response(visita, status=status.HTTP_400_BAD_REQUEST)

        if status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            visitas = tools.get_client_visits(cliente)
            paginated = self.paginate_queryset(visitas)
            serializer = serializers.VisitasSerializer(paginated, context={'request': request}, many=True)
            data = serializer.data

        return Response(data)


    def list(self, request, *args, **kwargs):
        data = {}
        area = request.QUERY_PARAMS.get('area')

        if area:
            try:
                area_obj = Area.objects.get(pk=area)
                self.object_list = Cliente.objects.filter(estado=Cliente.ACTIVO, coordenadas__within=area_obj.poligono)\
                    .values('id', 'nombres', 'apellidos', 'tipo_id', 'identif')
            except Area.DoesNotExist:
                status_code = status.HTTP_400_BAD_REQUEST
                data['result'] = [_(u"El area `%(pk)s` no existe." % {'pk': area})]
                return Response(data)
        else:
            self.object_list  = self.filter_queryset(self.get_queryset().values('id', 'nombres', 'apellidos', 'tipo_id', 'identif'))

        #serializer = self.get_serializer(self.object_list, many=True)
        return Response(self.object_list)


class MacroChannelViewSet(ChasquiModelViewSet):
    """
    Macro Canales
    """
    model = MacroCanal
    paginate_by = None


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

class MarketAssetsCompanies(ChasquiModelViewSet):
    model = EmpresaActivos
    serializer_class = serializers.MarketAssetsCompaniesSerializer
    paginate_by = None


class VisitsCompaniesViewSet(ChasquiModelViewSet):
    model = EmpresaVisitas
    serializer_class = serializers.VisitsCompaniesSerializer
    paginate_by = None


class PackagesViewSet(ChasquiModelViewSet):
    model = Envase
    serializer_class = serializers.PackagingSerializer
    paginate_by = None


class MacroCategoryViewSet(ChasquiModelViewSet):
    model = MacroCat
    paginate_by = None


class CategoryViewSet(ChasquiModelViewSet):
    """
    Categorias de Productos
    """
    model = Categoria
    serializer_class = serializers.CategoriesSerializer

    def list(self, request, macrocategory_pk=None):
        queryset = self.model.objects.filter(macro=macrocategory_pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, macrocategory_pk=None):
        queryset = self.model.objects.filter(pk=pk, macro=macrocategory_pk)
        category = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(category)
        return Response(serializer.data)


class MakeViewSet(ChasquiModelViewSet):
    """
    Marcas de Productos
    """
    model = Marca
    serializer_class = serializers.MakesSerializer

    def list(self, request, macrocategory_pk=None, category_pk=None):
        queryset = self.model.objects.filter(categoria=category_pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, macrocategory_pk=None, category_pk=None):
        queryset = self.model.objects.filter(pk=pk, categoria=category_pk)
        make = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(make)
        return Response(serializer.data)


class TrackingViewSet(ChasquiModelViewSet):
    """
    Enpoint para seguimiento del usuario.
    """
    model = UserTracking
    serializer_class = serializers.TrackingSerializer
    filter_fields = ['user']

    def get_queryset(self):
        qs = self.model.objects.all()
        return qs.select_related('user')