# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('censo', '0002_auto_20150305_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='presalesdistribution',
            name='frequency',
            field=models.CommaSeparatedIntegerField(max_length=32, null=True, verbose_name='Visit Days', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='presalesdistribution',
            name='route_type',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Route Type', choices=[(0, 'Pre Sale'), (1, 'Auto Sale'), (2, 'Tele Sale')]),
            preserve_default=True,
        ),
    ]
