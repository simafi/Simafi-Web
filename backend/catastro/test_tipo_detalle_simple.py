"""
Script simple para probar la búsqueda de tipo detalle.

OPCIÓN 1: Ejecutar desde Django shell interactivo:
    python manage.py shell
    >>> exec(open('test_tipo_detalle_simple.py').read())

OPCIÓN 2: Copiar y pegar el contenido en Django shell.

OPCIÓN 3: Ejecutar directamente (requiere configuración Django):
    python test_tipo_detalle_simple.py
"""

# Intentar importar Django si no está configurado
try:
    from catastro.models import TipoDetalle
except ImportError:
    import os
    import sys
    import django
    
    # Agregar el directorio actual al path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Configurar Django
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catastro.settings')
        django.setup()
        from catastro.models import TipoDetalle
    except Exception as e:
        print("=" * 70)
        print("ERROR: No se pudo configurar Django automáticamente")
        print("=" * 70)
        print(f"Error: {str(e)}")
        print("\nPor favor ejecuta este script desde Django shell:")
        print("  python manage.py shell")
        print("  >>> exec(open('test_tipo_detalle_simple.py').read())")
        print("=" * 70)
        sys.exit(1)

print("=" * 70)
print("PRUEBA DE BÚSQUEDA DE TIPO DETALLE")
print("=" * 70)

# Datos de prueba
empresa = "0301"
codigos_prueba = ["111", "112", "113", "121", "122"]

print(f"\nEmpresa: {empresa}")
print(f"Códigos a probar: {', '.join(codigos_prueba)}")
print("\n" + "-" * 70)

# Crear/verificar datos de prueba
datos_prueba = [
    {"codigo": "111", "descripcion": "ENCHAPES AZULEJO INFERIOR", "costo": 0.000},
    {"codigo": "112", "descripcion": "ENCHAPES AZULEJO REGULAR.", "costo": 210.82},
    {"codigo": "113", "descripcion": "NCHAPES AZULEJO SUPERIOR", "costo": 284.28},
    {"codigo": "121", "descripcion": "ENCHAPES CERAMICA INFERIOR", "costo": 261.14},
    {"codigo": "122", "descripcion": "ENCHAPES CERAMICA REGULAR", "costo": 271.85},
]

print("\n1. CREANDO/VERIFICANDO DATOS DE PRUEBA:")
print("-" * 70)
for dato in datos_prueba:
    tipo_detalle, created = TipoDetalle.objects.get_or_create(
        empresa=empresa,
        codigo=dato["codigo"],
        defaults={
            "descripcion": dato["descripcion"],
            "costo": dato["costo"]
        }
    )
    status = "✓ CREADO" if created else "→ YA EXISTE"
    print(f"{status}: código={dato['codigo']}, descripcion={tipo_detalle.descripcion}, costo={tipo_detalle.costo}")

print("\n" + "-" * 70)
print("\n2. PROBANDO BÚSQUEDA POR EMPRESA Y CÓDIGO:")
print("-" * 70)

for codigo in codigos_prueba:
    try:
        tipo_detalle = TipoDetalle.objects.filter(empresa=empresa, codigo=codigo).first()
        
        if tipo_detalle:
            print(f"✓ ENCONTRADO: código={codigo}")
            print(f"  - Descripción: {tipo_detalle.descripcion}")
            print(f"  - Costo: {tipo_detalle.costo}")
        else:
            print(f"✗ NO ENCONTRADO: código={codigo} (empresa={empresa})")
    except Exception as e:
        print(f"✗ ERROR al buscar código={codigo}: {str(e)}")

print("\n" + "-" * 70)
print("\n3. PROBANDO BÚSQUEDA SIN EMPRESA (solo código):")
print("-" * 70)

codigo = "111"
tipo_detalle = TipoDetalle.objects.filter(codigo=codigo).first()
if tipo_detalle:
    print(f"✓ ENCONTRADO sin empresa: código={codigo}")
    print(f"  - Empresa: {tipo_detalle.empresa}")
    print(f"  - Descripción: {tipo_detalle.descripcion}")
    print(f"  - Costo: {tipo_detalle.costo}")
else:
    print(f"✗ NO ENCONTRADO sin empresa: código={codigo}")

print("\n" + "=" * 70)
print("PRUEBAS COMPLETADAS")
print("=" * 70)
print("\nPara probar en el navegador:")
print("1. Inicia sesión en el sistema de catastro (empresa: 0301)")
print("2. Ve al formulario de detalle adicional")
print("3. Ingresa uno de estos códigos en el campo 'Código':")
for dato in datos_prueba:
    print(f"   - {dato['codigo']} ({dato['descripcion']} - Costo: {dato['costo']})")
print("4. Verifica que se autocompleten los campos 'Descripción' y 'Valor Unitario'")
print("=" * 70)

