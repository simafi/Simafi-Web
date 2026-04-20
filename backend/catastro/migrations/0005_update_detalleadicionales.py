# Generated migration to update DetalleAdicionales model according to SQL schema

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0004_add_empresa_to_edificacion'),
    ]

    operations = [
        # Since this is a significant structural change, we'll use RunSQL to ensure
        # the table structure matches exactly the SQL schema provided.
        # First, let's update the model fields in Django's state
        
        # Step 1: Remove old fields that need to be changed
        migrations.RemoveField(
            model_name='detalleadicionales',
            name='eliminar',
        ),
        
        # Step 2: Add new 'empresa' field
        migrations.AddField(
            model_name='detalleadicionales',
            name='empresa',
            field=models.CharField(db_collation='latin1_swedish_ci', default='', max_length=4, blank=True, verbose_name='Empresa'),
        ),
        
        # Step 3: Change 'clave' from ForeignKey to CharField
        # First remove the ForeignKey constraint
        migrations.AlterField(
            model_name='detalleadicionales',
            name='clave',
            field=models.CharField(db_collation='latin1_swedish_ci', default='', max_length=14, verbose_name='Clave Catastral'),
        ),
        
        # Step 4: Change 'usuario' from ForeignKey to CharField
        migrations.AlterField(
            model_name='detalleadicionales',
            name='usuario',
            field=models.CharField(db_collation='latin1_swedish_ci', default='', max_length=50, blank=True, verbose_name='Usuario'),
        ),
        
        # Step 5: Update 'fechasys' to allow null
        migrations.AlterField(
            model_name='detalleadicionales',
            name='fechasys',
            field=models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha de Registro'),
        ),
        
        # Step 6: Change primary key from 'no' to 'id' if needed
        # Note: This requires careful handling. If 'no' exists, we need to rename it to 'id'
        migrations.RenameField(
            model_name='detalleadicionales',
            old_name='no',
            new_name='id',
        ),
        
        # Step 7: Ensure 'id' is AutoField
        migrations.AlterField(
            model_name='detalleadicionales',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        
        # Step 8: Add index on 'clave' if it doesn't exist
        migrations.AddIndex(
            model_name='detalleadicionales',
            index=models.Index(fields=['clave'], name='detalleadicionales_idx1'),
        ),
    ]

