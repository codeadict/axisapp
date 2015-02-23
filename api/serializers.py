__author__ = 'codeadict'
from django.contrib.auth.models import User
from base.models import Area
from django.db.models import Q
import datetime
import json
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class AreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        exclude = ('censador', 'prevendedor')


class AreasNestedSerializer(serializers.ModelSerializer):
    clientes = serializers.SerializerMethodField('obtener_clientes_area')
    geojson = serializers.SerializerMethodField('obtener_geojson')

    def obtener_clientes_area(self, *args, **kwargs):
        area = args[0]
        return {}

    def get_geojson(self, *args, **kwargs):
        area = args[0]
        return json.loads(area.polygone)

    class Meta:
        model = Area
