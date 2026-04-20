from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

# Función helper para asegurar que tasa siempre sea 0 en transacciones
def forzar_tasa_cero(transaccion_id):
    """
    Fuerza el campo tasa a 0.00 usando update directo en BD.
    Se usa después de cualquier operación que modifique transacciones,
    especialmente cuando se calculan recargos moratorios.
    """
    from tributario.models import TransaccionesIcs
    from decimal import Decimal
    try:
        TransaccionesIcs.objects.filter(id=transaccion_id).update(tasa=Decimal('0.00'))
        return True
    except Exception as e:
        print(f"[FORZAR_TASA_CERO] Error forzando tasa a 0 para transacción {transaccion_id}: {e}")
        return False

def simple_redirect(request):
    """Simple redirect view for missing functions"""
    return redirect('tributario:maestro_negocios')

def simple_render(request):
    """Simple render view for missing functions"""
    # Crear un objeto negocio simulado para evitar errores de template
    class NegocioSimulado:
        def __init__(self):
            self.empre = '0301'
            self.rtm = ''
            self.expe = ''
            self.fecha_ini = None
            self.fecha_can = None
            self.identidad = ''
            self.rtnpersonal = ''
            self.comerciante = ''
            self.rtnnego = ''
            self.nombrenego = ''
            self.actividad = ''
            self.identidadrep = ''
            self.representante = ''
            self.estatus = 'A'
            self.catastral = ''
            self.cx = '0.0000000'
            self.cy = '0.0000000'
            self.direccion = ''
            self.telefono = ''
            self.celular = ''
            self.correo = ''
            self.pagweb = ''
            self.socios = ''
            self.comentario = ''
    
    negocio = NegocioSimulado()
    
    return render(request, 'maestro_negocios.html', {
        'negocio': negocio,
        'municipio_codigo': '0301',
        'modulo': 'Tributario',
        'descripcion': 'Gestión de impuestos y tasas municipales'
    })

