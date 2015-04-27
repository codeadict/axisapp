# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.fields
import django_countries.fields


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
            name='id_type',
            field=models.IntegerField(default=2, verbose_name='Identification type', choices=[(0, 'R.U.C.'), (1, 'Passport'), (2, 'National ID Card')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='nationality',
            field=django_countries.fields.CountryField(default=b'EC', max_length=2, verbose_name='Nationality'),
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
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.IntegerField(default=1, verbose_name='Status', choices=[(0, 'Inactive'), (1, 'Active'), (3, 'Settled')]),
        ),
    ]
