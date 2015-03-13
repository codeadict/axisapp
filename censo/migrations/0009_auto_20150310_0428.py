# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('censo', '0008_auto_20150309_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invproductos',
            name='presentacion',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, to='base.Presentacion', chained_model_field=b'marca', chained_field=b'marca', verbose_name=b'Presentacion'),
        ),
    ]
