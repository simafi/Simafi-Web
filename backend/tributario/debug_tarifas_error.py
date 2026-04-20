#!/usr/bin/env python3
"""
Script para diagnosticar el error específico de TarifasICS
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def debug_tarifas_error():
    """Diagnosticar el error específico de TarifasICS"""
    print("=== DIAGNÓSTICO DE ERROR TARIFASICS ===")
    
    try:
        # 1. Probar imports
        print("\n1️⃣ Probando imports...")
        from .tributario_app.models import Negocio, TarifasICS, Rubro, Tarifas
        from tributario_app.forms import TarifasICSForm
        print("✅ Todos los imports funcionan")
        
        # 2. Probar creación de formulario
        print("\n2️⃣ Probando creación de formulario...")
        form = TarifasICSForm()
        print("✅ Formulario creado correctamente")
        
        # 3. Probar acceso a modelos
        print("\n3️⃣ Probando acceso a modelos...")
        negocio_count = Negocio.objects.count()
        tarifas_ics_count = TarifasICS.objects.count()
        rubro_count = Rubro.objects.count()
        tarifas_count = Tarifas.objects.count()
        
        print(f"✅ Negocio: {negocio_count} registros")
        print(f"✅ TarifasICS: {tarifas_ics_count} registros")
        print(f"✅ Rubro: {rubro_count} registros")
        print(f"✅ Tarifas: {tarifas_count} registros")
        
        # 4. Probar búsqueda de negocio específico
        print("\n4️⃣ Probando búsqueda de negocio...")
        try:
            negocio = Negocio.objects.get(empre='0301', rtm='TEST003', expe='003')
            print(f"✅ Negocio encontrado: {negocio.nombrenego}")
            
            # 5. Probar búsqueda de tarifas ICS para este negocio
            print("\n5️⃣ Probando búsqueda de tarifas ICS...")
            tarifas_ics = TarifasICS.objects.filter(
                rtm=negocio.rtm,
                expe=negocio.expe
            ).order_by('cod_tarifa')
            print(f"✅ Tarifas ICS encontradas: {tarifas_ics.count()}")
            
        except Negocio.DoesNotExist:
            print("❌ Negocio no encontrado")
        except Exception as e:
            print(f"❌ Error al buscar negocio: {str(e)}")
        
        # 6. Probar la vista directamente
        print("\n6️⃣ Probando vista directamente...")
        try:
            from modules.tributario.simple_views import configurar_tasas_negocio
            print("✅ Vista importada correctamente")
        except Exception as e:
            print(f"❌ Error al importar vista: {str(e)}")
        
        print("\n✅ DIAGNÓSTICO COMPLETADO")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN DIAGNÓSTICO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_tarifas_error()
















