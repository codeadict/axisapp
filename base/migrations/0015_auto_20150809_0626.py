# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_auto_20150809_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='parroquia',
            name='codigo',
            field=models.CharField(default=b'', unique=True, max_length=10, verbose_name=b'Codigo de la Parroquia', db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='parroquia',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='canton',
            name='codigo',
            field=models.CharField(default=b'', unique=True, max_length=10, verbose_name=b'Codigo del Canton', db_index=True),
        ),
        migrations.AlterField(
            model_name='parroquia',
            name='canton',
            field=models.ForeignKey(to='base.Canton', to_field=b'codigo'),
        ),
    ]
