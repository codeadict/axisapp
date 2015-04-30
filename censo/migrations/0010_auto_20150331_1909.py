# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('censo', '0009_auto_20150310_0428'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'ordering': ['nombres']},
        ),
        migrations.AlterField(
            model_name='activosmercado',
            name='cliente',
            field=models.ForeignKey(related_name=b'market_assets', verbose_name=b'Cliente', to='censo.Cliente'),
        ),
        migrations.AlterField(
            model_name='presalesdistribution',
            name='final_client',
            field=models.ForeignKey(related_name=b'presales_final', blank=True, to='censo.Cliente', help_text='Select the final client from where you will finish selling', null=True),
        ),
    ]
