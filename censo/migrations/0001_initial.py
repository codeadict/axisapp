# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivosMercado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('p', models.PositiveIntegerField(verbose_name=b'P')),
                ('m', models.PositiveIntegerField(verbose_name=b'M')),
                ('g', models.PositiveIntegerField(verbose_name=b'G')),
                ('congelador', models.BooleanField(default=False, verbose_name=b'Cong.')),
                ('exhibidor', models.BooleanField(default=False, verbose_name=b'Exhib.')),
                ('estante', models.BooleanField(default=False, verbose_name=b'Estan.')),
                ('rotulo', models.BooleanField(default=False, verbose_name=b'Rotu.')),
                ('mesas', models.BooleanField(default=False, verbose_name=b'Mesas')),
                ('sillas', models.BooleanField(default=False, verbose_name=b'Sillas')),
            ],
            options={
                'verbose_name': 'Activo de Mercado',
                'verbose_name_plural': 'Activos de Mercado',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('partner_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='base.Partner')),
                ('nombres', models.CharField(max_length=255, verbose_name=b'Nombres')),
                ('apellidos', models.CharField(max_length=255, verbose_name=b'Apellidos')),
                ('tipo_id', models.PositiveIntegerField(default=0, verbose_name=b'Tipo ID', choices=[(0, b'CEDULA'), (1, b'RUC'), (2, b'PASAPORTE')])),
                ('identif', models.CharField(max_length=13, verbose_name=b'Identificacion')),
                ('fecha_verificado_sri', models.DateField(null=True, verbose_name=b'Fecha Verificacion SRi', blank=True)),
                ('email', models.EmailField(max_length=150, null=True, verbose_name=b'Email', blank=True)),
                ('celular', models.CharField(max_length=10, null=True, verbose_name=b'Celular', blank=True)),
                ('convencional', models.CharField(help_text=b'Poner con 9 numeros, Ejemplo: 021234567', max_length=9, null=True, verbose_name=b'Convencional', blank=True)),
                ('cumple', models.DateField(verbose_name=b'Cumpleanos')),
                ('administrador', models.CharField(max_length=255, null=True, verbose_name=b'Administrador', blank=True)),
                ('foto', models.ImageField(upload_to=b'fotos/clientes/', null=True, verbose_name='Foto', blank=True)),
                ('direccion', models.CharField(max_length=255, null=True, verbose_name=b'Direccion Local', blank=True)),
                ('tipo_local', models.PositiveIntegerField(default=0, verbose_name=b'Local', choices=[(0, b'ARRENDADO'), (1, b'PROPIO'), (2, b'COMODATO')])),
                ('especial', models.BooleanField(default=False, verbose_name=b'Contribuyente Especial')),
                ('estatal', models.BooleanField(default=False, verbose_name=b'Institucion Estado')),
                ('persona_compras', models.CharField(max_length=255, null=True, verbose_name=b'Persona aut. a comprar', blank=True)),
                ('razon_social', models.CharField(max_length=255, null=True, verbose_name=b'Razon Social', blank=True)),
                ('nombre_comercial', models.CharField(max_length=255, null=True, verbose_name=b'Nombre Comercial', blank=True)),
                ('website', models.URLField(max_length=255, null=True, verbose_name='Pagina Web', blank=True)),
                ('medida_frente', models.FloatField(null=True, verbose_name=b'Medida Frente', blank=True)),
                ('medida_fondo', models.FloatField(null=True, verbose_name=b'Medida Fondo', blank=True)),
                ('horario_desde', models.TimeField(help_text=b'Formato 24 horas: 00:00', verbose_name=b'Desde')),
                ('horario_hasta', models.TimeField(help_text=b'Formato 24 horas: 00:00', verbose_name=b'Hasta')),
                ('abc_compras', models.CharField(blank=True, max_length=1, null=True, verbose_name=b'ABC Compras', choices=[(b'a', b'A'), (b'b', b'B'), (b'c', b'C')])),
                ('abc_industrias', models.CharField(blank=True, max_length=1, null=True, verbose_name=b'ABC Industrias', choices=[(b'a', b'A'), (b'b', b'B'), (b'c', b'C')])),
                ('fecha_ingreso', models.DateField(null=True, verbose_name=b'Fecha Ingreso', blank=True)),
                ('fecha_retiro', models.DateField(null=True, verbose_name=b'Fecha Retiro', blank=True)),
                ('codigo', models.CharField(max_length=20, null=True, verbose_name=b'Codigo', blank=True)),
                ('barrio', models.CharField(max_length=255, null=True, verbose_name=b'Barrio', blank=True)),
                ('sector', models.CharField(max_length=255, null=True, verbose_name=b'Sector', blank=True)),
                ('coordenadas', django.contrib.gis.db.models.fields.PointField(srid=4326, db_column=b'geom')),
                ('frecuencia', models.CharField(max_length=20, null=True, verbose_name=b'Frecuencia', blank=True)),
                ('secuencia', models.CharField(max_length=20, null=True, verbose_name=b'Secuencia', blank=True)),
                ('estado', models.PositiveSmallIntegerField(default=0, verbose_name=b'Estado', choices=[(0, b'ACTIVO'), (1, b'PASIVO'), (2, b'ELIMINADO')])),
                ('foto_local', models.ImageField(upload_to=b'fotos/locales/', null=True, verbose_name='Foto del Local', blank=True)),
                ('canal', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'ocasion', chained_field=b'ocasion_consumo', blank=True, to='base.Canal', null=True)),
                ('macro_canal', models.ForeignKey(verbose_name=b'Macro Canal', blank=True, to='base.MacroCanal', null=True)),
                ('ocasion_consumo', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'macrocanal', chained_field=b'macro_canal', blank=True, to='base.OcasionConsumo', null=True)),
                ('subcanal', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'canal', chained_field=b'canal', blank=True, to='base.SubCanal', null=True)),
            ],
            options={
            },
            bases=('base.partner',),
        ),
        migrations.CreateModel(
            name='InvProductos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('categ', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, to='base.Categoria', chained_model_field=b'macro', chained_field=b'macro_categ', verbose_name=b'Categorizacion')),
                ('cliente', models.ForeignKey(verbose_name=b'Cliente', to='censo.Cliente')),
                ('envase', models.ForeignKey(verbose_name=b'Envase', to='base.Envase')),
                ('macro_categ', models.ForeignKey(verbose_name=b'Macro Cat.', to='base.MacroCat')),
                ('marca', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, to='base.Marca', chained_model_field=b'categoria', chained_field=b'categ', verbose_name=b'Marca')),
                ('presentacion', models.ForeignKey(verbose_name=b'Presentacion', to='base.Presentacion')),
            ],
            options={
                'verbose_name': 'Inventaario Producto',
                'verbose_name_plural': 'Inventario Productos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lunes', models.BooleanField(default=False, verbose_name=b'Lun')),
                ('martes', models.BooleanField(default=False, verbose_name=b'Mar')),
                ('miercoles', models.BooleanField(default=False, verbose_name=b'Mie')),
                ('jueves', models.BooleanField(default=False, verbose_name=b'Jue')),
                ('viernes', models.BooleanField(default=False, verbose_name=b'Vie')),
                ('sabado', models.BooleanField(default=False, verbose_name=b'Sab')),
                ('domingo', models.BooleanField(default=False, verbose_name=b'Dom')),
                ('preventa', models.BooleanField(default=False, verbose_name=b'Preventa')),
                ('autoventa', models.BooleanField(default=False, verbose_name=b'Autoventa')),
                ('televenta', models.BooleanField(default=False, verbose_name=b'Televenta')),
                ('cliente', models.ForeignKey(default=0, verbose_name=b'Cliente', to='censo.Cliente')),
                ('empresa', models.ForeignKey(verbose_name=b'Competencia', to='base.EmpresaVisitas')),
            ],
            options={
                'verbose_name': 'Visita del Cliente',
                'verbose_name_plural': 'Visitas del Cliente',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activosmercado',
            name='cliente',
            field=models.ForeignKey(verbose_name=b'Cliente', to='censo.Cliente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activosmercado',
            name='empresa',
            field=models.ForeignKey(verbose_name=b'Competencia', to='base.EmpresaActivos'),
            preserve_default=True,
        ),
    ]
