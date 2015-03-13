# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0003_auto_20150311_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='agencia',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Agencia', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='censador',
            field=models.ForeignKey(related_name=b'areas_censador', verbose_name=b'Censador Asignado', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='prevendedor',
            field=models.ForeignKey(related_name=b'areas_prevendedor', verbose_name=b'Prevendedor Asignado', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='ruta',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Ruta', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='ruta_geom',
            field=django.contrib.gis.db.models.fields.LineStringField(help_text=b'Ruta a seguir por el censador o prevendedor', srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='tipo_ruta',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Tipo Ruta', blank=True),
            preserve_default=True,
        ),
    ]
