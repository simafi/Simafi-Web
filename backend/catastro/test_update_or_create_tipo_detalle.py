"""
Script de prueba para verificar que la funcionalidad de update_or_create funciona correctamente
en la creación de tipos de detalle.

Ejecutar desde Django shell:
    python manage.py shell
    >>> exec(open('test_update_or_create_tipo_detalle.py').read())
"""

from catastro.models import TipoDetalle
from decimal import Decimal

print("=" * 70)
print("PRUEBA: UPDATE_OR_CREATE EN TIPO DETALLE")
print("=" * 70)

empresa = "0301"
codigo = "999"  # Código de prueba
descripcion_inicial = "PRUEBA INICIAL"
descripcion_actualizada = "PRUEBA ACTUALIZADA"
costo_inicial = Decimal('100.000')
costo_actualizado = Decimal('200.000')

print(f"\nEmpresa: {empresa}")
print(f"Código: {codigo}")
print(f"\n1. Creando registro inicial...")
print(f"   Descripción: {descripcion_inicial}")
print(f"   Costo: {costo_inicial}")

# Primera creación
tipo_detalle, created = TipoDetalle.objects.update_or_create(
    empresa=empresa,
    codigo=codigo,
    defaults={
        'descripcion': descripcion_inicial,
        'costo': costo_inicial
    }
)

if created:
    print("   ✓ Registro CREADO exitosamente")
else:
    print("   → Registro YA EXISTÍA, se actualizó")

print(f"\n   Estado actual:")
print(f"   - ID: {tipo_detalle.id}")
print(f"   - Descripción: {tipo_detalle.descripcion}")
print(f"   - Costo: {tipo_detalle.costo}")

print(f"\n2. Intentando crear/actualizar con el mismo código...")
print(f"   Descripción nueva: {descripcion_actualizada}")
print(f"   Costo nuevo: {costo_actualizado}")

# Segunda llamada (debería actualizar, no crear)
tipo_detalle2, created2 = TipoDetalle.objects.update_or_create(
    empresa=empresa,
    codigo=codigo,
    defaults={
        'descripcion': descripcion_actualizada,
        'costo': costo_actualizado
    }
)

if created2:
    print("   ✗ ERROR: Se creó un nuevo registro (no debería)")
else:
    print("   ✓ Registro ACTUALIZADO exitosamente (correcto)")

print(f"\n   Estado después de update_or_create:")
print(f"   - ID: {tipo_detalle2.id}")
print(f"   - Descripción: {tipo_detalle2.descripcion}")
print(f"   - Costo: {tipo_detalle2.costo}")

# Verificar que es el mismo registro
if tipo_detalle.id == tipo_detalle2.id:
    print(f"\n   ✓ Verificación: Es el MISMO registro (ID: {tipo_detalle.id})")
else:
    print(f"\n   ✗ ERROR: Son registros DIFERENTES (ID1: {tipo_detalle.id}, ID2: {tipo_detalle2.id})")

# Verificar que los datos se actualizaron
if tipo_detalle2.descripcion == descripcion_actualizada and tipo_detalle2.costo == costo_actualizado:
    print(f"   ✓ Verificación: Los datos se ACTUALIZARON correctamente")
else:
    print(f"   ✗ ERROR: Los datos NO se actualizaron correctamente")

print("\n" + "=" * 70)
print("PRUEBA COMPLETADA")
print("=" * 70)

# Limpiar registro de prueba (opcional)
# tipo_detalle2.delete()
# print("\nRegistro de prueba eliminado")




