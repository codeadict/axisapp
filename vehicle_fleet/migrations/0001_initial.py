# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.fields
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Vehicle Brand',
                'verbose_name_plural': 'Vehicle Brands',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Model Name')),
                ('brand', models.ForeignKey(related_name=b'models', verbose_name='Brand', to='vehicle_fleet.Brands')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Vehicle Model',
                'verbose_name_plural': 'Vehicle Models',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vehicles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plate_number', models.CharField(max_length=20, verbose_name='Plate number')),
                ('chassis_number', models.CharField(max_length=100, verbose_name='Chassis number')),
                ('year', models.PositiveIntegerField(verbose_name='Model year')),
                ('driver_name', models.CharField(max_length=255, verbose_name='Driver Name')),
                ('color', base.fields.ColorField(max_length=20, verbose_name='Color')),
                ('transmission', models.SmallIntegerField(default=0, verbose_name='Transmission type', choices=[(0, 'Automatic'), (1, 'Manual')])),
                ('fuel', models.SmallIntegerField(default=0, verbose_name='Fuel type', choices=[(0, 'Diesel'), (1, 'Gasoline'), (2, 'Electrical'), (3, 'Hybrid')])),
                ('power', models.PositiveIntegerField(help_text='Battery power in Kw', verbose_name='Power')),
                ('co2', models.FloatField(default=Decimal('0.00'), verbose_name='CO2 emission of the vehicle')),
                ('ownership', models.SmallIntegerField(default=1, verbose_name='Ownership', choices=[(0, 'Rented'), (1, 'Owned')])),
                ('vehicle_usage', models.SmallIntegerField(default=0, verbose_name='Usage', choices=[(0, 'Charge')])),
                ('doors', models.PositiveSmallIntegerField(default=2, verbose_name='Doors count')),
                ('people_capacity', models.PositiveSmallIntegerField(default=1, verbose_name='Number of passengers')),
                ('brand', models.ForeignKey(verbose_name=b'Brand', to='vehicle_fleet.Brands')),
                ('model', models.ForeignKey(verbose_name=b'Model', to='vehicle_fleet.Model')),
            ],
            options={
                'ordering': ['plate_number'],
                'verbose_name': 'Vehicle',
                'verbose_name_plural': 'Vehicles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VehicleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Vehicle Type',
                'verbose_name_plural': 'Vehicle Types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='vehicles',
            name='vehicle_type',
            field=models.ForeignKey(verbose_name='Vehicle type', to='vehicle_fleet.VehicleType'),
            preserve_default=True,
        ),
    ]
