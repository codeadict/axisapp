# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import axisapp.company.models
import axisapp.storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('help_text', models.CharField(max_length=255, null=True, verbose_name='Help Text', blank=True)),
                ('attrtype', models.PositiveSmallIntegerField(verbose_name='Type', choices=[(10, b'Boolean'), (20, b'Text Short'), (30, b'Text Extended'), (40, b'Integer'), (50, b'Stars'), (60, b'Dropdown'), (70, b'Datetime')])),
                ('required', models.BooleanField(default=False, verbose_name='Required')),
                ('list_show', models.BooleanField(default=False, verbose_name='Show in Lists')),
                ('filter_on', models.BooleanField(default=False, verbose_name='Available In Filters')),
                ('admin_only', models.BooleanField(default=False, help_text='Attributes can only be seen and edited by Admins.', verbose_name='Admin Only')),
                ('dft_int', models.IntegerField(default=0, verbose_name='Integer default')),
                ('dft_str', models.TextField(null=True, verbose_name='String default', blank=True)),
                ('max_stars', models.IntegerField(default=5, verbose_name='Maximum Stars')),
                ('drop_options', models.TextField(help_text='Comma separated list of options on dropdown.', null=True, verbose_name='Dropdown Options', blank=True)),
            ],
            options={
                'ordering': ['pk'],
                'verbose_name': 'Attribute Definition',
                'verbose_name_plural': 'Attribute Definitions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('value_int', models.IntegerField(null=True, verbose_name='Integer value', blank=True)),
                ('value_str', models.TextField(null=True, verbose_name='String value', blank=True)),
                ('value_dt', models.DateTimeField(null=True, verbose_name='Datetime value', blank=True)),
                ('value_dec', models.DecimalField(null=True, verbose_name='Decimal value', max_digits=20, decimal_places=2, blank=True)),
            ],
            options={
                'verbose_name': 'Attribute Value',
                'verbose_name_plural': 'Attribute Values',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.TextField(null=True, verbose_name='Street Address', blank=True)),
                ('town', models.CharField(max_length=255, null=True, verbose_name='Town', blank=True)),
                ('postcode', models.CharField(max_length=20, null=True, verbose_name='Postcode', blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='Branch Name')),
                ('pdf_logo', models.ImageField(storage=axisapp.storage.PublicDebugStorage(), upload_to=axisapp.company.models.branch_report_logo_path, blank=True, help_text='Note: this image is publicly available.', null=True, verbose_name='PDF Logo')),
                ('page_logo', models.ImageField(storage=axisapp.storage.PublicDebugStorage(), upload_to=axisapp.company.models.branch_page_logo_path, blank=True, help_text='Note: this image is publicly available.', null=True, verbose_name='Page Logo')),
                ('datetime_input', models.PositiveSmallIntegerField(default=1, help_text='The first half will be used for date fields, this does not affect how dates are displayed.', verbose_name='Date Input Format', choices=[(1, b'25/7/2014 14:30'), (2, b'25/7/2014 2:30 pm'), (3, b'7/25/2014 14:30'), (4, b'7/25/2014 2:30 pm'), (5, b'2014-07-25 14:30')])),
                ('datetime_output', models.PositiveSmallIntegerField(default=1, help_text='The first half will be used for dates.', verbose_name='Date Output Format', choices=[(1, b'25/7/2014 14:30'), (2, b'25/7/2014 2:30 pm'), (3, b'7/25/2014 14:30'), (4, b'7/25/2014 2:30 pm'), (5, b'2014-07-25 14:30'), (100, b'25 July 2014, Wed 14:30'), (101, b'25 July 2014, Wednesday 14:30')])),
                ('custom_css', models.FileField(help_text='Used to change the appearance of all pages.', upload_to=axisapp.company.models.branch_css_path, null=True, verbose_name='Custom CSS', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'ordering': ['pk'],
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Company Name')),
                ('status', models.CharField(default=b'active', max_length=30, verbose_name='Status', db_index=True, choices=[(b'inactive', 'Not activated yet'), (b'trial', 'Trial Period'), (b'active', 'Active'), (b'suspended', 'Suspended'), (b'terminated', 'Terminated')])),
                ('code', models.SlugField(max_length=40, blank=True, help_text='Used for login URL and files paths,  maybe continue only letters, numbers and underscores, Note: this field cannot be changed after initial setup.', unique=True, verbose_name='Abbreviation')),
                ('custom_css', models.FileField(upload_to=axisapp.company.models.company_css_path, null=True, verbose_name='Custom CSS', blank=True)),
                ('page_logo', models.ImageField(storage=axisapp.storage.PublicDebugStorage(), upload_to=axisapp.company.models.company_page_logo_path, blank=True, help_text='Note: this image is publicly available.', null=True, verbose_name='Page Logo')),
                ('tax_id', models.CharField(max_length=50, null=True, verbose_name='VAT number', blank=True)),
                ('website', models.URLField(help_text='Company Website', null=True, verbose_name='Website', blank=True)),
                ('invoice_due_days', models.IntegerField(default=10, help_text='Days after sending that an invoice is due for payment.', verbose_name='Invoice Due Delay')),
                ('uses_electronic_invoicing', models.BooleanField(default=False, verbose_name='Use Electronic Invoicing?')),
                ('api_access', models.BooleanField(default=False, verbose_name='API access')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('email_sending', models.BooleanField(default=True, help_text='If False all emails from this company will be muted except password resets.', verbose_name='Emails being sent')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('abbreviation', models.CharField(max_length=10, verbose_name='Abbreviation')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('code', models.CharField(unique=True, max_length=5, verbose_name='Code')),
                ('symbol', models.CharField(max_length=5, verbose_name='Symbol')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GeographicRegion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Geographic Region',
                'verbose_name_plural': 'Geographic Regions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('trans_code', models.CharField(default=b'XX', max_length=5, verbose_name='Translation Code', choices=[(b'XX', b'None'), (b'SE', b'Services'), (b'RE', b'Retail')])),
            ],
            options={
                'verbose_name': 'Industry',
                'verbose_name_plural': 'Industries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('file', models.FileField(verbose_name='Template File', editable=False, upload_to=axisapp.company.models.branch_html_path)),
                ('template_type', models.PositiveSmallIntegerField(verbose_name='Type', choices=[(1, 'Email Template'), (2, 'Invoice Template'), (3, 'Site CSS Template')])),
            ],
            options={
                'verbose_name': 'Template',
                'verbose_name_plural': 'Templates',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(storage=axisapp.storage.PublicDebugStorage(), upload_to=axisapp.company.models.company_upload_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(to='company.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
