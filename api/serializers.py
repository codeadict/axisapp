__author__ = 'codeadict'
import datetime
import json

from sdauth.models import User
from base.models import Area, OcasionConsumo, MacroCanal, Canal, SubCanal, EmpresaActivos, EmpresaVisitas, Envase,\
    MacroCat, Categoria, Marca
from censo.models import Cliente
from django.db.models import Q

from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='user', read_only=False)
    user_link = serializers.HyperlinkedRelatedField(source='user', read_only=True, view_name='api:user-detail')

    new_user_email = None
    old_user_email = None

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name',
                  'last_name', 'date_of_birth',
                  'phone', 'mobile', 'gender',
                  'password')

    def validate_user_email(self, attrs, source):
        new_email = attrs['email']
        if not self.object or new_email != self.object.email:
            same_users = User.objects.filter(email=new_email)

            if same_users.exists():
                raise serializers.ValidationError('This email is already used')

        return attrs

    def restore_object(self, attrs, instance=None):
        old_email = instance and instance.email

        obj = super(UserSerializer, self).restore_object(attrs, instance)
        obj.is_admin = False

        user_email = attrs.get('email', old_email)

        # Storing emails for saving further
        if user_email != old_email and old_email:
            self.new_user_email = user_email
            self.old_user_email = old_email

        return obj


class AreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area


class OcassionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OcasionConsumo


class ChannelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Canal


class SubChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCanal


class MarketAssetsCompaniesSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmpresaActivos


class VisitsCompaniesSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmpresaVisitas


class PackagingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Envase


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria


class MakesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marca


class ClientsSerialier(serializers.ModelSerializer):
    foto = Base64ImageField(required=False)
    foto_local = Base64ImageField(required=False)

    class Meta:
        partial = True
        model = Cliente

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
