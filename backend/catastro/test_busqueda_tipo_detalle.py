"""
Script de prueba para verificar la funcionalidad de búsqueda de tipo detalle
en el formulario de detalle adicional.

Este script prueba:
1. La búsqueda por empresa y código en la tabla tipodetalle
2. Que los datos se devuelvan correctamente (descripcion y costo)
3. Que la API funcione correctamente

Datos de prueba (deben existir en la BD):
- empresa: "0301"
- códigos: "111", "112", "113", "121", "122"

Para ejecutar:
    python manage.py shell < test_busqueda_tipo_detalle.py
    O desde el directorio catastro:
    python -c "exec(open('test_busqueda_tipo_detalle.py').read())"
"""

import os
import sys

# Intentar configurar Django de diferentes maneras
try:
    import django
    # Intentar con catastro.settings
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catastro.settings')
        django.setup()
    except:
        # Si falla, intentar encontrar el settings correcto
        # Buscar en el directorio padre
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        # Intentar con settings común
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
            django.setup()
        except:
            # Si estamos en shell de Django, ya está configurado
            pass
except ImportError:
    print("Django no está instalado o no se puede importar")
    print("Ejecuta este script desde Django shell: python manage.py shell < test_busqueda_tipo_detalle.py")
    sys.exit(1)

from catastro.models import TipoDetalle
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from catastro.views import api_buscar_tipo_detalle
import json

def crear_datos_prueba():
    """
    Crear datos de prueba en la tabla tipodetalle si no existen
    """
    empresa = "0301"
    datos_prueba = [
        {"codigo": "111", "descripcion": "ENCHAPES AZULEJO INFERIOR", "costo": 0.000},
        {"codigo": "112", "descripcion": "ENCHAPES AZULEJO REGULAR.", "costo": 210.82},
        {"codigo": "113", "descripcion": "NCHAPES AZULEJO SUPERIOR", "costo": 284.28},
        {"codigo": "121", "descripcion": "ENCHAPES CERAMICA INFERIOR", "costo": 261.14},
        {"codigo": "122", "descripcion": "ENCHAPES CERAMICA REGULAR", "costo": 271.85},
    ]
    
    print("=" * 70)
    print("CREANDO/VERIFICANDO DATOS DE PRUEBA EN tipodetalle")
    print("=" * 70)
    
    creados = 0
    existentes = 0
    
    for dato in datos_prueba:
        tipo_detalle, created = TipoDetalle.objects.get_or_create(
            empresa=empresa,
            codigo=dato["codigo"],
            defaults={
                "descripcion": dato["descripcion"],
                "costo": dato["costo"]
            }
        )
        
        if created:
            print(f"✓ Creado: empresa={empresa}, codigo={dato['codigo']}, descripcion={dato['descripcion']}, costo={dato['costo']}")
            creados += 1
        else:
            print(f"→ Ya existe: empresa={empresa}, codigo={dato['codigo']}, descripcion={tipo_detalle.descripcion}, costo={tipo_detalle.costo}")
            existentes += 1
    
    print(f"\nResumen: {creados} creados, {existentes} ya existían")
    print("=" * 70)
    return empresa

def probar_busqueda_directa():
    """
    Probar la búsqueda directa en el modelo
    """
    print("\n" + "=" * 70)
    print("PRUEBA 1: BÚSQUEDA DIRECTA EN EL MODELO")
    print("=" * 70)
    
    empresa = "0301"
    codigos_prueba = ["111", "112", "113", "121", "122", "999"]  # 999 no existe
    
    for codigo in codigos_prueba:
        try:
            tipo_detalle = TipoDetalle.objects.filter(empresa=empresa, codigo=codigo).first()
            
            if tipo_detalle:
                print(f"✓ Encontrado: codigo={codigo}")
                print(f"  - Descripción: {tipo_detalle.descripcion}")
                print(f"  - Costo: {tipo_detalle.costo}")
            else:
                print(f"✗ No encontrado: codigo={codigo} (empresa={empresa})")
        except Exception as e:
            print(f"✗ Error al buscar codigo={codigo}: {str(e)}")
    
    print("=" * 70)

