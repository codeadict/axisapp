# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20150414_0534'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelleAbleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.CharField(max_length=2048, verbose_name='Description', blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('type', models.IntegerField(default=0, verbose_name='Type', choices=[(0, 'Consumable'), (1, 'Service')])),
                ('price_excl_tax', models.FloatField(default=0.0, verbose_name='Price')),
                ('cost_price', models.FloatField(default=0.0, verbose_name='Cost price')),
                ('iva_tax', models.IntegerField(default=2, verbose_name='Taxes', choices=[(0, 'No I.V.A.'), (1, 'I.V.A. 0%'), (2, 'I.V.A. 12%')])),
                ('active', models.IntegerField(default=1, verbose_name='Active', choices=[(0, 'Not Active'), (1, 'Active')])),
                ('score', models.FloatField(default=Decimal('0'), verbose_name='Score', db_index=True)),
                ('date_created', models.DateField(default=products.models.date_default, verbose_name='Date Created')),
                ('attributes', models.ManyToManyField(to='products.ProductAttribute', null=True, verbose_name='Attributes', blank=True)),
                ('category', models.ForeignKey(verbose_name='Category', to='products.ProductsCategory')),
                ('image', models.ForeignKey(to='products.ProductImage', null=True)),
                ('related_items', models.ForeignKey(verbose_name='Related items', blank=True, to='products.Product', null=True)),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='product',
            name='active',
        ),
        migrations.RemoveField(
            model_name='product',
            name='attributes',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='cost_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='iva_tax',
        ),
        migrations.RemoveField(
            model_name='product',
            name='name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price_currency',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price_excl_tax',
        ),
        migrations.RemoveField(
            model_name='product',
            name='related_items',
        ),
        migrations.RemoveField(
            model_name='product',
            name='score',
        ),
        migrations.RemoveField(
            model_name='product',
            name='title',
        ),
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
        migrations.RemoveField(
            model_name='service',
            name='active',
        ),
        migrations.RemoveField(
            model_name='service',
            name='attributes',
        ),
        migrations.RemoveField(
            model_name='service',
            name='category',
        ),
        migrations.RemoveField(
            model_name='service',
            name='cost_price',
        ),
        migrations.RemoveField(
            model_name='service',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='service',
            name='description',
        ),
        migrations.RemoveField(
            model_name='service',
            name='id',
        ),
        migrations.RemoveField(
            model_name='service',
            name='image',
        ),
        migrations.RemoveField(
            model_name='service',
            name='iva_tax',
        ),
        migrations.RemoveField(
            model_name='service',
            name='name',
        ),
        migrations.RemoveField(
            model_name='service',
            name='price_currency',
        ),
        migrations.RemoveField(
            model_name='service',
            name='price_excl_tax',
        ),
        migrations.RemoveField(
            model_name='service',
            name='related_items',
        ),
        migrations.RemoveField(
            model_name='service',
            name='score',
        ),
        migrations.RemoveField(
            model_name='service',
            name='title',
        ),
        migrations.RemoveField(
            model_name='service',
            name='type',
        ),
        migrations.AddField(
            model_name='product',
            name='selleableitem_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=0, serialize=False, to='products.SelleAbleItem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='selleableitem_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=None, serialize=False, to='products.SelleAbleItem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='ice_tax',
            field=models.ForeignKey(verbose_name='Ice', blank=True, to='products.IceTax', null=True),
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='attr',
            field=models.ForeignKey(related_name=b'value', default=None, verbose_name='Attribute', to='products.ProductAttribute'),
        ),
    ]
