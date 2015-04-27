# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('hhrr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='county',
            field=models.CharField(max_length=255, null=True, verbose_name='County', blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'Provide international format +prefix-number', max_length=128, null=True, verbose_name='Phone number', blank=True),
        ),
    ]
