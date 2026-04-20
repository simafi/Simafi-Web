#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vista para obtener tarifas reales de la base de datos
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["GET"])
def obtener_tarifas_reales(request):
    """
    Obtiene las tarifas reales de la tabla tarifasimptoics categoría '1'
    """
    try:
        print("🔍 Obteniendo tarifas reales de la base de datos...")
        
        # Importar el modelo
        from tributario_app.models import TarifasImptoics
        
        print("✅ Modelo TarifasImptoics importado correctamente")
        
        # Obtener tarifas de categoría 1
        tarifas = TarifasImptoics.objects.filter(categoria='1').order_by('rango1')
        
        print(f"📊 Total de tarifas encontradas: {tarifas.count()}")
        
        if not tarifas.exists():
            print("❌ No se encontraron tarifas para la categoría '1'")
            return JsonResponse({
                'exito': False,
                'mensaje': 'No se encontraron tarifas para la categoría "1"',
                'tarifas': []
            })
        
        # Convertir a formato JSON
        tarifas_data = []
        for tarifa in tarifas:
            tarifas_data.append({
                'id': tarifa.id,
                'categoria': tarifa.categoria,
                'descripcion': tarifa.descripcion,
                'codigo': tarifa.codigo,
                'rango1': float(tarifa.rango1),
                'rango2': float(tarifa.rango2),
                'valor': float(tarifa.valor)
            })
        
        print(f"✅ Datos convertidos a JSON: {len(tarifas_data)} registros")
        
        return JsonResponse({
            'exito': True,
            'mensaje': f'Se obtuvieron {len(tarifas_data)} tarifas de la categoría "1"',
            'tarifas': tarifas_data
        })
        
    except Exception as e:
        print(f"❌ Error al obtener tarifas: {e}")
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al obtener tarifas: {str(e)}',
            'tarifas': []
        })
