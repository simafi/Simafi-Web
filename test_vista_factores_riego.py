#!/usr/bin/env python
"""
Script que simula exactamente lo que hace la vista terreno_rural_form
para identificar el problema con factores_riego
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

def simular_vista():
    """Simula exactamente la lógica de la vista"""
    print("=" * 80)
    print("SIMULACIÓN: Lógica de terreno_rural_form")
    print("=" * 80)
    
    # Inicializar como en la vista
    factores_riego = []
    
    print(f"\n1. Estado inicial: factores_riego = {factores_riego}")
    print(f"   Tipo: {type(factores_riego)}")
    print(f"   Longitud: {len(factores_riego)}")
    
    try:
        from django.db import connection
        
        print("\n2. Iniciando consulta SQL directa...")
        
        # Usar consulta SQL directa para obtener los factores de riego de la tabla factoresriego
        with connection.cursor() as cursor:
            # Consulta directa a la tabla factoresriego
            cursor.execute("SELECT codigo, descripcion, valor FROM factoresriego ORDER BY codigo")
            rows = cursor.fetchall()
            
            print(f"   ✅ Se obtuvieron {len(rows)} filas de la consulta directa.")
            
            # Convertir los resultados a lista de diccionarios
            factores_riego = []
            print(f"   ⚠️  Re-inicializando factores_riego como lista vacía")
            
            for idx, row in enumerate(rows):
                try:
                    codigo = str(row[0]).strip() if row[0] is not None else ''
                    descripcion = str(row[1]).strip() if row[1] is not None else ''
                    valor = float(row[2]) if row[2] is not None else 0.00
                    
                    factores_riego.append({
                        'codigo': codigo,
                        'descripcion': descripcion,
                        'valor': valor
                    })
                    
                    # Mostrar los primeros 3 registros
                    if idx < 3:
                        print(f"   Registro {idx+1}: codigo='{codigo}', descripcion='{descripcion}', valor={valor}")
                except Exception as e_row:
                    print(f"   ❌ Error procesando fila {idx}: {str(e_row)}")
            
            print(f"\n3. Después del procesamiento:")
            print(f"   factores_riego tiene {len(factores_riego)} elementos")
            print(f"   Tipo: {type(factores_riego)}")
            if factores_riego:
                print(f"   Primer elemento: {factores_riego[0]}")
            
            if len(factores_riego) > 0:
                print(f"   ✅ Se encontraron {len(factores_riego)} factores de riego para el combobox.")
            else:
                print(f"   ⚠️  No se encontraron factores de riego después de procesar las filas.")
                
    except Exception as e:
        # Si hay error, intentar con el modelo como fallback
        import traceback
        error_trace = traceback.format_exc()
        print(f"\n   ❌ Error en consulta SQL directa: {str(e)}")
        print(f"   Traceback: {error_trace[:500]}")
        
        try:
            print("\n4. Intentando fallback con modelo Django...")
            factores_riego_queryset = FactoresRiego.objects.all().order_by('codigo')
            factores_riego = list(factores_riego_queryset.values('codigo', 'descripcion', 'valor'))
            if len(factores_riego) > 0:
                print(f"   ✅ Usando modelo Django como fallback. Encontrados: {len(factores_riego)} factores.")
            else:
                print(f"   ⚠️  Modelo Django tampoco devolvió datos.")
        except Exception as e2:
            error_msg = f'Error modelo Django: {str(e2)}'
            print(f"   ❌ {error_msg}")
            factores_riego = []
    
    # Verificar que factores_riego tenga datos antes de pasarlo al contexto
    print(f"\n5. Verificación final antes del contexto:")
    print(f"   factores_riego: {factores_riego}")
    print(f"   Tipo: {type(factores_riego)}")
    print(f"   Longitud: {len(factores_riego) if factores_riego else 0}")
    print(f"   ¿Está vacío? {not factores_riego or len(factores_riego) == 0}")
    
    if not factores_riego or len(factores_riego) == 0:
        print(f"   ❌ ERROR CRÍTICO: factores_riego está vacío antes de pasar al template.")
    else:
        print(f"   ✅ factores_riego tiene {len(factores_riego)} elementos antes de pasar al template.")
    
    # Simular el contexto
    context = {
        'factores_riego': factores_riego,
    }
    
    print(f"\n6. Contexto creado:")
    print(f"   'factores_riego' en contexto: {'factores_riego' in context}")
    print(f"   Tipo en contexto: {type(context['factores_riego'])}")
    print(f"   Longitud en contexto: {len(context['factores_riego']) if context['factores_riego'] else 0}")
    
    if 'factores_riego' not in context:
        print(f"   ❌ ERROR: factores_riego no está en el contexto!")
    elif not context['factores_riego']:
        print(f"   ❌ ERROR: factores_riego en contexto está vacío.")
    else:
        print(f"   ✅ factores_riego en contexto tiene {len(context['factores_riego'])} elementos.")
    
    # Verificar estructura para el template
    print(f"\n7. Estructura para template:")
    if factores_riego:
        print(f"   Primer elemento: {factores_riego[0]}")
        print(f"   Claves del dict: {list(factores_riego[0].keys())}")
        print(f"   ¿Tiene 'codigo'? {'codigo' in factores_riego[0]}")
        print(f"   ¿Tiene 'descripcion'? {'descripcion' in factores_riego[0]}")
        print(f"   ¿Tiene 'valor'? {'valor' in factores_riego[0]}")
        
        # Simular el loop del template
        print(f"\n8. Simulación del loop del template:")
        print("   {% for factor in factores_riego %}")
        for idx, factor in enumerate(factores_riego[:3]):
            print(f"      factor.codigo = '{factor['codigo']}'")
            print(f"      factor.descripcion = '{factor['descripcion']}'")
            print(f"      <option value=\"{factor['codigo']}\">{factor['codigo']} - {factor['descripcion']}</option>")
        print("   {% endfor %}")
    
    return factores_riego, context

if __name__ == '__main__':
    factores_riego, context = simular_vista()
    
    print("\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"Total factores_riego: {len(factores_riego)}")
    print(f"¿Lista vacía? {not factores_riego}")
    print(f"¿En contexto? {'factores_riego' in context}")
    print(f"¿Contexto tiene datos? {bool(context.get('factores_riego'))}")