def declaracion_volumen(request):
    """Vista para declaración de volumen de ventas"""
    from tributario_app.forms import DeclaracionVolumenForm
    from tributario_app.models import DeclaracionVolumen, Negocio, TarifasICS, TasasDecla, Anos
    from django.http import JsonResponse
    import json
    
    # Obtener parámetros de la URL
    rtm = request.GET.get('rtm', '')
    expe = request.GET.get('expe', '')
    ano_param = request.GET.get('ano', '')
    
    # Inicializar variables
    negocio = None
    declaracion = None
    declaraciones = []
    tarifas_ics = []
    tasas_declaracion = []
    mensaje = None
    exito = False
    municipio_codigo = '0301'
    ano_actual = ano_param if ano_param else None
    
    # Buscar negocio si se proporcionan RTM y EXPE
    if rtm and expe:
        try:
            # Buscar el negocio real en la base de datos
            negocio = Negocio.objects.get(
                empre=municipio_codigo,
                rtm=rtm,
                expe=expe
            )
            
            # Buscar declaraciones existentes
            try:
                declaraciones = DeclaracionVolumen.objects.filter(
                    rtm=rtm, 
                    expe=expe
                ).order_by('-ano', '-mes')
            except Exception as e:
                print(f"Error obteniendo declaraciones: {e}")
                declaraciones = []
            
            # Obtener tarifas ICS vinculadas al negocio
            try:
                tarifas_ics = TarifasICS.objects.filter(
                    rtm=rtm,
                    expe=expe
                ).order_by('cod_tarifa')
            except Exception as e:
                print(f"Error obteniendo tarifas ICS: {e}")
                tarifas_ics = []
            
            # Obtener tasas de declaración vinculadas al negocio
            try:
                from tributario_app.models import Rubro
                # Filtrar por empresa, rtm, expe y año (si está disponible)
                filtros_tasas = {
                    'empresa': municipio_codigo,
                    'rtm': rtm,
                    'expe': expe
                }
                
                # Si hay un año específico, agregarlo al filtro
                if ano_actual:
                    filtros_tasas['ano'] = ano_actual
                
                print(f"\n🔍 DEBUG - Filtros para tasasdecla: {filtros_tasas}")
                
                tasas_declaracion_raw = TasasDecla.objects.filter(
                    **filtros_tasas
                ).order_by('-ano', 'rubro')
                
                print(f"🔍 DEBUG - Tasas encontradas (raw): {tasas_declaracion_raw.count()}")
                
                # Enriquecer con información del rubro
                tasas_declaracion = []
                for tasa in tasas_declaracion_raw:
                    tasa_dict = {
                        'id': tasa.id,
                        'empresa': tasa.empresa,
                        'rubro': tasa.rubro,
                        'rubro_nombre': '-',
                        'cod_tarifa': tasa.cod_tarifa,
                        'frecuencia': tasa.frecuencia,
                        'valor': tasa.valor,
                        'nodecla': tasa.nodecla,
                        'ano': tasa.ano,
                        'cuenta': tasa.cuenta,
                        'cuentarez': tasa.cuentarez,
                    }
                    
                    # Obtener nombre del rubro
                    if tasa.rubro:
                        try:
                            rubro_obj = Rubro.objects.get(codigo=tasa.rubro)
                            tasa_dict['rubro_nombre'] = rubro_obj.descripcion
                        except Rubro.DoesNotExist:
                            pass
                    
                    tasas_declaracion.append(tasa_dict)
                
                filtros_str = f"empresa={municipio_codigo}, rtm={rtm}, expe={expe}"
                if ano_actual:
                    filtros_str += f", ano={ano_actual}"
                print(f"Tasas de declaración encontradas: {len(tasas_declaracion)} para {filtros_str}")
            except Exception as e:
                print(f"Error obteniendo tasas de declaración: {e}")
                import traceback
                traceback.print_exc()
                tasas_declaracion = []
                
        except Exception as e:
            print(f"Error procesando negocio: {e}")
            mensaje = f"Error al procesar datos del negocio: {str(e)}"
            tasas_declaracion = []
    
    # Obtener años disponibles
    try:
        anos_disponibles = Anos.objects.all().order_by('-ano')
    except Exception as e:
        print(f"Error obteniendo años: {e}")
        anos_disponibles = []
    
    # Manejar solicitudes POST
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            accion = data.get('accion')
            
            if accion == 'guardar':
                # Crear formulario con los datos recibidos
                form_data = data.get('form_data', {})
                form = DeclaracionVolumenForm(form_data)
                
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.rtm = rtm
                    instance.expe = expe
                    # Asignar el ID del negocio si está disponible
                    if negocio and hasattr(negocio, 'id'):
                        instance.idneg = negocio.id
                    instance.save()
                    
                    return JsonResponse({
                        'exito': True,
                        'mensaje': 'Declaración guardada exitosamente',
                        'impuesto': float(instance.impuesto or 0)
                    })
                else:
                    return JsonResponse({
                        'exito': False,
                        'mensaje': 'Error en la validación del formulario',
                        'errores': form.errors
                    })
            else:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Acción no válida'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Error al procesar los datos JSON'
            })
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error interno: {str(e)}'
            })
    
    # Crear formulario para GET
    initial_data = {}
    if rtm and expe:
        initial_data = {'rtm': rtm, 'expe': expe}
        # Incluir el ID del negocio si está disponible
        if negocio and hasattr(negocio, 'id'):
            initial_data['idneg'] = negocio.id
    
    form = DeclaracionVolumenForm(initial=initial_data)
    
    # Context con todos los datos necesarios para el template
    import time
    timestamp = int(time.time())  # Timestamp para forzar recarga de archivos estáticos
    
    context = {
        'form': form,  # ← CLAVE: Pasar el formulario Django
        'negocio': negocio,
        'rtm': rtm,
        'expe': expe,
        'ano_actual': ano_actual,
        'declaraciones': declaraciones,
        'tarifas_ics': tarifas_ics,
        'tasas_declaracion': tasas_declaracion,
        'anos_disponibles': anos_disponibles,
        'mensaje': mensaje,
        'exito': exito,
        'municipio_codigo': municipio_codigo,
        'modulo': 'Tributario',
        'descripcion': 'Declaración de Volumen de Ventas',
        'timestamp': timestamp  # ← CLAVE: Timestamp para cache busting
    }
    
    return render(request, 'declaracion_volumen.html', context)

