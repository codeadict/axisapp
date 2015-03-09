# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('censo', '0003_auto_20150307_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='coordenadas',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, db_column=b'geom', blank=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='horario_desde',
            field=models.TimeField(help_text=b'Formato 24 horas: 00:00', verbose_name=b'Atencion Desde'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='horario_hasta',
            field=models.TimeField(help_text=b'Formato 24 horas: 00:00', verbose_name=b'Atencion Hasta'),
        ),
    ]
