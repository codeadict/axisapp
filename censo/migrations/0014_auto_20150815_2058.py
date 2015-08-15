# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('censo', '0013_auto_20150812_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='registrado_por',
            field=models.ForeignKey(verbose_name='Registrado Por', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='invproductos',
            name='presentacion',
            field=models.PositiveIntegerField(verbose_name=b'Presentacion(ML)'),
        ),
    ]
