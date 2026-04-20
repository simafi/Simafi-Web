#!/usr/bin/env python3
"""
Script para analizar y corregir el error OperationalError:
Unknown column 'declara.cocontrolado' in 'field list'
"""

import os
from pathlib import Path

def analizar_error_bd():
    """Analiza el error de columna faltante en la base de datos"""
    
    print("🔍 ANÁLISIS DEL ERROR:")
    print("=" * 50)
    print("❌ Error: Unknown column 'declara.cocontrolado' in 'field list'")
    print("📍 Ubicación: modules.tributario.views.declaracion_volumen")
    print("🌐 URL: /tributario/declaracion-volumen/?rtm=114-03-23&expe=1151")
    
    print("\n🔍 CAUSA DEL PROBLEMA:")
    print("1. El código Django está intentando acceder a 'declara.cocontrolado'")
    print("2. Esta columna NO EXISTE en la tabla 'declara' actual")
    print("3. El esquema original muestra: `cocontrolado` DECIMAL(16,2)")
    print("4. Pero la tabla real puede no tener esta columna")

def crear_solucion_inmediata():
    """Crea soluciones para el error de columna faltante"""
    
    # Solución 1: SQL para agregar la columna faltante
    sql_agregar_columna = """-- SOLUCIÓN 1: Agregar columna faltante
-- Ejecutar en la base de datos MySQL

USE tributario_db;  -- Cambiar por el nombre real de la BD

-- Verificar si la columna existe
SHOW COLUMNS FROM declara LIKE 'cocontrolado';

-- Si no existe, agregarla
ALTER TABLE declara 
ADD COLUMN cocontrolado DECIMAL(16,2) DEFAULT 0.00 
AFTER valorexcento;

-- Verificar que se agregó correctamente
DESCRIBE declara;

-- Opcional: Actualizar registros existentes
UPDATE declara SET cocontrolado = 0.00 WHERE cocontrolado IS NULL;
"""
    
    with open("c:/simafiweb/fix_cocontrolado_column.sql", 'w', encoding='utf-8') as f:
        f.write(sql_agregar_columna)
    
    print("✅ SQL creado: fix_cocontrolado_column.sql")

def crear_solucion_alternativa():
    """Crea solución alternativa modificando el código Django"""
    
    # Solución 2: Modificar el modelo Django para manejar la columna faltante
    solucion_django = '''# SOLUCIÓN 2: Modificar modelo Django
# Archivo: models.py

class Declara(models.Model):
    # Campos existentes...
    ventai = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    ventac = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    ventas = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    valorexcento = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    
    # OPCIÓN A: Agregar campo cocontrolado si no existe
    # cocontrolado = models.DecimalField(max_digits=16, decimal_places=2, default=0.00, null=True, blank=True)
    
    # OPCIÓN B: Usar property para mapear a campo existente
    @property
    def cocontrolado(self):
        # Mapear a otro campo existente o retornar 0
        return getattr(self, 'valorexcento', 0.00)
    
    @cocontrolado.setter
    def cocontrolado(self, value):
        # Opcional: guardar en otro campo
        pass

# SOLUCIÓN 3: Modificar la vista para evitar el campo
# En views.py, remover referencias a 'cocontrolado' temporalmente
'''
    
    with open("c:/simafiweb/solucion_django_cocontrolado.py", 'w', encoding='utf-8') as f:
        f.write(solucion_django)
    
    print("✅ Solución Django creada: solucion_django_cocontrolado.py")

