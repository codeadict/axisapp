# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('censo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresalesDistribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Polygon Name', blank=True)),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(srid=4326, verbose_name='Polygon')),
                ('assigned_seller', models.ForeignKey(related_name=b'areas_preseller', verbose_name=b'Assigned Pre-seller', to=settings.AUTH_USER_MODEL, null=True)),
                ('clients', models.ManyToManyField(related_name=b'distributions', verbose_name='Clients', to='censo.Cliente', blank=True)),
            ],
            options={
                'verbose_name': 'Distribution Area',
                'verbose_name_plural': 'Distribution Areas',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='invproductos',
            options={'verbose_name': 'Inventario Producto', 'verbose_name_plural': 'Inventario Productos'},
        ),
    ]
