#!/usr/bin/env python3
"""
Script para crear respaldo de los archivos funcionando correctamente
"""

import os
import shutil
from datetime import datetime

def crear_respaldo_funcionando():
    """Crea respaldo de todos los archivos modificados y funcionando"""
    
    print("🔒 CREANDO RESPALDO DE ARCHIVOS FUNCIONANDO")
    print("=" * 50)
    
    # Crear directorio de respaldo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"c:/simafiweb/RESPALDO_FUNCIONANDO_{timestamp}"
    
    try:
        os.makedirs(backup_dir, exist_ok=True)
        print(f"📁 Directorio de respaldo creado: {backup_dir}")
    except Exception as e:
        print(f"❌ Error creando directorio: {e}")
        return False
    
    # Lista de archivos a respaldar
    archivos_respaldo = [
        {
            "origen": r"c:\simafiweb\venv\Scripts\tributario\modules\tributario\views.py",
            "destino": "views_funcionando.py",
            "descripcion": "Views Django con API de tarifas y campo controlado corregido"
        },
        {
            "origen": "declaracion_volumen_interactivo.js",
            "destino": "declaracion_volumen_interactivo_funcionando.js",
            "descripcion": "JavaScript con sistema de variables ocultas y parsing mejorado"
        },
        {
            "origen": r"c:\simafiweb\venv\Scripts\tributario\tributario_app\templates\declaracion_volumen.html",
            "destino": "declaracion_volumen_funcionando.html",
            "descripcion": "Template HTML con funciones corregidas"
        },
        {
            "origen": r"c:\simafiweb\venv\Scripts\tributario\modules\tributario\urls.py",
            "destino": "urls_funcionando.py",
            "descripcion": "URLs con API de tarifas configurada"
        },
        {
            "origen": r"c:\simafiweb\venv\Scripts\tributario\tributario_app\forms.py",
            "destino": "forms_funcionando.py",
            "descripcion": "Formulario Django funcionando"
        },
        {
            "origen": r"c:\simafiweb\venv\Scripts\tributario\tributario_app\models.py",
            "destino": "models_funcionando.py",
            "descripcion": "Modelos Django funcionando"
        }
    ]
    
    archivos_copiados = 0
    archivos_error = 0
    
    for archivo in archivos_respaldo:
        try:
            origen = archivo["origen"]
            destino = os.path.join(backup_dir, archivo["destino"])
            
            if os.path.exists(origen):
                shutil.copy2(origen, destino)
                print(f"✅ {archivo['descripcion']}")
                print(f"   📁 {origen} → {destino}")
                archivos_copiados += 1
            else:
                print(f"⚠️ Archivo no encontrado: {origen}")
                archivos_error += 1
                
        except Exception as e:
            print(f"❌ Error copiando {archivo['origen']}: {e}")
            archivos_error += 1
    
    # Copiar documentación
    try:
        doc_origen = "c:/simafiweb/RESPALDO_PRODUCTOS_CONTROLADOS_FUNCIONANDO.md"
        doc_destino = os.path.join(backup_dir, "DOCUMENTACION_RESPALDO.md")
        if os.path.exists(doc_origen):
            shutil.copy2(doc_origen, doc_destino)
            print(f"✅ Documentación copiada")
            archivos_copiados += 1
    except Exception as e:
        print(f"❌ Error copiando documentación: {e}")
        archivos_error += 1
    
    # Crear archivo de información del respaldo
    info_respaldo = f"""# INFORMACIÓN DEL RESPALDO

**Fecha de creación:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
**Estado:** FUNCIONANDO CORRECTAMENTE
**Problema resuelto:** Productos controlados - formato decimal y separación de miles

## ARCHIVOS RESPALDADOS

### Archivos Principales:
- views_funcionando.py (Backend Django)
- declaracion_volumen_interactivo_funcionando.js (JavaScript principal)
- declaracion_volumen_funcionando.html (Template HTML)
- urls_funcionando.py (Configuración URLs)
- forms_funcionando.py (Formularios Django)
- models_funcionando.py (Modelos Django)

### Funcionalidades Implementadas:
1. ✅ Parsing mejorado de formatos numéricos (50,000.00 → 50000.00)
2. ✅ Sistema de variables ocultas para cálculos independientes
3. ✅ Consulta de tarifas reales desde tabla tarifasimptoics
4. ✅ Campo 'controlado' corregido en backend
5. ✅ API para obtener tarifas por categoría

### Resultado:
- Usuario ingresa: 50,000.00
- Sistema calcula: L. 5.00 (según tarifas BD)
- Estado: ✅ FUNCIONANDO

## INSTRUCCIONES DE RESTAURACIÓN

Para restaurar este respaldo funcionando:

1. Copiar views_funcionando.py → views.py
2. Copiar declaracion_volumen_interactivo_funcionando.js → declaracion_volumen_interactivo.js
3. Copiar declaracion_volumen_funcionando.html → declaracion_volumen.html
4. Copiar urls_funcionando.py → urls.py
5. Reiniciar servidor Django

⚠️ IMPORTANTE: Este respaldo contiene código FUNCIONANDO CORRECTAMENTE
"""
    
    try:
        info_path = os.path.join(backup_dir, "INSTRUCCIONES_RESPALDO.md")
        with open(info_path, 'w', encoding='utf-8') as f:
            f.write(info_respaldo)
        print(f"✅ Archivo de información creado")
        archivos_copiados += 1
    except Exception as e:
        print(f"❌ Error creando archivo de información: {e}")
        archivos_error += 1
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN DEL RESPALDO:")
    print(f"   ✅ Archivos copiados: {archivos_copiados}")
    print(f"   ❌ Errores: {archivos_error}")
    print(f"   📁 Directorio: {backup_dir}")
    
    if archivos_error == 0:
        print("\n🎉 ¡RESPALDO CREADO EXITOSAMENTE!")
        print("🔒 Todos los archivos funcionando han sido respaldados")
        return True
    else:
        print(f"\n⚠️ Respaldo creado con {archivos_error} errores")
        return False

if __name__ == "__main__":
    crear_respaldo_funcionando()










