"""
Vista AJAX simple para obtener tarifas escalonadas
"""

from django.http import JsonResponse

def obtener_tarifas_escalonadas_simple(request):
    """
    Vista AJAX simple para probar la conexión
    """
    print("DEBUG: Vista AJAX simple llamada")
    
    if request.method == 'POST':
        try:
            print("DEBUG: Método POST recibido")
            
            # Importar el modelo
            from tributario_app.models import TarifasImptoics
            print("DEBUG: Modelo importado correctamente")
            
            # Verificar conexión
            total_registros = TarifasImptoics.objects.count()
            print(f"DEBUG: Total registros: {total_registros}")
            
            # Obtener datos de categoría 1
            tarifas = TarifasImptoics.objects.filter(categoria='1').order_by('rango1')
            tarifas_count = tarifas.count()
            print(f"DEBUG: Tarifas categoría 1: {tarifas_count}")
            
            if tarifas_count == 0:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'No hay registros para categoría 1',
                    'debug': {
                        'total_registros': total_registros,
                        'tarifas_categoria_1': tarifas_count
                    }
                })
            
            # Construir estructura
            estructura = []
            for tarifa in tarifas:
                estructura.append({
                    'id': tarifa.id,
                    'rango1': float(tarifa.rango1),
                    'rango2': float(tarifa.rango2),
                    'valor': float(tarifa.valor),
                    'descripcion': tarifa.descripcion or ''
                })
            
            print(f"DEBUG: Estructura generada con {len(estructura)} elementos")
            
            return JsonResponse({
                'exito': True,
                'estructura': estructura,
                'debug': {
                    'total_registros': total_registros,
                    'tarifas_categoria_1': tarifas_count
                }
            })
            
        except Exception as e:
            print(f"DEBUG: Error: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })
