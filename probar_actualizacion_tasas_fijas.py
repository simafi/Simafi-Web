#!/usr/bin/env python
"""
Script para probar la funcionalidad de actualización de tasas fijas
en el formulario de volumen_ventas.

Este script simula el proceso que se ejecuta automáticamente cuando
se carga el formulario de declaración de volumen de ventas.
"""

import os
import sys
import django

# Configurar Django
sys.path.append('C:\\simafiweb')
sys.path.append('C:\\simafiweb\\venv\\Scripts')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')
django.setup()

def probar_actualizacion_tasas():
    """Probar la funcionalidad de actualización de tasas fijas"""
    
    print("🧪 PROBANDO ACTUALIZACIÓN DE TASAS FIJAS")
    print("=" * 50)
    
    try:
        from tributario.models import TasasDecla, Tarifas
        
        # Obtener algunas tasas de ejemplo para probar
        municipio_codigo = '0301'
        
        print(f"📋 Buscando tasas con tipota='F' en empresa {municipio_codigo}...")
        
        # Buscar tasas con tipota = 'F' (excluyendo C0001 y C0003)
        tasas_fijas = TasasDecla.objects.filter(
            empresa=municipio_codigo,
            tipota='F'
        ).exclude(
            cod_tarifa__in=['C0001', 'C0003']
        )[:5]  # Limitar a 5 para la prueba
        
        if not tasas_fijas.exists():
            print("⚠️ No se encontraron tasas con tipota='F' para probar")
            return
        
        print(f"✅ Encontradas {tasas_fijas.count()} tasas fijas para probar")
        print()
        
        tasas_actualizadas = 0
        
        for tasa in tasas_fijas:
            print(f"🔍 Procesando tasa: {tasa.cod_tarifa}")
            print(f"   - Empresa: {tasa.empresa}")
            print(f"   - Rubro: {tasa.rubro}")
            print(f"   - Año: {tasa.ano}")
            print(f"   - Valor actual: {tasa.valor}")
            
            try:
                # Buscar en la tabla tarifas
                tarifa = Tarifas.objects.get(
                    empresa=tasa.empresa,
                    rubro=tasa.rubro,
                    cod_tarifa=tasa.cod_tarifa,
                    ano=tasa.ano
                )
                
                print(f"   - Valor en tarifas: {tarifa.valor}")
                
                if tasa.valor != tarifa.valor:
                    print(f"   ✅ ACTUALIZACIÓN NECESARIA: {tasa.valor} → {tarifa.valor}")
                    # En una prueba real, aquí se haría: tasa.valor = tarifa.valor; tasa.save()
                    tasas_actualizadas += 1
                else:
                    print(f"   ✅ Valor ya actualizado")
                
            except Tarifas.DoesNotExist:
                print(f"   ⚠️ No se encontró tarifa correspondiente en tabla tarifas")
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            
            print()
        
        print(f"📊 RESUMEN DE PRUEBA:")
        print(f"   - Tasas procesadas: {tasas_fijas.count()}")
        print(f"   - Tasas que necesitan actualización: {tasas_actualizadas}")
        print(f"   - Tasas ya actualizadas: {tasas_fijas.count() - tasas_actualizadas}")
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")

def mostrar_estructura_tablas():
    """Mostrar la estructura de las tablas involucradas"""
    
    print("\n📋 ESTRUCTURA DE TABLAS")
    print("=" * 50)
    
    try:
        from tributario.models import TasasDecla, Tarifas
        
        print("🔹 TABLA tasasdecla:")
        print("   Campos clave: empresa, rubro, cod_tarifa, ano, valor, tipota")
        print("   - tipota='F' → Tasas fijas (se actualizan automáticamente)")
        print("   - tipota='V' → Tasas variables (no se actualizan)")
        print("   - tipota='T' → Tasas temporales (no se actualizan)")
        print("   - Excluye: C0001, C0003 (ya configuradas)")
        
        print("\n🔹 TABLA tarifas:")
        print("   Campos clave: empresa, rubro, cod_tarifa, ano, valor")
        print("   - Contiene los valores de referencia para las tarifas")
        
        print("\n🔹 PROCESO DE ACTUALIZACIÓN:")
        print("   1. Se filtran las tasas con tipota='F'")
        print("   2. Se excluyen C0001 y C0003")
        print("   3. Se busca en tarifas usando empresa+rubro+cod_tarifa+ano")
        print("   4. Se actualiza el valor en tasasdecla")
        
    except Exception as e:
        print(f"❌ Error mostrando estructura: {str(e)}")

def verificar_datos_ejemplo():
    """Verificar que existen datos de ejemplo para probar"""
    
    print("\n🔍 VERIFICANDO DATOS DE EJEMPLO")
    print("=" * 50)
    
    try:
        from tributario.models import TasasDecla, Tarifas
        
        municipio_codigo = '0301'
        
        # Contar tasas por tipo
        tasas_fijas = TasasDecla.objects.filter(empresa=municipio_codigo, tipota='F').count()
        tasas_variables = TasasDecla.objects.filter(empresa=municipio_codigo, tipota='V').count()
        tasas_temporales = TasasDecla.objects.filter(empresa=municipio_codigo, tipota='T').count()
        total_tasas = TasasDecla.objects.filter(empresa=municipio_codigo).count()
        
        print(f"📊 Tasas en empresa {municipio_codigo}:")
        print(f"   - Total: {total_tasas}")
        print(f"   - Fijas (tipota='F'): {tasas_fijas}")
        print(f"   - Variables (tipota='V'): {tasas_variables}")
        print(f"   - Temporales (tipota='T'): {tasas_temporales}")
        
        # Contar tarifas
        total_tarifas = Tarifas.objects.filter(empresa=municipio_codigo).count()
        print(f"   - Tarifas disponibles: {total_tarifas}")
        
        if tasas_fijas > 0:
            print("✅ Hay tasas fijas disponibles para probar")
        else:
            print("⚠️ No hay tasas fijas disponibles para probar")
        
    except Exception as e:
        print(f"❌ Error verificando datos: {str(e)}")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE ACTUALIZACIÓN DE TASAS FIJAS")
    print("=" * 60)
    
    # Mostrar estructura
    mostrar_estructura_tablas()
    
    # Verificar datos
    verificar_datos_ejemplo()
    
    # Probar actualización
    probar_actualizacion_tasas()
    
    print("\n✅ PRUEBAS COMPLETADAS")
    print("=" * 60)
