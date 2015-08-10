# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('censo', '0010_auto_20150331_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='registrado_por',
            field=models.ForeignKey(verbose_name='Registrado Por', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visita',
            name='cliente',
            field=models.ForeignKey(related_name=b'visits', verbose_name=b'Cliente', to='censo.Cliente'),
        ),
    ]
