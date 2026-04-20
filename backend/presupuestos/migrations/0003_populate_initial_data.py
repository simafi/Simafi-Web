from django.db import migrations

def populate_initial_data(apps, schema_editor):
    Fondo = apps.get_model('presupuestos', 'Fondo')
    CuentaPresupuestaria = apps.get_model('presupuestos', 'CuentaPresupuestaria')
    
    empresa_default = '01' # O la que se use por defecto en el sistema
    
    # 1. Poblar Fondos
    fondos_data = [
        ('1', 'Fondos Propios'),
        ('2', 'Transferencias'),
        ('3', 'Otros'),
        ('4', 'ERP26'),
        ('5', '15 % Salud y Educ.'),
        ('6', '10% Funcionamiento'),
    ]
    
    for cod, nom in fondos_data:
        Fondo.objects.get_or_create(
            empresa=empresa_default,
            codigo=cod,
            defaults={'nombre': nom}
        )
        
    # 2. Poblar Grupos (Cuentas Título)
    # Ingresos
    ingresos_titulos = [
        ('1', 'INGRESOS CORRIENTES'),
        ('2', 'SUBSIDIOS'),
    ]
    for cod, nom in ingresos_titulos:
        CuentaPresupuestaria.objects.get_or_create(
            empresa=empresa_default,
            codigo=cod,
            tipo_presupuesto='INGRESO',
            defaults={
                'nombre': nom,
                'tipo_cuenta': 'TITULO',
                'nivel': 1
            }
        )
        
    # Egresos
    egresos_titulos = [
        ('5', 'SERVICIO DE LA DEUDA Y DISMINUCION DE OTROS PASIVO'),
        ('2.1', 'Pasajes Viaticos y Otros Gastos de Viaje'), # Ejemplo de código
    ]
    for cod, nom in egresos_titulos:
        CuentaPresupuestaria.objects.get_or_create(
            empresa=empresa_default,
            codigo=cod,
            tipo_presupuesto='EGRESO',
            defaults={
                'nombre': nom,
                'tipo_cuenta': 'TITULO',
                'nivel': 1
            }
        )

def reverse_populate(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('presupuestos', '0002_remove_cuentapresupuestaria_tipo_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_initial_data, reverse_populate),
    ]
