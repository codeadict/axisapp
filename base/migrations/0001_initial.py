# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
import base.fields
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255, verbose_name=b'Nombre del poligono')),
                ('agencia', models.CharField(max_length=20, null=True, verbose_name=b'Agencia', blank=True)),
                ('tipo_ruta', models.CharField(max_length=20, null=True, verbose_name=b'Tipo Ruta', blank=True)),
                ('ruta', models.CharField(max_length=20, null=True, verbose_name=b'Ruta', blank=True)),
                ('poligono', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('ruta_geom', django.contrib.gis.db.models.fields.LineStringField(help_text=b'Ruta a seguir por el censador o prevendedor', srid=4326, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Canal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, verbose_name=b'Canal')),
            ],
            options={
                'verbose_name': 'Canal',
                'verbose_name_plural': 'Canales',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Canton',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=45, verbose_name=b'Nombre del Canton')),
            ],
            options={
                'verbose_name_plural': 'Cantones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255, verbose_name=b'Categorizacion')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmpresaActivos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255, verbose_name=b'Nombre Empresa')),
            ],
            options={
                'verbose_name': 'Empresa Activos de Mercado',
                'verbose_name_plural': 'Empresas Activos de Mercado',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmpresaVisitas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255, verbose_name=b'Nombre Empresa')),
            ],
            options={
                'verbose_name': 'Empresa Visita Cliente',
                'verbose_name_plural': 'Empresas Visitas Clientes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Envase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255, verbose_name=b'Tipo de Envase')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('colour', base.fields.ColorField(default=b'#ADF', max_length=20, verbose_name='Color')),
                ('applicable_partner_types', models.ManyToManyField(related_name=b'labels', verbose_name='Aplicable a', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Etiqueta',
                'verbose_name_plural': 'Etiquetas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MacroCanal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=150, verbose_name=b'Macro Canal')),
            ],
            options={
                'verbose_name': 'Macro Canal',
                'verbose_name_plural': 'Macro Canales',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MacroCat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=150, verbose_name=b'Macro Categoria')),
            ],
            options={
                'verbose_name': 'Macro Categoria',
                'verbose_name_plural': 'Macro Categorias',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('marca', models.CharField(max_length=255, verbose_name=b'Marca')),
                ('categoria', models.ForeignKey(verbose_name=b'Categorizacion', to='base.Categoria')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OcasionConsumo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, verbose_name=b'Ocasion de Consumo')),
                ('macrocanal', models.ForeignKey(to='base.MacroCanal')),
            ],
            options={
                'verbose_name': 'Ocasion de Consumo',
                'verbose_name_plural': 'Ocasiones de Consumo',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parroquia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=45, verbose_name=b'Nombre de la Parroquia')),
                ('canton', models.ForeignKey(to='base.Canton')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('partner_type', models.CharField(verbose_name='Tipo de Asociado', max_length=20, editable=False, db_index=True)),
                ('priority', models.PositiveSmallIntegerField(default=0, verbose_name='Orden de Prioridad', editable=False, db_index=True)),
            ],
            options={
                'ordering': ['-priority'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Presentacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, verbose_name=b'Presentacion')),
            ],
            options={
                'verbose_name': 'Presentacion',
                'verbose_name_plural': 'Presentaciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(default=b'', max_length=10, verbose_name=b'Codigo de Provincia')),
                ('nombre', models.CharField(max_length=45, verbose_name=b'Nombre de la Provincia')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubCanal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255, verbose_name=b'Sub Canal')),
                ('canal', models.ForeignKey(verbose_name=b'Canal', to='base.Canal')),
            ],
            options={
                'verbose_name': 'SubCanal',
                'verbose_name_plural': 'SubCanales',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='label',
            name='partners',
            field=models.ManyToManyField(related_name=b'labels', verbose_name='Asociados', to='base.Partner', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categoria',
            name='macro',
            field=models.ForeignKey(verbose_name=b'Macro Categorizacion', to='base.MacroCat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='canton',
            name='provincia',
            field=models.ForeignKey(to='base.Provincia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='canal',
            name='ocasion',
            field=models.ForeignKey(verbose_name=b'Ocacion de Consumo', to='base.OcasionConsumo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='canton',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'provincia', chained_field=b'provincia', auto_choose=True, to='base.Canton'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='censador',
            field=models.ForeignKey(related_name=b'areas_censador', verbose_name=b'Censador Asignado', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='parroquia',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'canton', to='base.Parroquia', chained_field=b'canton'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='prevendedor',
            field=models.ForeignKey(related_name=b'areas_prevendedor', verbose_name=b'Prevendedor Asignado', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='provincia',
            field=models.ForeignKey(to='base.Provincia'),
            preserve_default=True,
        ),
    ]
