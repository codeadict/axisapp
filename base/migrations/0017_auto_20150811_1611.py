# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_auto_20150809_0636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='canton',
        ),
        migrations.RemoveField(
            model_name='area',
            name='parroquia',
        ),
        migrations.RemoveField(
            model_name='area',
            name='provincia',
        ),
        migrations.RemoveField(
            model_name='area',
            name='ruta_geom',
        ),
    ]
