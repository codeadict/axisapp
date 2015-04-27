# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20150412_0507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='value_id',
        ),
        migrations.AddField(
            model_name='productattributevalue',
            name='attr',
            field=models.ForeignKey(related_name=b'attr', default=None, verbose_name='Attribute', to='products.ProductAttribute'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productimage',
            name='identification',
            field=models.CharField(max_length=255, null=True, verbose_name='Image identification', blank=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=b'products', max_length=255, verbose_name='Image'),
        ),
    ]
