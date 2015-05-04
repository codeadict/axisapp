# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import swampdragon.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='Datetime')),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('lgn', models.FloatField(verbose_name='Longitude')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Position',
                'verbose_name_plural': 'User positions',
            },
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
    ]
