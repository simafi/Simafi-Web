#!/usr/bin/env python
"""
Consulta las tarifas reales de la tabla tarifasimptoics
"""

import os
import sys

def consultar_tarifas_reales():
    """
    Consulta la tabla tarifasimptoics para obtener rangos y valores reales
    """
    print("🔍 CONSULTANDO TARIFAS REALES DE BASE DE DATOS")
    print("=" * 50)
    
    # Buscar archivos de configuración de base de datos
    posibles_configs = [
        r"c:\simafiweb\venv\Scripts\tributario\tributario\settings.py",
        r"c:\simafiweb\venv\Scripts\tributario\tributario_app\models.py",
        r"c:\simafiweb\settings.py"
    ]
    
    print("📋 ESTRUCTURA ESPERADA TABLA 'tarifasimptoics':")
    print("   • rango1: DECIMAL - Límite inferior del rango")
    print("   • rango2: DECIMAL - Límite superior del rango") 
    print("   • valor: DECIMAL - Tarifa por mil a aplicar")
    print("   • categoria: INT - Categoría de la tarifa")
    print()
    
    # Generar consulta SQL para obtener tarifas
    consulta_sql = """
    SELECT 
        rango1,
        rango2, 
        valor,
        categoria,
        descripcion
    FROM tarifasimptoics 
    WHERE categoria = 1 
    ORDER BY rango1 ASC;
    """
    
    print("📝 CONSULTA SQL PARA OBTENER TARIFAS:")
    print(consulta_sql)
    print()
    
    # Crear script para ejecutar consulta
    script_consulta = f"""
import mysql.connector
import json

def obtener_tarifas():
    try:
        # Configuración de conexión (ajustar según su BD)
        config = {{
            'host': 'localhost',
            'user': 'root',  # Ajustar usuario
            'password': '',  # Ajustar contraseña
            'database': 'tributario'  # Ajustar nombre BD
        }}
        
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''{consulta_sql}''')
        tarifas = cursor.fetchall()
        
        print("✅ TARIFAS OBTENIDAS DE BASE DE DATOS:")
        print("=" * 40)
        
        for i, tarifa in enumerate(tarifas, 1):
            rango1 = float(tarifa['rango1'])
            rango2 = float(tarifa['rango2'])
            valor = float(tarifa['valor'])
            
            print(f"Rango {{i}}: ${{rango1:,.0f}} - ${{rango2:,.0f}} = {{valor}}‰")
        
        # Generar JavaScript con tarifas reales
        js_tarifas = []
        for tarifa in tarifas:
            js_tarifa = {{
                'rango1': float(tarifa['rango1']),
                'rango2': float(tarifa['rango2']),
                'valor': float(tarifa['valor']),
                'descripcion': f"Rango ${{float(tarifa['rango1']):,.0f}} - ${{float(tarifa['rango2']):,.0f}}"
            }}
            js_tarifas.append(js_tarifa)
        
        # Guardar en archivo JSON
        with open('tarifas_reales.json', 'w') as f:
            json.dump(js_tarifas, f, indent=2)
        
        print("\\n📄 Tarifas guardadas en: tarifas_reales.json")
        
        cursor.close()
        conn.close()
        
        return js_tarifas
        
    except Exception as e:
        print(f"❌ Error consultando base de datos: {{e}}")
        return None

if __name__ == "__main__":
    obtener_tarifas()
"""
    
    # Escribir script de consulta
    with open('consultar_bd_tarifas.py', 'w', encoding='utf-8') as f:
        f.write(script_consulta)
    
    print("✅ Script de consulta creado: consultar_bd_tarifas.py")
    print()
    print("🔧 PASOS PARA OBTENER TARIFAS REALES:")
    print("   1. Ajuste la configuración de BD en consultar_bd_tarifas.py")
    print("   2. Ejecute: python consultar_bd_tarifas.py")
    print("   3. Se generará tarifas_reales.json con los datos")
    print()
    
    # Crear tarifas de ejemplo basadas en estructura común
    tarifas_ejemplo = [
        {"rango1": 0, "rango2": 1000000, "valor": 2.5, "descripcion": "Primer rango"},
        {"rango1": 1000000, "rango2": 5000000, "valor": 4.0, "descripcion": "Segundo rango"},
        {"rango1": 5000000, "rango2": 10000000, "valor": 6.0, "descripcion": "Tercer rango"},
        {"rango1": 10000000, "rango2": 50000000, "valor": 8.0, "descripcion": "Cuarto rango"},
        {"rango1": 50000000, "rango2": 999999999, "valor": 10.0, "descripcion": "Quinto rango"}
    ]
    
    print("⚠️  USANDO TARIFAS DE EJEMPLO (reemplazar con datos reales):")
    for i, tarifa in enumerate(tarifas_ejemplo, 1):
        print(f"   Rango {i}: ${tarifa['rango1']:,.0f} - ${tarifa['rango2']:,.0f} = {tarifa['valor']}‰")
    
    # Guardar tarifas de ejemplo
    import json
    with open('tarifas_ejemplo.json', 'w') as f:
        json.dump(tarifas_ejemplo, f, indent=2)
    
    print("\n📄 Tarifas de ejemplo guardadas en: tarifas_ejemplo.json")
    
    return tarifas_ejemplo

if __name__ == "__main__":
    consultar_tarifas_reales()