def crear_script_verificacion():
    """Crea script para verificar el estado de la base de datos"""
    
    script_verificacion = '''#!/usr/bin/env python3
"""
Script para verificar el estado de la tabla declara
"""

import pymysql
import os

def verificar_tabla_declara():
    """Verifica la estructura de la tabla declara"""
    
    # Configuración de conexión (ajustar según tu BD)
    config = {
        'host': 'localhost',
        'user': 'root',  # Cambiar por tu usuario
        'password': '',  # Cambiar por tu contraseña
        'database': 'tributario_db',  # Cambiar por tu BD
        'charset': 'utf8mb4'
    }
    
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        print("🔍 Verificando estructura de tabla 'declara'...")
        
        # Mostrar columnas existentes
        cursor.execute("SHOW COLUMNS FROM declara")
        columnas = cursor.fetchall()
        
        print("\\n📋 COLUMNAS EXISTENTES:")
        columnas_nombres = []
        for columna in columnas:
            nombre = columna[0]
            tipo = columna[1]
            columnas_nombres.append(nombre)
            print(f"  - {nombre}: {tipo}")
        
        # Verificar si cocontrolado existe
        if 'cocontrolado' in columnas_nombres:
            print("\\n✅ La columna 'cocontrolado' EXISTE")
        else:
            print("\\n❌ La columna 'cocontrolado' NO EXISTE")
            print("\\n🔧 SOLUCIÓN: Ejecutar el SQL:")
            print("ALTER TABLE declara ADD COLUMN cocontrolado DECIMAL(16,2) DEFAULT 0.00;")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error conectando a la BD: {e}")
        print("\\n📝 PASOS MANUALES:")
        print("1. Conectar a MySQL manualmente")
        print("2. Ejecutar: SHOW COLUMNS FROM declara;")
        print("3. Verificar si existe 'cocontrolado'")

if __name__ == "__main__":
    verificar_tabla_declara()
'''
    
    with open("c:/simafiweb/verificar_tabla_declara.py", 'w', encoding='utf-8') as f:
        f.write(script_verificacion)
    
    print("✅ Script verificación creado: verificar_tabla_declara.py")

def crear_migracion_django():
    """Crea una migración Django para agregar la columna"""
    
    migracion = '''# Migración Django para agregar campo cocontrolado
# Ejecutar: python manage.py makemigrations
# Luego: python manage.py migrate

from django.db import migrations, models

class Migration(migrations.Migration):
    
    dependencies = [
        ('tributario_app', '0037_tarifasimptoics_alter_planarbitrio_options_and_more'),
    ]
    
    operations = [
        migrations.AddField(
            model_name='declara',
            name='cocontrolado',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=16),
        ),
    ]
'''
    
    with open("c:/simafiweb/migracion_cocontrolado.py", 'w', encoding='utf-8') as f:
        f.write(migracion)
    
    print("✅ Migración Django creada: migracion_cocontrolado.py")

def main():
    print("🚨 ANÁLISIS Y CORRECCIÓN DEL ERROR COCONTROLADO")
    print("=" * 60)
    
    analizar_error_bd()
    
    print("\n🔧 CREANDO SOLUCIONES...")
    crear_solucion_inmediata()
    crear_solucion_alternativa()
    crear_script_verificacion()
    crear_migracion_django()
    
    print("\n" + "=" * 60)
    print("✅ ANÁLISIS COMPLETADO")
    
    print("\n🎯 SOLUCIONES DISPONIBLES:")
    print("\n1️⃣ SOLUCIÓN RÁPIDA (Recomendada):")
    print("   - Ejecutar: fix_cocontrolado_column.sql")
    print("   - Agrega la columna faltante a la BD")
    
    print("\n2️⃣ SOLUCIÓN DJANGO:")
    print("   - Copiar migracion_cocontrolado.py al directorio migrations/")
    print("   - Ejecutar: python manage.py migrate")
    
    print("\n3️⃣ VERIFICACIÓN:")
    print("   - Ejecutar: python verificar_tabla_declara.py")
    print("   - Confirma si la columna existe")
    
    print("\n⚠️ CAUSA DEL ERROR:")
    print("   - Django intenta acceder a 'declara.cocontrolado'")
    print("   - Esta columna no existe en la tabla actual")
    print("   - Necesita ser agregada a la base de datos")

if __name__ == "__main__":
    main()
