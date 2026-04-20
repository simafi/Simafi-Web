from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Departamento
from .forms import DepartamentoForm


def departamento_crud(request):
    """Vista CRUD para Departamentos"""
    mensaje = None
    exito = False
    departamento = None
    
    if request.method == 'POST':
        action = request.POST.get('action', 'guardar')
        
        if action == 'guardar':
            # Crear nuevo departamento
            form = DepartamentoForm(request.POST)
            if form.is_valid():
                try:
                    departamento = form.save()
                    mensaje = f"Departamento '{departamento.depto}' creado exitosamente."
                    exito = True
                    form = DepartamentoForm()  # Limpiar formulario
                except Exception as e:
                    mensaje = f"Error al crear el departamento: {str(e)}"
                    exito = False
            else:
                mensaje = "Por favor, corrija los errores en el formulario."
                exito = False
                
        elif action == 'actualizar':
            # Actualizar departamento existente
            codigo = request.POST.get('depto') or request.POST.get('codigo')
            try:
                departamento = Departamento.objects.get(depto=codigo)
                form = DepartamentoForm(request.POST, instance=departamento)
                if form.is_valid():
                    departamento = form.save()
                    mensaje = f"Departamento '{departamento.depto}' actualizado exitosamente."
                    exito = True
                    form = DepartamentoForm()  # Limpiar formulario
                else:
                    mensaje = "Por favor, corrija los errores en el formulario."
                    exito = False
            except Departamento.DoesNotExist:
                mensaje = f"No se encontró el departamento con código {codigo}."
                exito = False
                form = DepartamentoForm()
                
        elif action == 'eliminar':
            # Eliminar departamento
            codigo = request.POST.get('depto') or request.POST.get('codigo')
            try:
                departamento = Departamento.objects.get(depto=codigo)
                codigo_eliminado = departamento.depto
                departamento.delete()
                mensaje = f"Departamento '{codigo_eliminado}' eliminado exitosamente."
                exito = True
                form = DepartamentoForm()
            except Departamento.DoesNotExist:
                mensaje = f"No se encontró el departamento con código {codigo}."
                exito = False
                form = DepartamentoForm()
                
        elif action == 'nuevo':
            # Limpiar formulario para nuevo departamento
            form = DepartamentoForm()
            mensaje = "Formulario listo para nuevo departamento."
            exito = True
    else:
        # GET request - mostrar formulario vacío
        form = DepartamentoForm()
    
    # Obtener todos los departamentos para la tabla
    departamentos = Departamento.objects.all().order_by('depto')
    
    context = {
        'form': form,
        'departamentos': departamentos,
        'mensaje': mensaje,
        'exito': exito,
    }
    
    return render(request, 'formulario_departamento.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def buscar_departamento(request):
    """Vista AJAX para buscar departamento"""
    try:
        data = json.loads(request.body)
        codigo = data.get('codigo', '').strip()
        
        if not codigo:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Código es requerido'
            })
        
        # Buscar el departamento en la base de datos
        try:
            departamento = Departamento.objects.get(depto=codigo)
            return JsonResponse({
                'exito': True,
                'departamento': {
                    'depto': departamento.depto,
                    'codigo': departamento.depto,
                    'descripcion': departamento.descripcion,
                }
            })
        except Departamento.DoesNotExist:
            return JsonResponse({
                'exito': False,
                'mensaje': f'No se encontró el departamento con código {codigo}'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'exito': False,
            'mensaje': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error interno: {str(e)}'
        })







