# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20150323_0644'),
    ]

    operations = [
        migrations.CreateModel(
            name='IceTax',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('code', models.IntegerField(max_length=255, verbose_name='Code')),
                ('percent', models.DecimalField(default=Decimal('0'), max_digits=20, decimal_places=2)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'I.C.E. tax',
                'verbose_name_plural': 'I.C.E taxes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.CharField(max_length=2048, verbose_name='Description', blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('type', models.IntegerField(default=0, verbose_name='Type', choices=[(0, 'Consumable'), (1, 'Service')])),
                ('price_excl_tax', models.FloatField(default=0.0, verbose_name='Price')),
                ('cost_price', models.FloatField(default=0.0, verbose_name='Cost price')),
                ('price_currency', models.CharField(default='$', max_length=12, verbose_name='Currency')),
                ('iva_tax', models.IntegerField(default=2, verbose_name='Taxes', choices=[(0, 'No I.V.A.'), (0, 'I.V.A. 0%'), (0, 'I.V.A. 12%')])),
                ('active', models.IntegerField(default=1, verbose_name='Active', choices=[(0, 'Not Active'), (1, 'Active')])),
                ('score', models.FloatField(default=Decimal('0'), verbose_name='Score', db_index=True)),
                ('date_created', models.DateField(default=products.models.date_default, verbose_name='Date Created')),
                ('attributes', models.ManyToManyField(to='products.ProductAttribute', null=True, verbose_name='Attributes', blank=True)),
                ('category', models.ForeignKey(verbose_name='Category', to='products.ProductsCategory')),
                ('image', models.ForeignKey(to='products.ProductImage', null=True)),
                ('related_items', models.ForeignKey(verbose_name='Related items', blank=True, to='products.Product', null=True)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='stock',
            name='product',
        ),
        migrations.DeleteModel(
            name='Stock',
        ),
        migrations.RemoveField(
            model_name='taxesvalue',
            name='tax_id',
        ),
        migrations.DeleteModel(
            name='TaxesValue',
        ),
        migrations.RemoveField(
            model_name='product',
            name='related_products',
        ),
        migrations.RemoveField(
            model_name='product',
            name='taxes',
        ),
        migrations.DeleteModel(
            name='Taxes',
        ),
        migrations.AddField(
            model_name='product',
            name='cost_price',
            field=models.FloatField(default=0.0, verbose_name='Cost price'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='ice_tax',
            field=models.ForeignKey(default=Decimal('0'), verbose_name='Ice', to='products.IceTax'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='items_stock_number',
            field=models.BigIntegerField(default=0, verbose_name='Number in stock', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='iva_tax',
            field=models.IntegerField(default=2, verbose_name='Taxes', choices=[(0, 'No I.V.A.'), (0, 'I.V.A. 0%'), (0, 'I.V.A. 12%')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='low_stock_threshold',
            field=models.IntegerField(null=True, verbose_name='Low Stock Threshold', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='price_currency',
            field=models.CharField(default='$', max_length=12, verbose_name='Currency'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='price_excl_tax',
            field=models.FloatField(default=0.0, verbose_name='Price'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='related_items',
            field=models.ForeignKey(verbose_name='Related items', blank=True, to='products.Product', null=True),
            preserve_default=True,
        ),
    ]
