# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_auto_20150809_0626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parroquia',
            name='nombre',
            field=models.CharField(max_length=255, verbose_name=b'Nombre de la Parroquia'),
        ),
    ]
