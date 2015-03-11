# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('censo', '0005_auto_20150308_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='identif',
            field=models.CharField(max_length=16, verbose_name=b'Identificacion'),
        ),
    ]
