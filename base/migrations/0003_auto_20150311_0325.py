# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_presentacion_marca'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='agencia',
        ),
        migrations.RemoveField(
            model_name='area',
            name='censador',
        ),
        migrations.RemoveField(
            model_name='area',
            name='prevendedor',
        ),
        migrations.RemoveField(
            model_name='area',
            name='ruta',
        ),
        migrations.RemoveField(
            model_name='area',
            name='ruta_geom',
        ),
        migrations.RemoveField(
            model_name='area',
            name='tipo_ruta',
        ),
    ]
