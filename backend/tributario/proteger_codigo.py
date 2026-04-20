#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para proteger código funcionando antes de hacer cambios
Crea respaldos automáticos y verifica integridad
"""

import os
import shutil
import datetime
import json
from pathlib import Path

# Configuración
BASE_DIR = Path(__file__).parent
BACKUP_DIR = BASE_DIR / 'backups'
ARCHIVOS_CRITICOS = [
    'simple_views.py',
    'views.py',
    'models.py',
    'ajax_views.py',
]

PUNTOS_CRITICOS = {
    'simple_views.py': {
        'declaracion_volumen': {
            'lineas': (92, 750),
            'descripcion': 'Función crítica: guardado de declaraciones y creación de tasas'
        },
        'crear_tasas_desde_tarifasics': {
            'lineas': (409, 589),
            'descripcion': 'Proceso crítico: transferencia de tasas desde tarifasics a tasasdecla'
        }
    },
    'views.py': {
        'tarifas_crud': {
            'lineas': (1650, 1800),
            'descripcion': 'Vista crítica: formulario de tarifas'
        },
        'plan_arbitrio_crud': {
            'lineas': (1800, 2000),
            'descripcion': 'Vista crítica: formulario de plan de arbitrio'
        }
    }
}


def crear_respaldo(nombre_archivo, razon="Cambio manual"):
    """Crea un respaldo del archivo antes de modificarlo"""
    if not BACKUP_DIR.exists():
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    archivo_original = BASE_DIR / nombre_archivo
    if not archivo_original.exists():
        print(f"⚠️ Archivo {nombre_archivo} no existe")
        return None
    
    # Crear nombre de respaldo con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_backup = f"{nombre_archivo}.backup_{timestamp}"
    archivo_backup = BACKUP_DIR / nombre_backup
    
    # Copiar archivo
    shutil.copy2(archivo_original, archivo_backup)
    
    # Guardar metadatos
    metadata = {
        'archivo': nombre_archivo,
        'backup': nombre_backup,
        'fecha': timestamp,
        'razon': razon,
        'tamaño': archivo_original.stat().st_size
    }
    
    metadata_file = BACKUP_DIR / f"{nombre_backup}.meta.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Respaldo creado: {nombre_backup}")
    return str(archivo_backup)


def listar_respaldos(nombre_archivo=None):
    """Lista todos los respaldos disponibles"""
    if not BACKUP_DIR.exists():
        print("No hay respaldos disponibles")
        return []
    
    respaldos = []
    for archivo in BACKUP_DIR.glob("*.backup_*"):
        if not archivo.name.endswith('.meta.json'):
            if nombre_archivo is None or nombre_archivo in archivo.name:
                metadata_file = BACKUP_DIR / f"{archivo.name}.meta.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    respaldos.append(metadata)
    
    respaldos.sort(key=lambda x: x['fecha'], reverse=True)
    return respaldos


def restaurar_respaldo(nombre_backup):
    """Restaura un archivo desde un respaldo"""
    archivo_backup = BACKUP_DIR / nombre_backup
    if not archivo_backup.exists():
        print(f"❌ Respaldo {nombre_backup} no existe")
        return False
    
    # Leer metadata
    metadata_file = BACKUP_DIR / f"{nombre_backup}.meta.json"
    if metadata_file.exists():
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        archivo_original = BASE_DIR / metadata['archivo']
    else:
        # Intentar extraer nombre del archivo del nombre del backup
        nombre_archivo = nombre_backup.split('.backup_')[0]
        archivo_original = BASE_DIR / nombre_archivo
    
    # Crear respaldo del archivo actual antes de restaurar
    if archivo_original.exists():
        crear_respaldo(archivo_original.name, "Antes de restaurar backup")
    
    # Restaurar
    shutil.copy2(archivo_backup, archivo_original)
    print(f"✅ Archivo restaurado: {archivo_original.name}")
    print(f"   Desde respaldo: {nombre_backup}")
    if metadata_file.exists():
        print(f"   Fecha original: {metadata['fecha']}")
        print(f"   Razón: {metadata.get('razon', 'N/A')}")
    return True


def verificar_puntos_criticos():
    """Verifica que los puntos críticos del código sigan intactos"""
    problemas = []
    
    for archivo, puntos in PUNTOS_CRITICOS.items():
        archivo_path = BASE_DIR / archivo
        if not archivo_path.exists():
            problemas.append(f"❌ Archivo crítico no existe: {archivo}")
            continue
        
        with open(archivo_path, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        for punto, info in puntos.items():
            inicio, fin = info['lineas']
            # Verificar que las líneas críticas no estén vacías
            contenido_relevante = ''.join(lineas[inicio-1:fin])
            if not contenido_relevante.strip():
                problemas.append(
                    f"⚠️ {archivo}: {punto} ({info['descripcion']}) - "
                    f"Líneas {inicio}-{fin} parecen estar vacías"
                )
            else:
                print(f"✅ {archivo}: {punto} - OK")
    
    return problemas


def crear_checkpoint(razon="Checkpoint manual"):
    """Crea un checkpoint de todos los archivos críticos"""
    print("="*60)
    print("CREANDO CHECKPOINT DE ARCHIVOS CRÍTICOS")
    print("="*60)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_dir = BACKUP_DIR / f"checkpoint_{timestamp}"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    checkpoint_info = {
        'fecha': timestamp,
        'razon': razon,
        'archivos': []
    }
    
    for archivo in ARCHIVOS_CRITICOS:
        archivo_path = BASE_DIR / archivo
        if archivo_path.exists():
            backup_path = checkpoint_dir / archivo
            shutil.copy2(archivo_path, backup_path)
            checkpoint_info['archivos'].append({
                'archivo': archivo,
                'tamaño': archivo_path.stat().st_size,
                'lineas': len(open(archivo_path, 'r', encoding='utf-8').readlines())
            })
            print(f"✅ {archivo} respaldado")
    
    # Guardar info del checkpoint
    info_file = checkpoint_dir / "checkpoint_info.json"
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(checkpoint_info, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Checkpoint creado: checkpoint_{timestamp}")
    print(f"   Archivos: {len(checkpoint_info['archivos'])}")
    return checkpoint_dir


def menu_interactivo():
    """Menú interactivo para gestionar respaldos"""
    while True:
        print("\n" + "="*60)
        print("SISTEMA DE PROTECCIÓN DE CÓDIGO")
        print("="*60)
        print("1. Crear respaldo de archivo específico")
        print("2. Crear checkpoint completo")
        print("3. Listar respaldos disponibles")
        print("4. Restaurar respaldo")
        print("5. Verificar puntos críticos")
        print("6. Salir")
        print("="*60)
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == '1':
            print("\nArchivos críticos disponibles:")
            for i, archivo in enumerate(ARCHIVOS_CRITICOS, 1):
                print(f"  {i}. {archivo}")
            seleccion = input("\nNúmero de archivo (o nombre completo): ").strip()
            try:
                idx = int(seleccion) - 1
                nombre_archivo = ARCHIVOS_CRITICOS[idx]
            except (ValueError, IndexError):
                nombre_archivo = seleccion
            
            razon = input("Razón del respaldo: ").strip() or "Respaldo manual"
            crear_respaldo(nombre_archivo, razon)
        
        elif opcion == '2':
            razon = input("Razón del checkpoint: ").strip() or "Checkpoint manual"
            crear_checkpoint(razon)
        
        elif opcion == '3':
            print("\n📦 RESPALDOS DISPONIBLES:")
            respaldos = listar_respaldos()
            if respaldos:
                for i, respaldo in enumerate(respaldos, 1):
                    print(f"\n{i}. {respaldo['backup']}")
                    print(f"   Archivo: {respaldo['archivo']}")
                    print(f"   Fecha: {respaldo['fecha']}")
                    print(f"   Razón: {respaldo.get('razon', 'N/A')}")
            else:
                print("No hay respaldos disponibles")
        
        elif opcion == '4':
            respaldos = listar_respaldos()
            if not respaldos:
                print("No hay respaldos disponibles")
                continue
            
            print("\n📦 RESPALDOS DISPONIBLES:")
            for i, respaldo in enumerate(respaldos, 1):
                print(f"{i}. {respaldo['backup']} - {respaldo['fecha']}")
            
            seleccion = input("\nNúmero de respaldo a restaurar: ").strip()
            try:
                idx = int(seleccion) - 1
                nombre_backup = respaldos[idx]['backup']
                confirmar = input(f"¿Restaurar {nombre_backup}? (s/n): ").strip().lower()
                if confirmar == 's':
                    restaurar_respaldo(nombre_backup)
            except (ValueError, IndexError):
                print("❌ Selección inválida")
        
        elif opcion == '5':
            print("\n🔍 VERIFICANDO PUNTOS CRÍTICOS:")
            problemas = verificar_puntos_criticos()
            if problemas:
                print("\n⚠️ PROBLEMAS ENCONTRADOS:")
                for problema in problemas:
                    print(f"  {problema}")
            else:
                print("\n✅ Todos los puntos críticos están OK")
        
        elif opcion == '6':
            print("👋 Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    menu_interactivo()























