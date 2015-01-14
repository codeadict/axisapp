# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='uploader',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='template',
            name='company',
            field=models.ForeignKey(related_name='templates', editable=False, to='company.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='geographicregion',
            name='country',
            field=models.ForeignKey(related_name='regions', verbose_name='Country', to='company.Country'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='country',
            name='currency',
            field=models.ForeignKey(related_name='countries', verbose_name='Currency', blank=True, to='company.Currency', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(related_name='companies', to='company.Industry'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='branch',
            name='company',
            field=models.ForeignKey(related_name='branches', verbose_name='Company', to='company.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='branch',
            name='country',
            field=models.ForeignKey(related_name='model_branchs', blank=True, to='company.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='branch',
            name='currency',
            field=models.ForeignKey(related_name='branches', verbose_name='Currency', to='company.Currency'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='definition',
            field=models.ForeignKey(related_name='attrs', to='company.AttributeDefinition'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attributedefinition',
            name='company',
            field=models.ForeignKey(related_name='attributes', editable=False, to='company.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attributedefinition',
            name='content_type',
            field=models.ForeignKey(verbose_name='Apply To', to='contenttypes.ContentType'),
            preserve_default=True,
        ),
    ]
