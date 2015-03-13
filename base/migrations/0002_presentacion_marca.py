# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentacion',
            name='marca',
            field=models.ForeignKey(verbose_name=b'Marca', to='base.Marca', null=True),
            preserve_default=True,
        ),
    ]
