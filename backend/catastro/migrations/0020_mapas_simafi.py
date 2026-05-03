# Mapas Simafi: proyectos, capas y elementos GeoJSON (catastro_mapa_*)

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0019_add_index_empresa_clave_tasas_municipales'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapaProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.CharField(db_index=True, max_length=4, verbose_name='Empresa / municipio')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre del mapa')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
                (
                    'srid',
                    models.PositiveIntegerField(
                        default=4326,
                        help_text='Sistema de coordenadas de referencia, ej. 4326 WGS84',
                        verbose_name='SRID (EPSG)',
                    ),
                ),
                ('usuario_creacion', models.CharField(blank=True, max_length=80, verbose_name='Usuario')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Proyecto de mapa',
                'verbose_name_plural': 'Proyectos de mapas',
                'db_table': 'catastro_mapa_proyecto',
                'ordering': ['-actualizado_en', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='MapaCapa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, verbose_name='Nombre de la capa')),
                ('orden', models.PositiveSmallIntegerField(default=0, verbose_name='Orden')),
                ('color_linea', models.CharField(default='#2563eb', max_length=32, verbose_name='Color línea')),
                ('color_relleno', models.CharField(default='#2563eb', max_length=32, verbose_name='Color relleno')),
                ('opacidad_relleno', models.FloatField(default=0.25, verbose_name='Opacidad relleno (0–1)')),
                ('visible', models.BooleanField(default=True, verbose_name='Visible')),
                (
                    'proyecto',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='capas',
                        to='catastro.mapaproyecto',
                        verbose_name='Proyecto',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Capa de mapa',
                'verbose_name_plural': 'Capas de mapa',
                'db_table': 'catastro_mapa_capa',
                'ordering': ['orden', 'id'],
            },
        ),
        migrations.CreateModel(
            name='MapaElemento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta', models.CharField(blank=True, max_length=200, verbose_name='Etiqueta')),
                ('geometria', models.JSONField(verbose_name='Geometría (GeoJSON)')),
                ('propiedades', models.JSONField(blank=True, default=dict, verbose_name='Propiedades')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                (
                    'capa',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='elementos',
                        to='catastro.mapacapa',
                        verbose_name='Capa',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Elemento del mapa',
                'verbose_name_plural': 'Elementos del mapa',
                'db_table': 'catastro_mapa_elemento',
            },
        ),
        migrations.AddIndex(
            model_name='mapaproyecto',
            index=models.Index(fields=['empresa', 'activo'], name='catastro_mapa_proj_emp_act'),
        ),
        migrations.AddIndex(
            model_name='mapaelemento',
            index=models.Index(fields=['capa'], name='catastro_mapa_elem_capa'),
        ),
    ]
