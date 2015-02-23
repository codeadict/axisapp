__author__ = 'codeadict'
from sdauth.models import User

from rest_framework import generics

from api import serializers
from base.models import Area
from censo.models import Cliente

class UserListAPIView(generics.ListAPIView):
    """
    Vista para manejar autenticacion de usuarios
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserAreasList(generics.ListAPIView):
    serializer_class = serializers.AreasSerializer

    def get_queryset(self):
        user = self.request.user
        return Area.objects.filter(censador=user)


class ClientesAreaList(generics.ListAPIView):
    """
    Lista todos los clientes de determinada area
    """
    model = Cliente

    def get_queryset(self):
        queryset = Cliente.objects.all()
        area = self.kwargs.get('area', None)
        if area is not None:
            area_obj = Area.objects.get(pk=area)
            queryset = queryset.filter(coordenadas__within=area_obj.poligono)
        return queryset