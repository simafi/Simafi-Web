#!/usr/bin/env python
"""
Script de prueba para diagnosticar por qué no se muestran los factores de riego en el combobox
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, r'C:\simafiweb\venv\Scripts\tributario')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

from django.db import connection
from catastro.models import FactoresRiego
import traceback

def test_direct_sql():
    """Prueba consulta SQL directa"""
    print("=" * 80)
    print("TEST 1: Consulta SQL Directa")
    print("=" * 80)
    try:
        with connection.cursor() as cursor:
            # Probar diferentes variaciones de la consulta
            queries = [
                ("SELECT codigo, descripcion, valor FROM factoresriego ORDER BY codigo", "Sin backticks"),
                ("SELECT `codigo`, `descripcion`, `valor` FROM `factoresriego` ORDER BY `codigo`", "Con backticks"),
                ("SELECT COUNT(*) as total FROM factoresriego", "Conteo total"),
                ("SHOW TABLES LIKE 'factoresriego'", "Verificar tabla existe"),
            ]
            
            for query, descripcion in queries:
                print(f"\n--- {descripcion} ---")
                print(f"Query: {query}")
                try:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    print(f"✅ Éxito: {len(rows)} filas obtenidas")
                    if rows:
                        print(f"Primeras 3 filas:")
                        for idx, row in enumerate(rows[:3]):
                            print(f"  Fila {idx+1}: {row}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    print(f"   Tipo: {type(e).__name__}")
    except Exception as e:
        print(f"❌ Error general en SQL directa: {str(e)}")
        traceback.print_exc()

def test_django_model():
    """Prueba usando el modelo Django"""
    print("\n" + "=" * 80)
    print("TEST 2: Modelo Django")
    print("=" * 80)
    try:
        # Probar diferentes consultas
        print("\n--- FactoresRiego.objects.all() ---")
        all_factores = FactoresRiego.objects.all()
        print(f"Total registros: {all_factores.count()}")
        
        if all_factores.exists():
            print("Primeros 3 registros:")
            for idx, factor in enumerate(all_factores[:3]):
                print(f"  {idx+1}. ID={factor.id}, codigo='{factor.codigo}', descripcion='{factor.descripcion}', valor={factor.valor}, empresa='{factor.empresa}'")
        
        print("\n--- FactoresRiego.objects.values('codigo', 'descripcion', 'valor') ---")
        valores = list(FactoresRiego.objects.values('codigo', 'descripcion', 'valor'))
        print(f"Total registros: {len(valores)}")
        if valores:
            print("Primeros 3 registros:")
            for idx, val in enumerate(valores[:3]):
                print(f"  {idx+1}. {val}")
        
        print("\n--- FactoresRiego.objects.filter(empresa='0301') ---")
        filtrados = FactoresRiego.objects.filter(empresa='0301')
        print(f"Total registros con empresa='0301': {filtrados.count()}")
        if filtrados.exists():
            print("Primeros 3 registros:")
            for idx, factor in enumerate(filtrados[:3]):
                print(f"  {idx+1}. codigo='{factor.codigo}', descripcion='{factor.descripcion}', valor={factor.valor}")
        
    except Exception as e:
        print(f"❌ Error en modelo Django: {str(e)}")
        traceback.print_exc()

def test_table_structure():
    """Verifica la estructura de la tabla"""
    print("\n" + "=" * 80)
    print("TEST 3: Estructura de la Tabla")
    print("=" * 80)
    try:
        with connection.cursor() as cursor:
            cursor.execute("DESCRIBE factoresriego")
            columns = cursor.fetchall()
            print("Columnas de la tabla factoresriego:")
            for col in columns:
                print(f"  {col}")
            
            cursor.execute("SHOW INDEX FROM factoresriego")
            indexes = cursor.fetchall()
            print("\nÍndices de la tabla factoresriego:")
            for idx in indexes:
                print(f"  {idx}")
    except Exception as e:
        print(f"❌ Error al verificar estructura: {str(e)}")
        traceback.print_exc()

def test_data_format():
    """Prueba el formato de datos que se pasa al template"""
    print("\n" + "=" * 80)
    print("TEST 4: Formato de Datos para Template")
    print("=" * 80)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT codigo, descripcion, valor FROM factoresriego ORDER BY codigo LIMIT 5")
            rows = cursor.fetchall()
            
            factores_riego = []
            for idx, row in enumerate(rows):
                try:
                    codigo = str(row[0]).strip() if row[0] is not None else ''
                    descripcion = str(row[1]).strip() if row[1] is not None else ''
                    valor = float(row[2]) if row[2] is not None else 0.00
                    
                    factor_dict = {
                        'codigo': codigo,
                        'descripcion': descripcion,
                        'valor': valor
                    }
                    factores_riego.append(factor_dict)
                    
                    print(f"Registro {idx+1}:")
                    print(f"  Tipo codigo: {type(codigo)}, Valor: '{codigo}'")
                    print(f"  Tipo descripcion: {type(descripcion)}, Valor: '{descripcion}'")
                    print(f"  Tipo valor: {type(valor)}, Valor: {valor}")
                    print(f"  Dict completo: {factor_dict}")
                    print()
                except Exception as e_row:
                    print(f"❌ Error procesando fila {idx}: {str(e_row)}")
                    print(f"   Fila raw: {row}")
            
            print(f"Total factores_riego procesados: {len(factores_riego)}")
            print(f"Tipo de factores_riego: {type(factores_riego)}")
            if factores_riego:
                print(f"Ejemplo de estructura: {factores_riego[0]}")
    except Exception as e:
        print(f"❌ Error en formato de datos: {str(e)}")
        traceback.print_exc()

def test_variable_conflicts():
    """Verifica conflictos de variables"""
    print("\n" + "=" * 80)
    print("TEST 5: Verificación de Conflictos de Variables")
    print("=" * 80)
    
    # Simular el contexto de la vista
    factores_riego = []
    factores_riego_queryset = None
    
    try:
        # Probar la misma lógica que en la vista
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT codigo, descripcion, valor FROM factoresriego ORDER BY codigo")
            rows = cursor.fetchall()
            
            factores_riego = []
            for idx, row in enumerate(rows):
                codigo = str(row[0]).strip() if row[0] is not None else ''
                descripcion = str(row[1]).strip() if row[1] is not None else ''
                valor = float(row[2]) if row[2] is not None else 0.00
                
                factores_riego.append({
                    'codigo': codigo,
                    'descripcion': descripcion,
                    'valor': valor
                })
        
        print(f"factores_riego (lista): {len(factores_riego)} elementos")
        print(f"Tipo: {type(factores_riego)}")
        
        # Probar con el modelo Django también
        factores_riego_queryset = FactoresRiego.objects.all().order_by('codigo')
        factores_riego_model = list(factores_riego_queryset.values('codigo', 'descripcion', 'valor'))
        
        print(f"factores_riego_model (modelo): {len(factores_riego_model)} elementos")
        print(f"Tipo: {type(factores_riego_model)}")
        
        # Verificar si hay diferencias
        if len(factores_riego) != len(factores_riego_model):
            print(f"⚠️ ADVERTENCIA: Diferencia en cantidad de registros!")
            print(f"   SQL directa: {len(factores_riego)}")
            print(f"   Modelo Django: {len(factores_riego_model)}")
        
        # Verificar estructura
        if factores_riego and factores_riego_model:
            print("\nComparación de estructuras:")
            print(f"SQL directa primer elemento: {factores_riego[0]}")
            print(f"Modelo Django primer elemento: {factores_riego_model[0]}")
            print(f"¿Estructuras iguales? {factores_riego[0].keys() == factores_riego_model[0].keys()}")
        
    except Exception as e:
        print(f"❌ Error en verificación de conflictos: {str(e)}")
        traceback.print_exc()

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("DIAGNÓSTICO: Factores de Riego - Combobox Vacío")
    print("=" * 80)
    
    test_direct_sql()
    test_django_model()
    test_table_structure()
    test_data_format()
    test_variable_conflicts()
    
    print("\n" + "=" * 80)
    print("FIN DEL DIAGNÓSTICO")
    print("=" * 80)








