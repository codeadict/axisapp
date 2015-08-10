# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20150809_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provincia',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True),
        ),
    ]
