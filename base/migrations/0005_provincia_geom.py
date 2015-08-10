# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20150313_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='provincia',
            name='geom',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4269, null=True),
            preserve_default=True,
        ),
    ]
