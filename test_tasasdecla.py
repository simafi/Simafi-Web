"""
Script de prueba para verificar la consulta a la tabla tasasdecla
"""
import os
import sys
import django

# Configurar el path
sys.path.insert(0, r'C:\simafiweb\venv\Scripts')
sys.path.insert(0, r'C:\simafiweb\venv\Scripts\tributario')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

# Importar modelos
from tributario_app.models import TasasDecla, Rubro

print("=" * 80)
print("TEST DE CONSULTA A TABLA TASASDECLA")
print("=" * 80)

# Parámetros de prueba
empresa = '0301'
rtm = '114-03-23'
expe = '1151'

print(f"\n📋 Parámetros de búsqueda:")
print(f"   Empresa: {empresa}")
print(f"   RTM: {rtm}")
print(f"   EXPE: {expe}")
print("-" * 80)

# Test 1: Verificar si hay registros en general en la tabla
print("\n🔍 Test 1: Verificar todos los registros en tasasdecla")
try:
    total_registros = TasasDecla.objects.all().count()
    print(f"   ✅ Total de registros en tasasdecla: {total_registros}")
    
    if total_registros > 0:
        print("\n   📊 Primeros 5 registros:")
        for i, tasa in enumerate(TasasDecla.objects.all()[:5], 1):
            print(f"   {i}. empresa={tasa.empresa}, rtm={tasa.rtm}, expe={tasa.expe}, ano={tasa.ano}, rubro={tasa.rubro}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Buscar por RTM solamente
print("\n🔍 Test 2: Buscar por RTM solamente")
try:
    registros_rtm = TasasDecla.objects.filter(rtm=rtm)
    print(f"   Total encontrados: {registros_rtm.count()}")
    for tasa in registros_rtm[:3]:
        print(f"   - empresa={tasa.empresa}, rtm={tasa.rtm}, expe={tasa.expe}, ano={tasa.ano}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Buscar por RTM y EXPE
print("\n🔍 Test 3: Buscar por RTM y EXPE")
try:
    registros_rtm_expe = TasasDecla.objects.filter(rtm=rtm, expe=expe)
    print(f"   Total encontrados: {registros_rtm_expe.count()}")
    for tasa in registros_rtm_expe[:3]:
        print(f"   - empresa={tasa.empresa}, rtm={tasa.rtm}, expe={tasa.expe}, ano={tasa.ano}, rubro={tasa.rubro}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Buscar por empresa, RTM y EXPE (como en la vista)
print("\n🔍 Test 4: Buscar por EMPRESA, RTM y EXPE")
try:
    registros_completo = TasasDecla.objects.filter(
        empresa=empresa,
        rtm=rtm,
        expe=expe
    )
    print(f"   Total encontrados: {registros_completo.count()}")
    
    if registros_completo.count() > 0:
        print("\n   📊 Registros encontrados:")
        for i, tasa in enumerate(registros_completo, 1):
            # Obtener nombre del rubro
            rubro_nombre = '-'
            if tasa.rubro:
                try:
                    rubro_obj = Rubro.objects.get(codigo=tasa.rubro)
                    rubro_nombre = rubro_obj.descripcion
                except Rubro.DoesNotExist:
                    rubro_nombre = f'Rubro {tasa.rubro} no encontrado'
            
            print(f"\n   {i}. ID: {tasa.id}")
            print(f"      Empresa: {tasa.empresa}")
            print(f"      RTM: {tasa.rtm}")
            print(f"      EXPE: {tasa.expe}")
            print(f"      Año: {tasa.ano}")
            print(f"      Rubro: {tasa.rubro} ({rubro_nombre})")
            print(f"      Código Tarifa: {tasa.cod_tarifa}")
            print(f"      Frecuencia: {tasa.frecuencia}")
            print(f"      Valor: L. {tasa.valor}")
            print(f"      No. Declaración: {tasa.nodecla}")
            print(f"      Cuenta: {tasa.cuenta}")
            print(f"      Cuenta Rezago: {tasa.cuentarez}")
    else:
        print("   ⚠️ No se encontraron registros con estos filtros")
        
        # Verificar qué registros existen para este RTM/EXPE
        print("\n   🔍 Verificando registros existentes para RTM y EXPE:")
        registros_alternos = TasasDecla.objects.filter(rtm=rtm, expe=expe)
        if registros_alternos.count() > 0:
            print(f"   Se encontraron {registros_alternos.count()} registros con RTM y EXPE")
            print("   Valores de 'empresa' encontrados:")
            empresas = registros_alternos.values_list('empresa', flat=True).distinct()
            for emp in empresas:
                count = registros_alternos.filter(empresa=emp).count()
                print(f"      - empresa='{emp}' (tipo: {type(emp).__name__}, len: {len(emp) if emp else 0}): {count} registros")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Consulta SQL directa
print("\n🔍 Test 5: Consulta SQL directa")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, empresa, rtm, expe, ano, rubro, cod_tarifa, frecuencia, valor, nodecla
            FROM tasasdecla
            WHERE rtm = %s AND expe = %s
            LIMIT 5
        """, [rtm, expe])
        
        rows = cursor.fetchall()
        print(f"   Total encontrados: {len(rows)}")
        
        if rows:
            print("\n   📊 Registros (SQL directo):")
            for row in rows:
                print(f"   - id={row[0]}, empresa='{row[1]}', rtm={row[2]}, expe={row[3]}, ano={row[4]}, rubro={row[5]}")
        else:
            print("   ⚠️ No se encontraron registros")
            
        # Verificar estructura de la tabla
        cursor.execute("DESCRIBE tasasdecla")
        columns = cursor.fetchall()
        print("\n   📋 Estructura de la tabla:")
        for col in columns:
            print(f"      {col[0]}: {col[1]}")
            
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("FIN DEL TEST")
print("=" * 80)