def probar_api_vista():
    """
    Probar la vista API api_buscar_tipo_detalle
    """
    print("\n" + "=" * 70)
    print("PRUEBA 2: PRUEBA DE LA VISTA API")
    print("=" * 70)
    
    empresa = "0301"
    codigos_prueba = ["111", "112", "113", "121", "122", "999"]  # 999 no existe
    
    factory = RequestFactory()
    
    for codigo in codigos_prueba:
        try:
            # Crear request GET con empresa y código
            request = factory.get('/api/buscar-tipo-detalle/', {
                'empresa': empresa,
                'codigo': codigo
            })
            
            # Agregar sesión al request
            middleware = SessionMiddleware(lambda req: None)
            middleware.process_request(request)
            request.session.save()
            request.session['catastro_empresa'] = empresa
            
            # Llamar a la vista
            response = api_buscar_tipo_detalle(request)
            
            # Parsear respuesta JSON
            if hasattr(response, 'content'):
                data = json.loads(response.content.decode('utf-8'))
            else:
                data = response
            
            if data.get('encontrado'):
                print(f"✓ API Encontrado: codigo={codigo}")
                print(f"  - Descripción: {data.get('descripcion', 'N/A')}")
                print(f"  - Costo: {data.get('costo', 'N/A')}")
            else:
                print(f"✗ API No encontrado: codigo={codigo}")
                print(f"  - Mensaje: {data.get('mensaje', 'N/A')}")
        except Exception as e:
            print(f"✗ Error al probar API codigo={codigo}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("=" * 70)

def probar_busqueda_sin_empresa():
    """
    Probar la búsqueda sin empresa (solo código)
    """
    print("\n" + "=" * 70)
    print("PRUEBA 3: BÚSQUEDA SIN EMPRESA (SOLO CÓDIGO)")
    print("=" * 70)
    
    codigo = "111"
    
    factory = RequestFactory()
    
    try:
        # Crear request GET solo con código (sin empresa)
        request = factory.get('/api/buscar-tipo-detalle/', {
            'codigo': codigo
        })
        
        # Agregar sesión al request
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        # No establecer empresa en la sesión
        
        # Llamar a la vista
        response = api_buscar_tipo_detalle(request)
        
        # Parsear respuesta JSON
        if hasattr(response, 'content'):
            data = json.loads(response.content.decode('utf-8'))
        else:
            data = response
        
        if data.get('encontrado'):
            print(f"✓ Encontrado sin empresa: codigo={codigo}")
            print(f"  - Descripción: {data.get('descripcion', 'N/A')}")
            print(f"  - Costo: {data.get('costo', 'N/A')}")
        else:
            print(f"✗ No encontrado sin empresa: codigo={codigo}")
            print(f"  - Mensaje: {data.get('mensaje', 'N/A')}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("=" * 70)

def main():
    """
    Función principal que ejecuta todas las pruebas
    """
    print("\n" + "=" * 70)
    print("SCRIPT DE PRUEBA: BÚSQUEDA DE TIPO DETALLE")
    print("=" * 70)
    
    try:
        # Crear/verificar datos de prueba
        empresa = crear_datos_prueba()
        
        # Probar búsqueda directa
        probar_busqueda_directa()
        
        # Probar API vista
        probar_api_vista()
        
        # Probar búsqueda sin empresa
        probar_busqueda_sin_empresa()
        
        print("\n" + "=" * 70)
        print("PRUEBAS COMPLETADAS")
        print("=" * 70)
        print("\nPara probar en el navegador:")
        print(f"1. Inicia sesión en el sistema de catastro")
        print(f"2. Ve al formulario de detalle adicional")
        print(f"3. Ingresa uno de estos códigos en el campo 'Código':")
        print(f"   - 111 (ENCHAPES AZULEJO INFERIOR - Costo: 0.00)")
        print(f"   - 112 (ENCHAPES AZULEJO REGULAR. - Costo: 210.82)")
        print(f"   - 113 (NCHAPES AZULEJO SUPERIOR - Costo: 284.28)")
        print(f"   - 121 (ENCHAPES CERAMICA INFERIOR - Costo: 261.14)")
        print(f"   - 122 (ENCHAPES CERAMICA REGULAR - Costo: 271.85)")
        print(f"4. Verifica que se autocompleten los campos 'Descripción' y 'Valor Unitario'")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ ERROR GENERAL: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

