# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('censo', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='presalesdistribution',
            name='final_client',
            field=models.ForeignKey(related_name=b'presales_final', blank=True, to='censo.Cliente', help_text='Select the final client from where you will start selling', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='presalesdistribution',
            name='initial_client',
            field=models.ForeignKey(related_name=b'presales_initial', blank=True, to='censo.Cliente', help_text='Select the initial client from where you will start selling', null=True),
            preserve_default=True,
        ),
    ]