@csrf_exempt
def configurar_tasas_negocio(request):
    """Vista para configurar las tasas de un negocio específico"""
    # Importar modelos necesarios
    from tributario_app.models import Negocio, TarifasICS, Rubro, Tarifas
    from tributario_app.forms import TarifasICSForm
    
    # Obtener el municipio del usuario desde la sesión
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    # Obtener datos del negocio desde la URL o POST
    negocio_id = request.GET.get('negocio_id') or request.POST.get('negocio_id')
    rtm = request.GET.get('rtm') or request.POST.get('rtm')
    expe = request.GET.get('expe') or request.POST.get('expe')
    
    # Variables para el contexto
    negocio = None
    tarifas_ics = []
    mensaje = None
    exito = False
    
    # Buscar el negocio
    if negocio_id or (rtm and expe):
        try:
            if negocio_id:
                negocio = Negocio.objects.get(id=negocio_id)
            else:
                negocio = Negocio.objects.get(
                    empre=municipio_codigo,
                    rtm=rtm,
                    expe=expe
                )
        except Negocio.DoesNotExist:
            mensaje = "Negocio no encontrado"
            exito = False
        except Exception as e:
            mensaje = f"Error al buscar negocio: {str(e)}"
            exito = False
    
    # Si no se encontró el negocio, mostrar error
    if not negocio:
        # Crear formulario vacío para el caso de error
        try:
            form = TarifasICSForm()
        except Exception:
            form = None
            
        return render(request, 'configurar_tasas_negocio.html', {
            'negocio': None,
            'form': form,
            'tarifas_ics': [],
            'mensaje': mensaje or "Debe especificar un negocio válido",
            'exito': False,
            'municipio_codigo': municipio_codigo,
            'modulo': 'Tributario',
            'descripcion': 'Configurar Tasas del Negocio'
        })
    
    # Manejar solicitudes POST
    if request.method == 'POST':
        try:
            accion = request.POST.get('accion')
            
            if accion == 'agregar_tarifa':
                # Agregar nueva tarifa ICS
                form = TarifasICSForm(request.POST)
                if form.is_valid():
                    # Obtener datos del formulario
                    rubro = form.cleaned_data.get('rubro')
                    tarifa_rubro = form.cleaned_data.get('tarifa_rubro')
                    valor_personalizado = form.cleaned_data.get('valor_personalizado')
                    
                    # Buscar la tarifa seleccionada para obtener su valor por defecto
                    try:
                        from datetime import datetime
                        ano_vigente = datetime.now().year
                        
                        tarifa = Tarifas.objects.get(
                            empresa=municipio_codigo,
                            rubro=rubro,
                            cod_tarifa=tarifa_rubro,
                            ano=ano_vigente
                        )
                        
                        # Usar el valor personalizado si se proporciona, sino usar el valor de la tarifa
                        valor_final = valor_personalizado if valor_personalizado else tarifa.valor
                        
                        # Crear la tarifa ICS
                        tarifa_ics = TarifasICS(
                            idneg=negocio.id,
                            rtm=negocio.rtm,
                            expe=negocio.expe,
                            cod_tarifa=tarifa_rubro,
                            valor=valor_final
                        )
                        tarifa_ics.save()
                        
                        mensaje = "Tarifa agregada exitosamente"
                        exito = True
                        
                    except Tarifas.DoesNotExist:
                        mensaje = "La tarifa seleccionada no existe"
                        exito = False
                        
                else:
                    mensaje = "Error en el formulario: " + ", ".join([str(error) for error in form.errors.values()])
                    exito = False
                    
            elif accion == 'eliminar_tarifa':
                # Eliminar tarifa ICS
                tarifa_id = request.POST.get('tarifa_id')
                try:
                    tarifa_ics = TarifasICS.objects.get(id=tarifa_id)
                    tarifa_ics.delete()
                    mensaje = "Tarifa eliminada exitosamente"
                    exito = True
                except TarifasICS.DoesNotExist:
                    mensaje = "La tarifa no existe"
                    exito = False
                    
            elif accion == 'actualizar_valor':
                # Actualizar valor de tarifa ICS
                tarifa_id = request.POST.get('tarifa_id')
                nuevo_valor = request.POST.get('nuevo_valor')
                try:
                    tarifa_ics = TarifasICS.objects.get(id=tarifa_id)
                    tarifa_ics.valor = nuevo_valor
                    tarifa_ics.save()
                    mensaje = "Valor actualizado exitosamente"
                    exito = True
                except TarifasICS.DoesNotExist:
                    mensaje = "La tarifa no existe"
                    exito = False
                except ValueError:
                    mensaje = "El valor debe ser un número válido"
                    exito = False
                    
        except Exception as e:
            mensaje = f"Error al procesar la solicitud: {str(e)}"
            exito = False
    
    # Obtener las tarifas ICS configuradas para este negocio
    try:
        if negocio:
            tarifas_ics = TarifasICS.objects.filter(
                rtm=negocio.rtm,
                expe=negocio.expe
            ).order_by('cod_tarifa')
        else:
            tarifas_ics = []
    except Exception as e:
        tarifas_ics = []
        if not mensaje:
            mensaje = f"Error al cargar tarifas: {str(e)}"
            exito = False
    
    # Crear el formulario para agregar nuevas tarifas
    try:
        form = TarifasICSForm()
    except Exception as e:
        form = None
        if not mensaje:
            mensaje = f"Error al crear formulario: {str(e)}"
            exito = False
    
    return render(request, 'configurar_tasas_negocio.html', {
        'negocio': negocio,
        'form': form,
        'tarifas_ics': tarifas_ics,
        'mensaje': mensaje,
        'exito': exito,
        'municipio_codigo': municipio_codigo,
        'modulo': 'Tributario',
        'descripcion': 'Configurar Tasas del Negocio'
    })

