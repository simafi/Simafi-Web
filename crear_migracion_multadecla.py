#!/usr/bin/env python3
"""
Script para crear migración manual del campo multadecla
"""

import os
import sys
from datetime import datetime

def crear_migracion_multadecla():
    """Crea una migración manual para agregar el campo multadecla"""
    
    # Contenido de la migración
    migracion_content = f'''# Generated manually for multadecla field
# Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tributario_app', '0001_initial'),  # Ajustar según la última migración
    ]

    operations = [
        migrations.AddField(
            model_name='declaracionvolumen',
            name='multadecla',
            field=models.DecimalField(
                blank=True, 
                decimal_places=2, 
                default=0.0, 
                max_digits=12, 
                null=True, 
                verbose_name='Multa Declaración Tardía'
            ),
        ),
    ]
'''
    
    # Directorio de migraciones
    migraciones_dir = r'c:\simafiweb\venv\Scripts\tributario\tributario_app\migrations'
    
    # Verificar si el directorio existe
    if not os.path.exists(migraciones_dir):
        print(f"❌ Directorio de migraciones no encontrado: {migraciones_dir}")
        return False
    
    # Buscar el número de la siguiente migración
    archivos_migracion = [f for f in os.listdir(migraciones_dir) if f.startswith('00') and f.endswith('.py')]
    if archivos_migracion:
        numeros = [int(f[:4]) for f in archivos_migracion if f[:4].isdigit()]
        siguiente_numero = max(numeros) + 1 if numeros else 2
    else:
        siguiente_numero = 2
    
    # Nombre del archivo de migración
    nombre_archivo = f'{siguiente_numero:04d}_add_multadecla_field.py'
    ruta_migracion = os.path.join(migraciones_dir, nombre_archivo)
    
    try:
        # Escribir el archivo de migración
        with open(ruta_migracion, 'w', encoding='utf-8') as f:
            f.write(migracion_content)
        
        print(f"✅ Migración creada exitosamente: {nombre_archivo}")
        print(f"📁 Ubicación: {ruta_migracion}")
        print(f"🔄 Para aplicar, ejecutar: python manage.py migrate")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando migración: {e}")
        return False

def verificar_estructura_proyecto():
    """Verifica que la estructura del proyecto sea correcta"""
    
    rutas_verificar = [
        r'c:\simafiweb\venv\Scripts\tributario\tributario_app\models.py',
        r'c:\simafiweb\venv\Scripts\tributario\tributario_app\forms.py',
        r'c:\simafiweb\venv\Scripts\tributario\tributario_app\migrations',
        r'c:\simafiweb\venv\Scripts\manage.py'
    ]
    
    print("🔍 VERIFICANDO ESTRUCTURA DEL PROYECTO:")
    print("=" * 40)
    
    for ruta in rutas_verificar:
        if os.path.exists(ruta):
            tipo = "📁 Directorio" if os.path.isdir(ruta) else "📄 Archivo"
            print(f"✅ {tipo}: {ruta}")
        else:
            print(f"❌ No encontrado: {ruta}")
    
    return True

def main():
    print("🚀 CREADOR DE MIGRACIÓN PARA CAMPO MULTADECLA")
    print("=" * 50)
    
    # Verificar estructura
    verificar_estructura_proyecto()
    
    print("\n📝 CREANDO MIGRACIÓN MANUAL...")
    if crear_migracion_multadecla():
        print("\n🎯 MIGRACIÓN CREADA EXITOSAMENTE")
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. cd c:\\simafiweb\\venv\\Scripts")
        print("2. python manage.py migrate")
        print("3. python manage.py runserver 8080")
    else:
        print("\n❌ ERROR AL CREAR MIGRACIÓN")
        print("Verificar permisos y estructura del proyecto")

if __name__ == "__main__":
    main()










