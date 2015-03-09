# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('censo', '0004_auto_20150308_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='horario_desde',
            field=models.TimeField(help_text=b'Formato 24 horas: 00:00', verbose_name=b'Horario Desde'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='horario_hasta',
            field=models.TimeField(help_text=b'Formato 24 horas: 00:00', verbose_name=b'Horario Hasta'),
        ),
    ]
