# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('censo', '0012_auto_20150812_0426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invproductos',
            name='presentacion',
            field=models.PositiveIntegerField(verbose_name=b'Presentacion'),
        ),
    ]
