from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def buscar_identificacion(request):
    """Vista AJAX para buscar identificación por DNI"""
    try:
        # Obtener datos tanto de GET como de POST
        if request.method == 'GET':
            identidad = request.GET.get('identidad', '')
        elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                identidad = data.get('identidad', '')
            except json.JSONDecodeError:
                # Si no es JSON, intentar con form data
                identidad = request.POST.get('identidad', '')
        else:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Método no permitido'
            })
        
        print(f"[DEBUG] Buscando identificación: identidad={identidad}")
        
        if identidad:
            from tributario.models import Identificacion
            try:
                identificacion = Identificacion.objects.get(identidad=identidad)
                
                print(f"[OK] Identificación encontrada: {identificacion.nombres} {identificacion.apellidos}")
                
                return JsonResponse({
                    'exito': True,
                    'encontrado': True,
                    'identificacion': {
                        'identidad': identificacion.identidad,
                        'nombres': identificacion.nombres or '',
                        'apellidos': identificacion.apellidos or '',
                        'nombre_completo': f"{identificacion.nombres or ''} {identificacion.apellidos or ''}".strip(),
                        'fechanac': identificacion.fechanac.strftime('%Y-%m-%d') if identificacion.fechanac else None
                    }
                })
            except Identificacion.DoesNotExist:
                print(f"[ERROR] Identificación no encontrada: identidad={identidad}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Identidad no encontrada'
                })
            except Exception as e:
                print(f"[ERROR] Error al buscar identificación: {e}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'Error al buscar identificación: {str(e)}'
                })
        else:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Número de identidad es obligatorio'
            })
            
    except Exception as e:
        print(f"[ERROR] Error general en buscar_identificacion: {e}")
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error en el servidor: {str(e)}'
        })
