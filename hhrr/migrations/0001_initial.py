# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields
import base.fields
import mptt.fields
import hhrr.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('institution', models.CharField(max_length=255, verbose_name='Institution Name')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='Institution Name')),
                ('start_date', models.DateField(default=hhrr.models.date_default, verbose_name='Start date')),
                ('graduation_date', models.DateField(default=hhrr.models.date_default, verbose_name='Graduation date')),
                ('instruction_level', models.IntegerField(default=0, verbose_name='Level', choices=[(0, 'No instruction'), (1, 'Basic school'), (2, 'Primary'), (3, 'Secondary'), (4, 'Bachelor'), (5, 'Fourth'), (6, 'Senior Technician'), (7, 'Technics'), (8, 'Third')])),
                ('degree', models.CharField(max_length=255, verbose_name='Degree')),
                ('is_finished', models.BooleanField(default=False, verbose_name='Finished?')),
                ('last_finished_semester', models.IntegerField(default=0, verbose_name='Last finished semester')),
            ],
            options={
                'ordering': ['institution'],
                'verbose_name': 'Studied education',
                'verbose_name_plural': 'Studied educations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EducationArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Area name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('partner_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='base.Partner')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last Name')),
                ('id_type', models.IntegerField(default=2, verbose_name='Id type', choices=[(0, 'R.U.C.'), (1, 'Passport'), (2, 'Id')])),
                ('identification', models.CharField(max_length=20, verbose_name='ID number')),
                ('photo', models.ImageField(upload_to=b'', verbose_name='Image')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('county', models.CharField(max_length=255, verbose_name='County')),
                ('city', models.CharField(max_length=255, verbose_name='City')),
                ('postcode', models.CharField(max_length=10, verbose_name='Postal Code')),
                ('nationality', django_countries.fields.CountryField(max_length=2, verbose_name='Nationality')),
                ('blood_type', models.IntegerField(default=0, verbose_name='Blood type', choices=[(0, 'Type O'), (1, 'Type O+'), (2, 'Type O-'), (3, 'Type a'), (4, 'Type A-'), (5, 'Type A+'), (6, 'Type B'), (7, 'Type B+'), (8, 'Type B-'), (9, 'Type AB'), (10, 'Type AB+'), (11, 'Type AB-')])),
                ('handicapped', models.BooleanField(default=0, verbose_name='Is handicapped?')),
                ('handicap_percent', base.fields.PercentageField(default=0, verbose_name='Handicap percent', max_digits=6, decimal_places=3)),
                ('handicap_type', models.CharField(max_length=255, verbose_name='Handicap type')),
                ('handicap_card_number', models.CharField(max_length=255, verbose_name='Handicap card number')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'If phone from different country                                          than company please, provide international format +prefix-number', max_length=128, verbose_name='Phone number')),
                ('cellphone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'If cellphone from different                                          country than company please, provide international format +prefix-number', max_length=128, verbose_name='Cellphone number')),
                ('email', models.EmailField(max_length=255, verbose_name='Email')),
                ('skype', models.CharField(max_length=255, verbose_name='Skype user')),
                ('marital_status', models.IntegerField(default=0, verbose_name='Marital status', choices=[(0, 'Single'), (1, 'Married'), (2, 'Widowed'), (3, 'Divorces'), (4, 'Union free')])),
                ('sex', models.IntegerField(default=-1, verbose_name='Gender', choices=[(0, 'Male'), (1, 'Female')])),
                ('birthday', models.DateField(default=hhrr.models.date_default, verbose_name='Birthday')),
                ('emergency_person', models.CharField(max_length=255, verbose_name='Name to call at emergency')),
                ('emergency_phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='Phone number to call at emergency')),
                ('maintain_reserve_funds', models.BooleanField(default=False, verbose_name='Maintain reserve funds?')),
                ('status', models.IntegerField(default=0, verbose_name='Status', choices=[(0, 'Inactive'), (1, 'Active'), (3, 'Settled')])),
                ('ethnic_race', models.IntegerField(default=0, verbose_name='Ethnic race', choices=[(4, 'Asian'), (1, 'Black'), (0, 'White'), (2, 'Mixed'), (5, 'Other')])),
                ('canton', models.ForeignKey(verbose_name='Canton', to='base.Canton')),
            ],
            options={
                'ordering': ['last_name'],
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
            bases=('base.partner',),
        ),
        migrations.CreateModel(
            name='EmploymentHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(max_length=255, verbose_name='Company Name')),
                ('position', models.CharField(max_length=255, verbose_name='Position')),
                ('date_in', models.DateField(default=hhrr.models.date_default, verbose_name='Date hired')),
                ('date_out', models.DateField(default=hhrr.models.date_default, verbose_name='Date leaving')),
                ('out_reason', models.CharField(max_length=255, verbose_name='Reason of leaving')),
            ],
            options={
                'ordering': ['date_out'],
                'verbose_name': 'Employment history',
                'verbose_name_plural': 'Employment history',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnterpriseDepartment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Department name')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('manager', models.ForeignKey(verbose_name='Department Manager', to='hhrr.Employee')),
                ('parent', mptt.fields.TreeForeignKey(related_name=b'sub_department', blank=True, to='hhrr.EnterpriseDepartment', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FamilyDependant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name')),
                ('birthday', models.DateField(default=hhrr.models.date_default, verbose_name='Birthday')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'If phone from different country                                          than company, please provide international format +prefix-number', max_length=128, verbose_name='Phone Number')),
                ('handicapped', models.BooleanField(default=False, verbose_name='Handicapped')),
                ('have_insurance', models.BooleanField(default=False, verbose_name='Insurance')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Family dependant',
                'verbose_name_plural': 'Family dependants',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FamilyRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
                ('code_mrl', models.CharField(max_length=255, verbose_name='Code MRL')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Family relation',
                'verbose_name_plural': 'Family relations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.PositiveIntegerField(default=19, verbose_name='Language Name', choices=[(0, (b'af', b'Afrikaans')), (1, (b'ar', b'Arabic')), (2, (b'ast', b'Asturian')), (3, (b'az', b'Azerbaijani')), (4, (b'bg', b'Bulgarian')), (5, (b'be', b'Belarusian')), (6, (b'bn', b'Bengali')), (7, (b'br', b'Breton')), (8, (b'bs', b'Bosnian')), (9, (b'ca', b'Catalan')), (10, (b'cs', b'Czech')), (11, (b'cy', b'Welsh')), (12, (b'da', b'Danish')), (13, (b'de', b'German')), (14, (b'el', b'Greek')), (15, (b'en', b'English')), (16, (b'en-au', b'Australian English')), (17, (b'en-gb', b'British English')), (18, (b'eo', b'Esperanto')), (19, (b'es', b'Spanish')), (20, (b'es-ar', b'Argentinian Spanish')), (21, (b'es-mx', b'Mexican Spanish')), (22, (b'es-ni', b'Nicaraguan Spanish')), (23, (b'es-ve', b'Venezuelan Spanish')), (24, (b'et', b'Estonian')), (25, (b'eu', b'Basque')), (26, (b'fa', b'Persian')), (27, (b'fi', b'Finnish')), (28, (b'fr', b'French')), (29, (b'fy', b'Frisian')), (30, (b'ga', b'Irish')), (31, (b'gl', b'Galician')), (32, (b'he', b'Hebrew')), (33, (b'hi', b'Hindi')), (34, (b'hr', b'Croatian')), (35, (b'hu', b'Hungarian')), (36, (b'ia', b'Interlingua')), (37, (b'id', b'Indonesian')), (38, (b'io', b'Ido')), (39, (b'is', b'Icelandic')), (40, (b'it', b'Italian')), (41, (b'ja', b'Japanese')), (42, (b'ka', b'Georgian')), (43, (b'kk', b'Kazakh')), (44, (b'km', b'Khmer')), (45, (b'kn', b'Kannada')), (46, (b'ko', b'Korean')), (47, (b'lb', b'Luxembourgish')), (48, (b'lt', b'Lithuanian')), (49, (b'lv', b'Latvian')), (50, (b'mk', b'Macedonian')), (51, (b'ml', b'Malayalam')), (52, (b'mn', b'Mongolian')), (53, (b'mr', b'Marathi')), (54, (b'my', b'Burmese')), (55, (b'nb', b'Norwegian Bokmal')), (56, (b'ne', b'Nepali')), (57, (b'nl', b'Dutch')), (58, (b'nn', b'Norwegian Nynorsk')), (59, (b'os', b'Ossetic')), (60, (b'pa', b'Punjabi')), (61, (b'pl', b'Polish')), (62, (b'pt', b'Portuguese')), (63, (b'pt-br', b'Brazilian Portuguese')), (64, (b'ro', b'Romanian')), (65, (b'ru', b'Russian')), (66, (b'sk', b'Slovak')), (67, (b'sl', b'Slovenian')), (68, (b'sq', b'Albanian')), (69, (b'sr', b'Serbian')), (70, (b'sr-latn', b'Serbian Latin')), (71, (b'sv', b'Swedish')), (72, (b'sw', b'Swahili')), (73, (b'ta', b'Tamil')), (74, (b'te', b'Telugu')), (75, (b'th', b'Thai')), (76, (b'tr', b'Turkish')), (77, (b'tt', b'Tatar')), (78, (b'udm', b'Udmurt')), (79, (b'uk', b'Ukrainian')), (80, (b'ur', b'Urdu')), (81, (b'vi', b'Vietnamese')), (82, (b'zh-cn', b'Simplified Chinese')), (83, (b'zh-hans', b'Simplified Chinese')), (84, (b'zh-hant', b'Traditional Chinese')), (85, (b'zh-tw', b'Traditional Chinese'))])),
                ('speak', models.PositiveIntegerField(default=0, verbose_name='Speak skills', choices=[(0, 'Low'), (1, 'Intermediate'), (2, 'High'), (3, 'Native')])),
                ('write', models.PositiveIntegerField(default=0, verbose_name='Write skills', choices=[(0, 'Low'), (1, 'Intermediate'), (2, 'High'), (3, 'Native')])),
                ('read', models.PositiveIntegerField(default=0, verbose_name='Read skills', choices=[(0, 'Low'), (1, 'Intermediate'), (2, 'High'), (3, 'Native')])),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='familydependant',
            name='relationship',
            field=models.ForeignKey(verbose_name='Relation ship', to='hhrr.FamilyRelation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(related_name=b'employees', verbose_name='Department', to='hhrr.EnterpriseDepartment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='education',
            field=models.ForeignKey(related_name=b'education', verbose_name='Education', to='hhrr.Education'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='employment_history',
            field=models.ForeignKey(related_name=b'history', verbose_name='Employment history', to='hhrr.EmploymentHistory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='family_dependants',
            field=models.ForeignKey(related_name=b'family_sdependants', verbose_name='Family dependants', to='hhrr.FamilyDependant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='language_skill',
            field=models.ForeignKey(related_name=b'languages', verbose_name='Language skills', to='hhrr.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='parish',
            field=models.ForeignKey(verbose_name='Parish', to='base.Parroquia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='province',
            field=models.ForeignKey(verbose_name='Province', to='base.Provincia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='education',
            name='education_area',
            field=models.ForeignKey(verbose_name='Education Area', to='hhrr.EducationArea'),
            preserve_default=True,
        ),
    ]
