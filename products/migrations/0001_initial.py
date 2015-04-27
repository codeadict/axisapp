# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from decimal import Decimal
import products.models


class Migration(migrations.Migration):

    dependencies = [
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
                ('attr', models.ForeignKey(related_name=b'value', default=None, verbose_name='Attribute', to='products.ProductAttribute')),
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
                ('identification', models.CharField(max_length=255, null=True, verbose_name='Image identification', blank=True)),
                ('display_order', models.IntegerField(verbose_name='Display order')),
                ('image', models.ImageField(upload_to=b'products', max_length=255, verbose_name='Image')),
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
                ('default_attributes', models.ManyToManyField(related_name=b'category_attributes', null=True, verbose_name=b'Attributes', to='products.ProductAttribute', blank=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name=b'sub_categories', verbose_name='Sub categories', blank=True, to='products.ProductsCategory', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SelleAbleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.CharField(max_length=2048, verbose_name='Description', blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('type', models.CharField(verbose_name='Type', max_length=50, editable=False, db_index=True)),
                ('price_excl_tax', models.FloatField(default=0.0, verbose_name='Price')),
                ('cost_price', models.FloatField(default=0.0, verbose_name='Cost price')),
                ('iva_tax', models.IntegerField(default=2, verbose_name='Taxes', choices=[(0, 'No I.V.A.'), (1, 'I.V.A. 0%'), (2, 'I.V.A. 12%')])),
                ('active', models.IntegerField(default=1, verbose_name='Active', choices=[(0, 'Not Active'), (1, 'Active')])),
                ('score', models.FloatField(default=Decimal('0'), verbose_name='Score', db_index=True)),
                ('date_created', models.DateField(default=products.models.date_default, verbose_name='Date Created')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('selleableitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='products.SelleAbleItem')),
                ('upc', models.CharField(null=True, max_length=64, blank=True, help_text='Universal Product Code (UPC)', unique=True, verbose_name='UPC')),
                ('items_stock_number', models.BigIntegerField(default=0, verbose_name='Number in stock', blank=True)),
                ('low_stock_threshold', models.IntegerField(null=True, verbose_name='Low Stock Threshold', blank=True)),
                ('ice_tax', models.ForeignKey(verbose_name='Ice', blank=True, to='products.IceTax', null=True)),
            ],
            options={
                'ordering': ['upc'],
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=('products.selleableitem',),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('selleableitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='products.SelleAbleItem')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=('products.selleableitem',),
        ),
        migrations.AddField(
            model_name='selleableitem',
            name='attributes',
            field=models.ManyToManyField(to='products.ProductAttribute', null=True, verbose_name='Attributes', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='selleableitem',
            name='category',
            field=models.ForeignKey(verbose_name='Category', to='products.ProductsCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='selleableitem',
            name='image',
            field=models.ForeignKey(to='products.ProductImage', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='selleableitem',
            name='related_items',
            field=models.ForeignKey(verbose_name='Related items', blank=True, to='products.Product', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='productattributevalue',
            name='unit_measure',
            field=models.ForeignKey(related_name=b'unit_measure', verbose_name='Unit of measure', to='products.ProductAttributeValueUnitMeasure'),
            preserve_default=True,
        ),
    ]
