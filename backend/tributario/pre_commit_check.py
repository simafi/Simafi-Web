#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para ejecutar antes de hacer commit o cambios importantes
Verifica que las funcionalidades críticas sigan funcionando
"""

import sys
import os
from pathlib import Path

# Agregar el directorio al path para imports
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

# Lista de funciones críticas que deben existir
FUNCIONES_CRITICAS = {
    'simple_views.py': [
        'declaracion_volumen',
        'generar_transacciones',
    ],
    'views.py': [
        'tarifas_crud',
        'plan_arbitrio_crud',
    ],
    'ajax_views.py': [
        'buscar_actividad_ajax',
        'calcular_tasas_plan_arbitrio',
    ]
}

# Patrones que deben existir en el código
PATRONES_CRITICOS = {
    'simple_views.py': [
        ('TarifasICS.objects.filter', 'Debe buscar tarifasics'),
        ('TasasDecla.objects.create', 'Debe crear tasas en tasasdecla'),
        ('nodecla', 'Debe usar nodecla para declaraciones'),
        ('safe_decimal', 'Debe usar safe_decimal para conversiones'),
    ]
}


def verificar_funciones_criticas():
    """Verifica que las funciones críticas existan"""
    problemas = []
    
    for archivo, funciones in FUNCIONES_CRITICAS.items():
        archivo_path = BASE_DIR / archivo
        if not archivo_path.exists():
            problemas.append(f"❌ Archivo no existe: {archivo}")
            continue
        
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        for funcion in funciones:
            # Buscar definición de función
            patron_def = f"def {funcion}("
            patron_async = f"async def {funcion}("
            
            if patron_def not in contenido and patron_async not in contenido:
                problemas.append(
                    f"⚠️ {archivo}: Función '{funcion}' no encontrada"
                )
            else:
                print(f"✅ {archivo}: {funcion} - OK")
    
    return problemas


def verificar_patrones_criticos():
    """Verifica que los patrones críticos existan en el código"""
    problemas = []
    
    for archivo, patrones in PATRONES_CRITICOS.items():
        archivo_path = BASE_DIR / archivo
        if not archivo_path.exists():
            continue
        
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        for patron, descripcion in patrones:
            if patron not in contenido:
                problemas.append(
                    f"⚠️ {archivo}: Patrón '{patron}' no encontrado - {descripcion}"
                )
            else:
                print(f"✅ {archivo}: Patrón '{patron}' - OK")
    
    return problemas


def verificar_imports_criticos():
    """Verifica que los imports críticos estén presentes"""
    problemas = []
    
    archivo = 'simple_views.py'
    archivo_path = BASE_DIR / archivo
    if not archivo_path.exists():
        return problemas
    
    with open(archivo_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    imports_criticos = [
        'from tributario.models import',
        'from tributario_app.models import TarifasICS',
        'from decimal import Decimal',
    ]
    
    for import_critico in imports_criticos:
        if import_critico not in contenido:
            problemas.append(
                f"⚠️ {archivo}: Import crítico no encontrado: {import_critico}"
            )
        else:
            print(f"✅ {archivo}: Import '{import_critico}' - OK")
    
    return problemas


def main():
    """Ejecuta todas las verificaciones"""
    print("="*60)
    print("VERIFICACIÓN PRE-COMMIT")
    print("="*60)
    
    problemas = []
    
    print("\n🔍 Verificando funciones críticas...")
    problemas.extend(verificar_funciones_criticas())
    
    print("\n🔍 Verificando patrones críticos...")
    problemas.extend(verificar_patrones_criticos())
    
    print("\n🔍 Verificando imports críticos...")
    problemas.extend(verificar_imports_criticos())
    
    print("\n" + "="*60)
    if problemas:
        print("⚠️ PROBLEMAS ENCONTRADOS:")
        for problema in problemas:
            print(f"  {problema}")
        print("\n❌ NO se recomienda hacer commit hasta resolver estos problemas")
        return 1
    else:
        print("✅ Todas las verificaciones pasaron")
        print("✅ Código listo para commit")
        return 0


if __name__ == "__main__":
    sys.exit(main())























