from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0015_add_unique_constraint_confi_tipologia'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetEspecificacion',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('empresa', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=4, verbose_name='Empresa')),
                ('clave', models.CharField(db_collation='latin1_swedish_ci', default='0', max_length=14, verbose_name='Clave Catastral')),
                ('edifino', models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='No. Edificación')),
                ('piso', models.DecimalField(decimal_places=0, default=0, max_digits=2, verbose_name='Piso')),
                ('pisoestruc', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Piso Estructura')),
                ('pisoacabado', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Piso Acabado')),
                ('pisocalidad', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Piso Calidad')),
                ('paredextestruc', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Pared Ext. Estructura')),
                ('paredextacabado', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Pared Ext. Acabado')),
                ('paredextcalidad', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Pared Ext. Calidad')),
                ('paredextpintura', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Pared Ext. Pintura')),
                ('techotipo', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Techo Tipo')),
                ('techoarteson', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Techo Artesón')),
                ('techoacabado', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Techo Acabado')),
                ('techocalidad', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Techo Calidad')),
                ('paredintestruc', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Pared Int. Estructura')),
                ('paredintacabado', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Pared Int. Acabado')),
                ('paredintacalidad', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Pared Int. Calidad')),
                ('paredintpintura', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Pared Int. Pintura')),
                ('cieloestruc', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Cielo Estructura')),
                ('cieloacabado', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Cielo Acabado')),
                ('cielocalidad', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Cielo Calidad')),
                ('electrialumbrado', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Eléctrica Alumbrado')),
                ('electrisalida', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Eléctrica Salida')),
                ('electricalidad', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Eléctrica Calidad')),
                ('inodorocal', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Inodoro Calidad')),
                ('lavamanocal', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Lavamanos Calidad')),
                ('duchacal', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Ducha Calidad')),
                ('lavatrastocal', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Lavatrapos Calidad')),
                ('lavanderocal', models.DecimalField(decimal_places=0, default=0, max_digits=1, verbose_name='Lavandero Calidad')),
                ('puerta1', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Puerta 1')),
                ('puerta2', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Puerta 2')),
                ('puerta3', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Puerta 3')),
                ('puerta4', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Puerta 4')),
                ('ventana1', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Ventana 1')),
                ('ventana2', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Ventana 2')),
                ('ventana3', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Ventana 3')),
                ('ventana4', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Ventana 4')),
                ('closet1', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Closet 1')),
                ('closet2', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Closet 2')),
                ('closet3', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Closet 3')),
                ('closet4', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Closet 4')),
                ('gabinete1', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Gabinete 1')),
                ('gabinete2', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Gabinete 2')),
                ('gabinete3', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Gabinete 3')),
                ('gabinete4', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Gabinete 4')),
                ('usuario', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Usuario')),
                ('fechasys', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Fecha de Registro')),
            ],
            options={
                'verbose_name': 'Detalle de Especificación',
                'verbose_name_plural': 'Detalles de Especificaciones',
                'db_table': 'detespecificacion',
            },
        ),
        migrations.AddIndex(
            model_name='detespecificacion',
            index=models.Index(fields=['empresa', 'clave', 'edifino', 'piso'], name='detespecificacion_idx1'),
        ),
    ]

