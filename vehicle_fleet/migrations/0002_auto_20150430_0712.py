# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_fleet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='vehicle_usage',
            field=models.SmallIntegerField(default=0, verbose_name='Usage', choices=[(0, 'Charge'), (1, 'Transportation')]),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='year',
            field=models.PositiveIntegerField(null=True, verbose_name='Model year', blank=True),
        ),
    ]
