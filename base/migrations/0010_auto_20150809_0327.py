# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0009_auto_20150809_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provincia',
            name='codigo',
            field=models.CharField(unique=True, max_length=10, verbose_name=b'Codigo de Provincia'),
        ),
        migrations.AddField(
            model_name='canton',
            name='codigo',
            field=models.CharField(default=b'', unique=True, max_length=10, verbose_name=b'Codigo de Provincia',
                                   db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='canton',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='canton',
            name='provincia',
            field=models.ForeignKey(to='base.Provincia', to_field=b'codigo'),
        ),
    ]