@csrf_exempt
def obtener_tarifas_rubro(request):
    """Vista AJAX para obtener las tarifas de un rubro específico"""
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        rubro_codigo = request.POST.get('rubro', '').strip()
        municipio_codigo = request.session.get('municipio_codigo', '0301')
        
        if not rubro_codigo:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Código de rubro requerido'
            })
        
        # Buscar tarifas del rubro
        from tributario_app.models import Tarifas
        from datetime import datetime
        
        ano_vigente = datetime.now().year
        
        tarifas = Tarifas.objects.filter(
            empresa=municipio_codigo,
            rubro=rubro_codigo,
            ano=ano_vigente,
            categoria='C'  # Solo tarifas comerciales
        ).order_by('cod_tarifa')
        
        # Convertir a lista de diccionarios
        tarifas_data = []
        for tarifa in tarifas:
            tarifas_data.append({
                'cod_tarifa': tarifa.cod_tarifa,
                'descripcion': tarifa.descripcion,
                'valor': float(tarifa.valor),
                'frecuencia': tarifa.frecuencia,
                'tipo': tarifa.tipo
            })
        
        return JsonResponse({
            'exito': True,
            'tarifas': tarifas_data
        })
        
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al obtener tarifas: {str(e)}'
        })

def validar_plan_arbitrio(request):
    """
    Vista AJAX para validar si existe un plan de arbitrio según la clave única planarbitio_idx1
    """
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        import json
        from django.http import JsonResponse
        from tributario_app.models import PlanArbitrio
        
        # Obtener datos del request
        data = json.loads(request.body)
        empresa = data.get('empresa', '').strip()
        rubro = data.get('rubro', '').strip()
        cod_tarifa = data.get('cod_tarifa', '').strip()
        ano = data.get('ano', '').strip()
        codigo = data.get('codigo', '').strip()
        
        # Validar que todos los campos estén presentes
        if not all([empresa, rubro, cod_tarifa, ano, codigo]):
            return JsonResponse({
                'exito': False,
                'mensaje': 'Todos los campos de la clave única son requeridos'
            })
        
        # Buscar el plan de arbitrio existente según la clave única planarbitio_idx1
        try:
            plan_existente = PlanArbitrio.objects.get(
                empresa=empresa,
                rubro=rubro,
                cod_tarifa=cod_tarifa,
                ano=ano,
                codigo=codigo
            )
            
            # Si existe, retornar los datos
            return JsonResponse({
                'exito': True,
                'existe': True,
                'concepto': {
                    'id': plan_existente.id,
                    'empresa': plan_existente.empresa,
                    'rubro': plan_existente.rubro,
                    'cod_tarifa': plan_existente.cod_tarifa,
                    'ano': str(plan_existente.ano),
                    'codigo': plan_existente.codigo,
                    'descripcion': plan_existente.descripcion,
                    'minimo': str(plan_existente.minimo),
                    'maximo': str(plan_existente.maximo),
                    'valor': str(plan_existente.valor)
                },
                'mensaje': 'Plan de arbitrio existente encontrado'
            })
            
        except PlanArbitrio.DoesNotExist:
            # No existe, retornar que no se encontró
            return JsonResponse({
                'exito': True,
                'existe': False,
                'mensaje': 'No se encontró un plan de arbitrio con esos criterios'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'exito': False,
            'mensaje': 'Error al procesar los datos JSON'
        })
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error interno: {str(e)}'
        })

def simple_ajax(request):
    """Simple AJAX response for missing functions"""
    return JsonResponse({
        'exito': False,
        'mensaje': 'Función no implementada aún'
    })
