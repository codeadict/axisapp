# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hhrr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='family_dependants',
            field=models.ForeignKey(related_name=b'family_dependants', verbose_name='Family dependants', to='hhrr.FamilyDependant'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='handicap_card_number',
            field=models.CharField(max_length=255, verbose_name='Handicap card number', blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='handicap_percent',
            field=base.fields.PercentageField(default=0, verbose_name='Handicap percent', max_digits=6, decimal_places=3, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='handicap_type',
            field=models.CharField(max_length=255, verbose_name='Handicap type', blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.ImageField(upload_to=b'photos/employee/', null=True, verbose_name='Image', blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='skype',
            field=models.CharField(max_length=255, verbose_name='Skype user', blank=True),
        ),
    ]
