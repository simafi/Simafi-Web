#!/usr/bin/env python3
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
        
        print("\n📋 COLUMNAS EXISTENTES:")
        columnas_nombres = []
        for columna in columnas:
            nombre = columna[0]
            tipo = columna[1]
            columnas_nombres.append(nombre)
            print(f"  - {nombre}: {tipo}")
        
        # Verificar si cocontrolado existe
        if 'cocontrolado' in columnas_nombres:
            print("\n✅ La columna 'cocontrolado' EXISTE")
        else:
            print("\n❌ La columna 'cocontrolado' NO EXISTE")
            print("\n🔧 SOLUCIÓN: Ejecutar el SQL:")
            print("ALTER TABLE declara ADD COLUMN cocontrolado DECIMAL(16,2) DEFAULT 0.00;")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error conectando a la BD: {e}")
        print("\n📝 PASOS MANUALES:")
        print("1. Conectar a MySQL manualmente")
        print("2. Ejecutar: SHOW COLUMNS FROM declara;")
        print("3. Verificar si existe 'cocontrolado'")

if __name__ == "__main__":
    verificar_tabla_declara()
