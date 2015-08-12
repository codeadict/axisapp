# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('censo', '0011_auto_20150810_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invproductos',
            name='cliente',
            field=models.ForeignKey(related_name=b'products', verbose_name=b'Cliente', to='censo.Cliente'),
        ),
    ]
