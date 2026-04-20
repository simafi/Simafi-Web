#!/usr/bin/env python
"""
Script simple para verificar el campo tipota en la base de datos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario.models import TasasDecla

def check_tipota():
    print("🔍 VERIFICANDO CAMPO TIPOTA EN BASE DE DATOS")
    print("=" * 60)
    
    try:
        # Verificar si hay registros
        total = TasasDecla.objects.count()
        print(f"📊 Total de registros en tasasdecla: {total}")
        
        if total == 0:
            print("❌ No hay registros en la tabla tasasdecla")
            return
        
        # Obtener algunos registros de muestra
        print("\n📋 PRIMEROS 5 REGISTROS:")
        tasas = TasasDecla.objects.all()[:5]
        
        for i, tasa in enumerate(tasas, 1):
            print(f"   {i}. ID: {tasa.id}")
            print(f"      RTM: {tasa.rtm}")
            print(f"      Rubro: {tasa.rubro}")
            print(f"      Tipota: '{tasa.tipota}' (longitud: {len(str(tasa.tipota))})")
            print(f"      Valor: {tasa.valor}")
            print()
        
        # Verificar registros con tipota vacío vs con valor
        vacios = TasasDecla.objects.filter(tipota='').count()
        con_valor = TasasDecla.objects.exclude(tipota='').count()
        
        print(f"📊 ESTADÍSTICAS:")
        print(f"   - Registros con tipota vacío: {vacios}")
        print(f"   - Registros con tipota con valor: {con_valor}")
        
        # Mostrar valores únicos de tipota
        valores_unicos = TasasDecla.objects.values_list('tipota', flat=True).distinct()
        print(f"\n📊 VALORES ÚNICOS DE TIPOTA:")
        for valor in valores_unicos:
            count = TasasDecla.objects.filter(tipota=valor).count()
            print(f"   - '{valor}': {count} registros")
        
        # Verificar si hay registros con tipota = 'F' o 'V'
        f_count = TasasDecla.objects.filter(tipota='F').count()
        v_count = TasasDecla.objects.filter(tipota='V').count()
        
        print(f"\n📊 VALORES ESPECÍFICOS:")
        print(f"   - tipota = 'F': {f_count} registros")
        print(f"   - tipota = 'V': {v_count} registros")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_tipota()









































