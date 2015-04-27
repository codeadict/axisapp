# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hhrr', '0002_auto_20150427_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='coordinates',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, db_column=b'geom', blank=True),
            preserve_default=True,
        ),
    ]
