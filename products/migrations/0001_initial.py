# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import products.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.CharField(max_length=2048, verbose_name='Description', blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('type', models.IntegerField(default=0, verbose_name='Type', choices=[(0, 'Consumable'), (1, 'Service')])),
                ('upc', models.CharField(null=True, max_length=64, blank=True, help_text='Universal Product Code (UPC)', unique=True, verbose_name='UPC')),
                ('active', models.IntegerField(default=1, verbose_name='Active', choices=[(0, 'Not Active'), (1, 'Active')])),
                ('score', models.FloatField(default=0.0, verbose_name='Score', db_index=True)),
                ('date_created', models.DateField(default=products.models.date_default, verbose_name='Date Created')),
            ],
            options={
                'ordering': ['upc'],
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Attribute',
                'verbose_name_plural': 'Attributes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('value', models.FloatField(null=True, verbose_name='Value', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductAttributeValueUnitMeasure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('representation_sign', models.CharField(max_length=5, verbose_name='Representation sign')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identification', models.CharField(max_length=255, verbose_name='Image identification')),
                ('display_order', models.IntegerField(verbose_name='Display order')),
                ('image', models.ImageField(max_length=255, upload_to=b'products', null=True, verbose_name='Image', blank=True)),
                ('date_uploaded', models.DateField(default=products.models.date_default, verbose_name='Date added')),
            ],
            options={
                'ordering': ['identification'],
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductsCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('full_name', models.CharField(max_length=255, verbose_name='Full name')),
                ('description', models.CharField(max_length=2048, null=True, verbose_name='Name', blank=True)),
                ('image', models.ImageField(max_length=255, upload_to=b'categories', null=True, verbose_name='Image', blank=True)),
                ('date_created', models.DateField(default=products.models.date_default, verbose_name='Date Created')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('child', mptt.fields.TreeForeignKey(related_name=b'sub_categories', verbose_name='Sub categories', blank=True, to='products.ProductsCategory', null=True)),
                ('default_attributes', models.ManyToManyField(related_name=b'category_attributes', null=True, verbose_name=b'Attributes', to='products.ProductAttribute', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price_excl_tax', models.FloatField(default=0.0, verbose_name='Price')),
                ('cost_price', models.FloatField(default=0.0, verbose_name='Cost price')),
                ('price_currency', models.CharField(max_length=12, verbose_name='Currency')),
                ('items_number', models.BigIntegerField(verbose_name='Number in stock', blank=True)),
                ('low_stock_threshold', models.IntegerField(null=True, verbose_name='Low Stock Threshold', blank=True)),
                ('date_created', models.DateField(default=products.models.date_default, verbose_name='Date Created')),
                ('date_updated', models.DateField(default=products.models.date_default, verbose_name='Date Updated')),
                ('product', models.ForeignKey(verbose_name='Product', to='products.Product')),
            ],
            options={
                'verbose_name': 'Stock record',
                'verbose_name_plural': 'Stock records',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Taxes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Tax',
                'verbose_name_plural': 'Taxes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaxesValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField(null=True, verbose_name='Value', blank=True)),
                ('tax_id', models.ForeignKey(blank=True, to='products.Taxes', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='productattributevalue',
            name='unit_measure',
            field=models.ForeignKey(related_name=b'unit_measure', verbose_name='Unit of measure', to='products.ProductAttributeValueUnitMeasure'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='productattribute',
            name='value_id',
            field=models.ForeignKey(verbose_name='Value', blank=True, to='products.ProductAttributeValue', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(to='products.ProductAttribute', null=True, verbose_name='Attributes', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(verbose_name='Category', to='products.ProductsCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ForeignKey(to='products.ProductImage', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='related_products',
            field=models.ForeignKey(related_name=b'related', verbose_name='Related products', blank=True, to='products.Product', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='taxes',
            field=models.ManyToManyField(to='products.Taxes', null=True, verbose_name='Taxes', blank=True),
            preserve_default=True,
        ),
    ]
