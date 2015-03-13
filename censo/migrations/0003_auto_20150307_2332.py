# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('censo', '0002_auto_20150305_0118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='frecuencia',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='secuencia',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cumple',
            field=models.DateField(null=True, verbose_name=b'Cumpleanos', blank=True),
        ),
    ]
