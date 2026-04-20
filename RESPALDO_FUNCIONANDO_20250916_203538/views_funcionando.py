from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

def tributario_login(request):
    """Vista de login del módulo tributario"""
    # Redirigir directamente al menú general del tributario
    return redirect('tributario:tributario_menu_principal')

def tributario_logout(request):
    """Vista de logout del módulo tributario"""
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('core:menu_principal')

def tributario_menu_principal(request):
    """Menú principal del módulo tributario"""
    return render(request, 'menugeneral.html', {
        'modulo': 'Tributario',
        'descripcion': 'Gestión de impuestos y tasas municipales'
    })

# Vistas para las funcionalidades del menugeneral.html
@csrf_exempt
def maestro_negocios(request):
    """Vista para maestro de negocios"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Manejar solicitudes POST para acciones AJAX
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            accion = data.get('accion')
            
            if accion == 'salvar':
                return handle_salvar_negocio(request, data)
            elif accion == 'eliminar':
                return handle_eliminar_negocio(request, data)
            elif accion == 'configuracion':
                # Redirigir a la página de configuración de tasas
                rtm = data.get('rtm', '')
                expe = data.get('expe', '')
                if rtm and expe:
                    return JsonResponse({
                        'exito': True,
                        'redirect': f'/tributario/configurar-tasas-negocio/?rtm={rtm}&expe={expe}'
                    })
                else:
                    return JsonResponse({
                        'exito': False,
                        'mensaje': 'RTM y Expediente son requeridos para configurar tasas'
                    })
            elif accion == 'declaracion':
                # Redirigir a la página de declaración de volumen
                rtm = data.get('rtm', '')
                expe = data.get('expe', '')
                if rtm and expe:
                    return JsonResponse({
                        'exito': True,
                        'redirect': f'/tributario/declaracion-volumen/?rtm={rtm}&expe={expe}'
                    })
                else:
                    return JsonResponse({
                        'exito': False,
                        'mensaje': 'RTM y Expediente son requeridos para declaración de volumen'
                    })
            else:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Acción no válida'
                })
        except json.JSONDecodeError:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Datos JSON inválidos'
            })
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error en el servidor: {str(e)}'
            })
    
    # Manejar solicitudes GET para mostrar el formulario
    # Crear un objeto negocio vacío para el formulario
    negocio = {
        'empre': empresa,
        'rtm': '',
        'expe': '',
        'fecha_ini': '',
        'fecha_can': '',
        'identidad': '',
        'rtnpersonal': '',
        'comerciante': '',
        'rtnnego': '',
        'nombrenego': '',
        'actividad': '',
        'identidadrep': '',
        'representante': '',
        'estatus': 'A',
        'catastral': '',
        'cx': '0.0000000',
        'cy': '0.0000000',
        'direccion': '',
        'telefono': '',
        'celular': '',
        'correo': '',
        'pagweb': '',
        'socios': '',
        'comentario': ''
    }
    
    # Obtener actividades económicas desde la tabla actividad
    try:
        from tributario_app.models import Actividad
        actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
        actividades_list = [
            {'codigo': act.codigo, 'descripcion': act.descripcion}
            for act in actividades
        ]
    except Exception as e:
        # Si hay error, usar datos de ejemplo
        actividades_list = [
            {'codigo': '001', 'descripcion': 'Comercio al por menor'},
            {'codigo': '002', 'descripcion': 'Servicios profesionales'},
            {'codigo': '003', 'descripcion': 'Industria manufacturera'},
            {'codigo': '004', 'descripcion': 'Servicios de transporte'},
            {'codigo': '005', 'descripcion': 'Servicios financieros'}
        ]
    
    return render(request, 'maestro_negocios_optimizado.html', {
        'negocio': negocio,
        'actividades': actividades_list,
        'empresa': empresa,
        'modulo': 'Tributario',
        'descripcion': 'Maestro de Negocios'
    })

def handle_salvar_negocio(request, data):
    """Maneja el guardado de un negocio"""
    try:
        from tributario_app.models import Negocio
        
        # Función auxiliar para truncar campos según max_length
        def truncar_campo(valor, max_length):
            if valor and len(str(valor)) > max_length:
                return str(valor)[:max_length]
            return valor
        
        # Obtener datos del negocio (los datos vienen directamente, no anidados)
        negocio_data = data
        
        # Buscar si ya existe un negocio con el mismo RTM y expediente
        rtm = negocio_data.get('rtm', '')
        expe = negocio_data.get('expe', '')
        
        if rtm and expe:
            negocio, created = Negocio.objects.get_or_create(
                empre=negocio_data.get('empre', '0301'),
                rtm=rtm,
                expe=expe,
                defaults={
                    'fecha_ini': negocio_data.get('fecha_ini') if negocio_data.get('fecha_ini') else None,
                    'fecha_can': negocio_data.get('fecha_can') if negocio_data.get('fecha_can') else None,
                    'identidad': truncar_campo(negocio_data.get('identidad', ''), 15),
                    'rtnpersonal': truncar_campo(negocio_data.get('rtnpersonal', ''), 14),
                    'comerciante': truncar_campo(negocio_data.get('comerciante', ''), 100),
                    'rtnnego': truncar_campo(negocio_data.get('rtnnego', ''), 14),
                    'nombrenego': truncar_campo(negocio_data.get('nombrenego', ''), 100),
                    'actividad': negocio_data.get('actividad', ''),
                    'identidadrep': truncar_campo(negocio_data.get('identidadrep', ''), 15),
                    'representante': truncar_campo(negocio_data.get('representante', ''), 100),
                    'estatus': negocio_data.get('estatus', 'A'),
                    'catastral': negocio_data.get('catastral', ''),
                    'cx': negocio_data.get('cx', '0.0000000'),
                    'cy': negocio_data.get('cy', '0.0000000'),
                    'direccion': truncar_campo(negocio_data.get('direccion', ''), 200),
                    'telefono': truncar_campo(negocio_data.get('telefono', ''), 9),
                    'celular': truncar_campo(negocio_data.get('celular', ''), 20),
                    'correo': truncar_campo(negocio_data.get('correo', ''), 100),
                    'pagweb': truncar_campo(negocio_data.get('pagweb', ''), 100),
                    'socios': truncar_campo(negocio_data.get('socios', ''), 200),
                    'comentario': truncar_campo(negocio_data.get('comentario', ''), 500)
                }
            )
            
            if not created:
                # Actualizar el negocio existente
                negocio.fecha_ini = negocio_data.get('fecha_ini') if negocio_data.get('fecha_ini') else None
                negocio.fecha_can = negocio_data.get('fecha_can') if negocio_data.get('fecha_can') else None
                negocio.identidad = truncar_campo(negocio_data.get('identidad', ''), 15)
                negocio.rtnpersonal = truncar_campo(negocio_data.get('rtnpersonal', ''), 14)
                negocio.comerciante = truncar_campo(negocio_data.get('comerciante', ''), 100)
                negocio.rtnnego = truncar_campo(negocio_data.get('rtnnego', ''), 14)
                negocio.nombrenego = truncar_campo(negocio_data.get('nombrenego', ''), 100)
                negocio.actividad = negocio_data.get('actividad', '')
                negocio.identidadrep = truncar_campo(negocio_data.get('identidadrep', ''), 15)
                negocio.representante = truncar_campo(negocio_data.get('representante', ''), 100)
                negocio.estatus = negocio_data.get('estatus', 'A')
                negocio.catastral = negocio_data.get('catastral', '')
                negocio.cx = negocio_data.get('cx', '0.0000000')
                negocio.cy = negocio_data.get('cy', '0.0000000')
                negocio.direccion = truncar_campo(negocio_data.get('direccion', ''), 200)
                negocio.telefono = truncar_campo(negocio_data.get('telefono', ''), 9)
                negocio.celular = truncar_campo(negocio_data.get('celular', ''), 20)
                negocio.correo = truncar_campo(negocio_data.get('correo', ''), 100)
                negocio.pagweb = truncar_campo(negocio_data.get('pagweb', ''), 100)
                negocio.socios = truncar_campo(negocio_data.get('socios', ''), 200)
                negocio.comentario = truncar_campo(negocio_data.get('comentario', ''), 500)
                negocio.save()
            
            return JsonResponse({
                'exito': True,
                'mensaje': 'Negocio guardado correctamente',
                'negocio_id': negocio.id
            })
        else:
            return JsonResponse({
                'exito': False,
                'mensaje': 'RTM y Expediente son obligatorios'
            })
            
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al guardar: {str(e)}'
        })

def handle_eliminar_negocio(request, data):
    """Maneja la eliminación de un negocio"""
    try:
        from tributario_app.models import Negocio
        
        # Obtener datos del negocio
        negocio_data = data.get('negocio', {})
        rtm = negocio_data.get('rtm', '')
        expe = negocio_data.get('expe', '')
        
        if rtm and expe:
            try:
                negocio = Negocio.objects.get(
                    empre=negocio_data.get('empre', '0301'),
                    rtm=rtm,
                    expe=expe
                )
                negocio.delete()
                return JsonResponse({
                    'exito': True,
                    'mensaje': 'Negocio eliminado correctamente'
                })
            except Negocio.DoesNotExist:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Negocio no encontrado'
                })
        else:
            return JsonResponse({
                'exito': False,
                'mensaje': 'RTM y Expediente son obligatorios'
            })
            
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al eliminar: {str(e)}'
        })

@csrf_exempt
def buscar_negocio_ajax(request):
    """Vista AJAX para buscar negocio por RTM y expediente"""
    try:
        # Obtener datos tanto de GET como de POST
        if request.method == 'GET':
            rtm = request.GET.get('rtm', '')
            expe = request.GET.get('expe', '')
            empresa = request.GET.get('empre', '0301')
        elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                rtm = data.get('rtm', '')
                expe = data.get('expe', '')
                empresa = data.get('empresa', '0301')
            except json.JSONDecodeError:
                # Si no es JSON, intentar con form data
                rtm = request.POST.get('rtm', '')
                expe = request.POST.get('expe', '')
                empresa = request.POST.get('empre', '0301')
        else:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Método no permitido'
            })
        
        print(f"[DEBUG] Buscando negocio: empre={empresa}, rtm={rtm}, expe={expe}")
        
        if rtm and expe:
            from tributario_app.models import Negocio
            try:
                negocio = Negocio.objects.get(
                    empre=empresa,
                    rtm=rtm,
                    expe=expe
                )
                
                print(f"[OK] Negocio encontrado: {negocio.nombrenego}")
                
                return JsonResponse({
                    'exito': True,
                    'negocio': {
                        'empre': negocio.empre,
                        'rtm': negocio.rtm,
                        'expe': negocio.expe,
                        'fecha_ini': negocio.fecha_ini.strftime('%Y-%m-%d') if negocio.fecha_ini else None,
                        'fecha_can': negocio.fecha_can.strftime('%Y-%m-%d') if negocio.fecha_can else None,
                        'identidad': negocio.identidad,
                        'rtnpersonal': negocio.rtnpersonal,
                        'comerciante': negocio.comerciante,
                        'rtnnego': negocio.rtnnego,
                        'nombrenego': negocio.nombrenego,
                        'actividad': negocio.actividad,
                        'identidadrep': negocio.identidadrep,
                        'representante': negocio.representante,
                        'estatus': negocio.estatus,
                        'catastral': negocio.catastral,
                        'cx': str(negocio.cx) if negocio.cx else '0.0000000',
                        'cy': str(negocio.cy) if negocio.cy else '',
                        'direccion': negocio.direccion,
                        'telefono': negocio.telefono,
                        'celular': negocio.celular,
                        'correo': negocio.correo,
                        'pagweb': negocio.pagweb,
                        'socios': negocio.socios,
                        'comentario': negocio.comentario
                    }
                })
            except Negocio.DoesNotExist:
                print(f"[ERROR] Negocio no encontrado: empre={empresa}, rtm={rtm}, expe={expe}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Negocio no encontrado'
                })
            except Exception as e:
                print(f"[ERROR] Error al buscar negocio: {e}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'Error al buscar negocio: {str(e)}'
                })
        else:
            return JsonResponse({
                'exito': False,
                'mensaje': 'RTM y Expediente son obligatorios'
            })
            
    except Exception as e:
        print(f"[ERROR] Error general en buscar_negocio_ajax: {e}")
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error en el servidor: {str(e)}'
        })

@csrf_exempt
def configurar_tasas_negocio(request):
    """Vista para configurar las tasas de un negocio específico"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
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
            from tributario_app.models import Negocio
            if negocio_id:
                negocio = Negocio.objects.get(id=negocio_id)
            else:
                negocio = Negocio.objects.get(
                    empre=empresa,
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
        return render(request, 'configurar_tasas_negocio.html', {
            'negocio': None,
            'tarifas_ics': [],
            'mensaje': mensaje or "Debe especificar un negocio válido",
            'exito': False,
            'empresa': empresa,
            'modulo': 'Tributario',
            'descripcion': 'Configurar Tasas del Negocio'
        })
    
    # Manejar solicitudes POST
    if request.method == 'POST':
        try:
            from tributario_app.forms import TarifasICSForm
            from tributario_app.models import TarifasICS, Rubro, Tarifas
            
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
                        from tributario_app.models import Tarifas
                        from datetime import datetime
                        ano_vigente = datetime.now().year
                        
                        tarifa = Tarifas.objects.get(
                            empresa=empresa,
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
                            rubro=rubro,
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
                if tarifa_id:
                    try:
                        tarifa_ics = TarifasICS.objects.get(id=tarifa_id, idneg=negocio.id)
                        tarifa_ics.delete()
                        mensaje = "Tarifa eliminada exitosamente"
                        exito = True
                    except TarifasICS.DoesNotExist:
                        mensaje = "Tarifa no encontrada"
                        exito = False
                else:
                    mensaje = "ID de tarifa requerido"
                    exito = False
                    
            elif accion == 'actualizar_valor':
                # Actualizar valor de tarifa ICS
                tarifa_id = request.POST.get('tarifa_id')
                nuevo_valor = request.POST.get('valor')
                if tarifa_id and nuevo_valor:
                    try:
                        tarifa_ics = TarifasICS.objects.get(id=tarifa_id, idneg=negocio.id)
                        tarifa_ics.valor = nuevo_valor
                        tarifa_ics.save()
                        mensaje = "Valor actualizado exitosamente"
                        exito = True
                    except TarifasICS.DoesNotExist:
                        mensaje = "Tarifa no encontrada"
                        exito = False
                else:
                    mensaje = "ID de tarifa y valor requeridos"
                    exito = False
                    
        except Exception as e:
            mensaje = f"Error en el servidor: {str(e)}"
            exito = False
    
    # Obtener tarifas ICS del negocio
    try:
        from tributario_app.models import TarifasICS
        tarifas_ics = TarifasICS.objects.filter(idneg=negocio.id).order_by('cod_tarifa')
    except Exception as e:
        tarifas_ics = []
        if not mensaje:
            mensaje = f"Error al cargar tarifas: {str(e)}"
            exito = False
    
    # Crear formulario inicial
    try:
        from tributario_app.forms import TarifasICSForm
        form = TarifasICSForm(initial={
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe
        })
    except Exception as e:
        form = None
        if not mensaje:
            mensaje = f"Error al crear formulario: {str(e)}"
            exito = False
    
    return render(request, 'configurar_tasas_negocio.html', {
        'negocio': negocio,
        'tarifas_ics': tarifas_ics,
        'form': form,
        'mensaje': mensaje,
        'exito': exito,
        'empresa': empresa,
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
        empresa = request.session.get('empresa', '0301')
        
        if not rubro_codigo:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Código de rubro requerido'
            })
        
        from tributario_app.models import Tarifas
        
        # Obtener año vigente (año actual)
        from datetime import datetime
        ano_vigente = datetime.now().year
        
        # Buscar tarifas del rubro con categoría 'C' del año vigente
        tarifas = Tarifas.objects.filter(
            empresa=empresa,
            rubro=rubro_codigo,
            categoria='C',
            ano=ano_vigente
        ).order_by('cod_tarifa')
        
        tarifas_list = [
            {
                'cod_tarifa': tarifa.cod_tarifa,
                'descripcion': tarifa.descripcion,
                'valor': str(tarifa.valor),
                'frecuencia': tarifa.frecuencia,
                'tipo': tarifa.tipo
            }
            for tarifa in tarifas
        ]
        
        return JsonResponse({
            'exito': True,
            'tarifas': tarifas_list
        })
        
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al obtener tarifas: {str(e)}'
        })

def cierre_anual(request):
    """Vista para cierre anual"""
    return render(request, 'cierre_anual.html', {
        'modulo': 'Tributario',
        'descripcion': 'Cierre Anual'
    })

def cargo_anual(request):
    """Vista para cargo anual"""
    return render(request, 'cargo_anual.html', {
        'modulo': 'Tributario',
        'descripcion': 'Cargo Anual'
    })

def recargos_moratorios(request):
    """Vista para recargos moratorios"""
    return render(request, 'recargos_moratorios.html', {
        'modulo': 'Tributario',
        'descripcion': 'Recargos Moratorios'
    })

def informes(request):
    """Vista para informes"""
    return render(request, 'informes.html', {
        'modulo': 'Tributario',
        'descripcion': 'Informes'
    })

def declaracion_volumen(request):
    """Vista para declaración de volumen de ventas"""
    empresa = request.session.get('empresa', '0301')
    declaraciones = []
    negocio = None
    mensaje = None
    exito = False
    rtm = request.GET.get('rtm', '')
    expe = request.GET.get('expe', '')

    if request.method == 'POST':
        try:
            from tributario_app.models import DeclaracionVolumen, Negocio
            from tributario_app.forms import DeclaracionVolumenForm
            accion = request.POST.get('accion')
            if accion == 'nuevo':
                mensaje = 'Formulario preparado para nueva declaración'
                exito = True
            elif accion == 'guardar':
                form = DeclaracionVolumenForm(request.POST)
                if form.is_valid():
                    declaracion = form.save(commit=False)
                    declaracion.usuario = request.session.get('usuario', 'SISTEMA')
                    declaracion_existente = DeclaracionVolumen.objects.filter(
                        rtm=declaracion.rtm, expe=declaracion.expe,
                        ano=declaracion.ano, mes=declaracion.mes
                    ).first()
                    if declaracion_existente:
                        declaracion_existente.tipo = declaracion.tipo
                        declaracion_existente.ventai = declaracion.ventai
                        declaracion_existente.ventac = declaracion.ventac
                        declaracion_existente.ventas = declaracion.ventas
                        declaracion_existente.valorexcento = declaracion.valorexcento
                        declaracion_existente.controlado = declaracion.controlado
                        declaracion_existente.unidad = declaracion.unidad
                        declaracion_existente.factor = declaracion.factor
                        declaracion_existente.save()
                        mensaje = f'Declaración {declaracion.ano}/{declaracion.mes:02d} actualizada correctamente'
                    else:
                        declaracion.save()
                        mensaje = f'Declaración {declaracion.ano}/{declaracion.mes:02d} creada correctamente'
                    exito = True
                else:
                    mensaje = 'Error en el formulario: ' + ', '.join([str(error) for error in form.errors.values()])
                    exito = False
            elif accion == 'eliminar':
                declaracion_id = request.POST.get('id')
                if declaracion_id:
                    try:
                        declaracion = DeclaracionVolumen.objects.get(id=declaracion_id)
                        declaracion.delete()
                        mensaje = f'Declaración eliminada correctamente'
                        exito = True
                    except DeclaracionVolumen.DoesNotExist:
                        mensaje = 'Declaración no encontrada'
                        exito = False
                else:
                    mensaje = 'ID de declaración es requerido para eliminar'
                    exito = False
            elif accion == 'actualizar_codigo_tarifa':
                tarifa_id = request.POST.get('tarifa_id')
                codigo_tarifa = request.POST.get('codigo_tarifa')
                if tarifa_id and codigo_tarifa:
                    try:
                        from tributario_app.models import TarifasICS
                        tarifa_ics = TarifasICS.objects.get(id=tarifa_id, idneg=negocio.id)
                        tarifa_ics.cod_tarifa = codigo_tarifa
                        tarifa_ics.save()
                        mensaje = f'Código de tarifa actualizado correctamente'
                        exito = True
                    except TarifasICS.DoesNotExist:
                        mensaje = 'Tarifa no encontrada'
                        exito = False
                else:
                    mensaje = 'ID de tarifa y código son requeridos'
                    exito = False
            elif accion == 'actualizar_tarifa_completa':
                tarifa_id = request.POST.get('tarifa_id')
                codigo_tarifa = request.POST.get('codigo_tarifa')
                valor = request.POST.get('valor')
                if tarifa_id and codigo_tarifa and valor:
                    try:
                        from tributario_app.models import TarifasICS
                        tarifa_ics = TarifasICS.objects.get(id=tarifa_id, idneg=negocio.id)
                        tarifa_ics.cod_tarifa = codigo_tarifa
                        tarifa_ics.valor = valor
                        tarifa_ics.save()
                        mensaje = f'Tarifa actualizada correctamente'
                        exito = True
                    except TarifasICS.DoesNotExist:
                        mensaje = 'Tarifa no encontrada'
                        exito = False
                else:
                    mensaje = 'ID de tarifa, código y valor son requeridos'
                    exito = False
        except Exception as e:
            mensaje = f'Error: {str(e)}'
            exito = False

    if rtm and expe:
        try:
            from tributario_app.models import Negocio
            negocio = Negocio.objects.get(empre=empresa, rtm=rtm, expe=expe)
        except Negocio.DoesNotExist:
            mensaje = 'Negocio no encontrado'
            exito = False

        if negocio:
            try:
                from tributario_app.models import DeclaracionVolumen, TarifasICS, Rubro
                declaraciones = DeclaracionVolumen.objects.filter(
                    rtm=negocio.rtm, expe=negocio.expe
                ).order_by('-ano', '-mes')
                
                # Obtener tarifas ICS vinculadas al negocio con información del rubro
                tarifas_ics_raw = TarifasICS.obtener_tarifas_por_negocio(negocio.id)
                tarifas_ics = []
                
                for tarifa_ics in tarifas_ics_raw:
                    # Buscar información del rubro
                    try:
                        rubro_info = Rubro.objects.get(
                            empresa=empresa,
                            codigo=tarifa_ics.rubro
                        )
                        rubro_nombre = rubro_info.descripcion
                    except Rubro.DoesNotExist:
                        rubro_nombre = "Rubro no encontrado"
                    
                    # Buscar tarifas disponibles en tarifasics para este negocio y rubro específico
                    try:
                        tarifas_disponibles = TarifasICS.objects.filter(
                            idneg=negocio.id,
                            rubro=tarifa_ics.rubro
                        ).exclude(id=tarifa_ics.id).order_by('cod_tarifa')
                        
                        # Crear lista de opciones para el combobox
                        opciones_tarifas = []
                        for tarifa in tarifas_disponibles:
                            opciones_tarifas.append({
                                'codigo': tarifa.cod_tarifa,
                                'descripcion': f"Tarifa {tarifa.cod_tarifa}",
                                'valor': str(tarifa.valor)
                            })
                        tarifa_ics.tarifas_disponibles = opciones_tarifas
                    except Exception as e:
                        tarifa_ics.tarifas_disponibles = []
                    
                    # Agregar información del rubro al objeto tarifa_ics
                    tarifa_ics.rubro_nombre = rubro_nombre
                    tarifas_ics.append(tarifa_ics)
                    
            except Exception as e:
                print(f"Error al cargar declaraciones: {e}")
                declaraciones = []
                tarifas_ics = []

    from tributario_app.forms import DeclaracionVolumenForm
    initial_data = {}
    if negocio:
        initial_data = {'idneg': negocio.id, 'rtm': negocio.rtm, 'expe': negocio.expe}
    form = DeclaracionVolumenForm(initial=initial_data)

    return render(request, 'declaracion_volumen.html', {
        'form': form, 'negocio': negocio, 'declaraciones': declaraciones,
        'tarifas_ics': tarifas_ics, 'mensaje': mensaje, 'exito': exito, 
        'empresa': empresa,
        'modulo': 'Tributario', 'descripcion': 'Declaración de Volumen de Ventas'
    })

def miscelaneos(request):
    """Vista para misceláneos"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Cargar oficinas disponibles
    oficinas = []
    try:
        from tributario_app.models import Oficina
        oficinas = Oficina.objects.filter(empresa=empresa).order_by('codigo')
    except Exception as e:
        print(f"Error al cargar oficinas: {e}")
        oficinas = []
    
    return render(request, 'miscelaneos.html', {
        'modulo': 'Tributario',
        'descripcion': 'Misceláneos',
        'empresa': empresa,
        'oficinas': oficinas
    })

def convenios_pagos(request):
    """Vista para convenios de pagos"""
    return render(request, 'convenios_pagos.html', {
        'modulo': 'Tributario',
        'descripcion': 'Convenios de Pagos'
    })

def actividad_crud(request):
    """Vista para CRUD de actividades"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Variables para el contexto
    actividades = []
    empresa_filtro = None
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        try:
            from tributario_app.models import Actividad
            
            accion = request.POST.get('accion')
            empresa = request.POST.get('empresa', '')
            codigo = request.POST.get('codigo', '')
            descripcion = request.POST.get('descripcion', '')
            
            if accion == 'nuevo':
                # Limpiar campos para nuevo registro
                mensaje = 'Formulario preparado para nueva actividad'
                exito = True
                
            elif accion == 'guardar':
                if not empresa or not codigo or not descripcion:
                    mensaje = 'Todos los campos son obligatorios'
                    exito = False
                else:
                    # Verificar si ya existe la actividad
                    if Actividad.objects.filter(empresa=empresa, codigo=codigo).exists():
                        # Actualizar actividad existente
                        actividad = Actividad.objects.get(empresa=empresa, codigo=codigo)
                        actividad.descripcion = descripcion
                        actividad.save()
                        mensaje = f'Actividad {codigo} actualizada correctamente'
                        exito = True
                    else:
                        # Crear nueva actividad
                        Actividad.objects.create(
                            empresa=empresa,
                            codigo=codigo,
                            descripcion=descripcion
                        )
                        mensaje = f'Actividad {codigo} creada correctamente'
                        exito = True
                        
            elif accion == 'eliminar':
                codigo_eliminar = request.POST.get('codigo')
                empresa_eliminar = request.POST.get('empresa')
                
                if codigo_eliminar and empresa_eliminar:
                    try:
                        actividad = Actividad.objects.get(empresa=empresa_eliminar, codigo=codigo_eliminar)
                        actividad.delete()
                        mensaje = f'Actividad {codigo_eliminar} eliminada correctamente'
                        exito = True
                    except Actividad.DoesNotExist:
                        mensaje = 'Actividad no encontrada'
                        exito = False
                else:
                    mensaje = 'Código y empresa son obligatorios para eliminar'
                    exito = False
                    
        except Exception as e:
            mensaje = f'Error: {str(e)}'
            exito = False
    
    # Cargar actividades si hay un municipio seleccionado
    if empresa:
        try:
            from tributario_app.models import Actividad
            actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
            empresa_filtro = empresa
        except Exception as e:
            print(f"Error al cargar actividades: {e}")
            actividades = []
    
    return render(request, 'actividad.html', {
        'empresa': empresa,
        'actividades': actividades,
        'empresa_filtro': empresa_filtro,
        'mensaje': mensaje,
        'exito': exito,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Actividades'
    })

def oficina_crud(request):
    """Vista para CRUD de oficinas"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Variables para el contexto
    oficinas = []
    empresa_filtro = None
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        try:
            from tributario_app.models import Oficina
            
            accion = request.POST.get('accion')
            empresa = request.POST.get('empresa', '')
            codigo = request.POST.get('codigo', '')
            descripcion = request.POST.get('descripcion', '')
            
            if accion == 'nuevo':
                # Limpiar campos para nuevo registro
                mensaje = 'Formulario preparado para nueva oficina'
                exito = True
                
            elif accion == 'guardar':
                if not empresa or not codigo or not descripcion:
                    mensaje = 'Todos los campos son obligatorios'
                    exito = False
                else:
                    # Verificar si ya existe la oficina
                    if Oficina.objects.filter(empresa=empresa, codigo=codigo).exists():
                        # Actualizar oficina existente
                        oficina = Oficina.objects.get(empresa=empresa, codigo=codigo)
                        oficina.descripcion = descripcion
                        oficina.save()
                        mensaje = f'Oficina {codigo} actualizada correctamente'
                        exito = True
                    else:
                        # Crear nueva oficina
                        Oficina.objects.create(
                            empresa=empresa,
                            codigo=codigo,
                            descripcion=descripcion
                        )
                        mensaje = f'Oficina {codigo} creada correctamente'
                        exito = True
                        
            elif accion == 'eliminar':
                codigo_eliminar = request.POST.get('codigo')
                empresa_eliminar = request.POST.get('empresa')
                
                if codigo_eliminar and empresa_eliminar:
                    try:
                        oficina = Oficina.objects.get(empresa=empresa_eliminar, codigo=codigo_eliminar)
                        oficina.delete()
                        mensaje = f'Oficina {codigo_eliminar} eliminada correctamente'
                        exito = True
                    except Oficina.DoesNotExist:
                        mensaje = 'Oficina no encontrada'
                        exito = False
                else:
                    mensaje = 'Código y empresa son obligatorios para eliminar'
                    exito = False
                    
        except Exception as e:
            mensaje = f'Error: {str(e)}'
            exito = False
    
    # Cargar oficinas si hay un municipio seleccionado
    if empresa:
        try:
            from tributario_app.models import Oficina
            oficinas = Oficina.objects.filter(empresa=empresa).order_by('codigo')
            empresa_filtro = empresa
        except Exception as e:
            print(f"Error al cargar oficinas: {e}")
            oficinas = []
    
    return render(request, 'oficina.html', {
        'empresa': empresa,
        'oficinas': oficinas,
        'empresa_filtro': empresa_filtro,
        'mensaje': mensaje,
        'exito': exito,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Oficinas'
    })

def rubros_crud(request):
    """Vista para CRUD de rubros"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Variables para el contexto
    rubros = []
    actividades = []
    empresa_filtro = None
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        try:
            from tributario_app.models import Rubro, Actividad
            
            action = request.POST.get('action')
            empresa = request.POST.get('empresa', '')
            codigo = request.POST.get('codigo', '')
            descripcion = request.POST.get('descripcion', '')
            tipo = request.POST.get('tipo', '')
            cuenta = request.POST.get('cuenta', '')
            cuentarez = request.POST.get('cuentarez', '')
            
            if action == 'nuevo':
                # Limpiar campos para nuevo registro
                mensaje = 'Formulario preparado para nuevo rubro'
                exito = True
                
            elif action == 'guardar':
                # Validación mejorada - solo campos realmente obligatorios según el modelo
                if not empresa or not codigo:
                    mensaje = 'Empresa y código son obligatorios'
                    exito = False
                elif not descripcion or not descripcion.strip():
                    mensaje = 'La descripción es obligatoria'
                    exito = False
                else:
                    # Verificar si ya existe el rubro
                    if Rubro.objects.filter(empresa=empresa, codigo=codigo).exists():
                        # Actualizar rubro existente
                        rubro = Rubro.objects.get(empresa=empresa, codigo=codigo)
                        rubro.descripcion = descripcion.strip() if descripcion else ''
                        rubro.tipo = tipo.strip() if tipo else ''
                        rubro.cuenta = cuenta.strip() if cuenta else ''
                        rubro.cuentarez = cuentarez.strip() if cuentarez else ''
                        rubro.save()
                        mensaje = f'Rubro {codigo} actualizado correctamente'
                        exito = True
                        # Limpiar formulario después de actualizar
                        form_context = {
                            'empresa': empresa,
                            'codigo': '',
                            'descripcion': '',
                            'tipo': '',
                            'cuenta': '',
                            'cuentarez': ''
                        }
                    else:
                        try:
                            # Crear nuevo rubro
                            rubro = Rubro.objects.create(
                                empresa=empresa,
                                codigo=codigo,
                                descripcion=descripcion.strip() if descripcion else '',
                                tipo=tipo.strip() if tipo else '',
                                cuenta=cuenta.strip() if cuenta else '',
                                cuentarez=cuentarez.strip() if cuentarez else ''
                            )
                            mensaje = f'Rubro {codigo} creado correctamente'
                            exito = True
                            # Limpiar formulario después de crear
                            form_context = {
                                'empresa': empresa,
                                'codigo': '',
                                'descripcion': '',
                                'tipo': '',
                                'cuenta': '',
                                'cuentarez': ''
                            }
                        except Exception as e:
                            mensaje = f'Error al crear rubro: {str(e)}'
                            exito = False
                        
            elif action == 'eliminar':
                codigo_eliminar = request.POST.get('codigo_eliminar')
                empresa_eliminar = request.POST.get('empresa_eliminar')
                
                print(f"Debug eliminación - Código: {codigo_eliminar}, Empresa: {empresa_eliminar}")
                
                if codigo_eliminar and empresa_eliminar:
                    try:
                        rubro = Rubro.objects.get(empresa=empresa_eliminar, codigo=codigo_eliminar)
                        rubro.delete()
                        mensaje = f'Rubro {codigo_eliminar} eliminado correctamente'
                        exito = True
                    except Rubro.DoesNotExist:
                        mensaje = 'Rubro no encontrado'
                        exito = False
                else:
                    mensaje = f'Empresa no encontrada para eliminar el rubro. Código: {codigo_eliminar}, Empresa: {empresa_eliminar}'
                    exito = False
                    
        except Exception as e:
            mensaje = f'Error: {str(e)}'
            exito = False
    
    # Cargar rubros y actividades si hay un municipio seleccionado
    if empresa:
        try:
            from tributario_app.models import Rubro, Actividad
            rubros = Rubro.objects.filter(empresa=empresa).order_by('codigo')
            actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
            empresa_filtro = empresa
        except Exception as e:
            print(f"Error al cargar rubros/actividades: {e}")
            rubros = []
            actividades = []
    
    # Crear un contexto básico para el formulario
    form_context = {
        'empresa': empresa,
        'codigo': '',
        'descripcion': '',
        'tipo': '',
        'cuenta': '',
        'cuentarez': ''
    }
    
    return render(request, 'formulario_rubros.html', {
        'empresa': empresa,
        'empresa': empresa,  # Agregar variable empresa para el template
        'rubros': rubros,
        'actividades': actividades,
        'empresa_filtro': empresa_filtro,
        'mensaje': mensaje,
        'exito': exito,
        'form': form_context,  # Agregar contexto del formulario
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Rubros'
    })

def tarifas_crud(request):
    """Vista para CRUD de tarifas"""
    empresa = request.session.get('empresa', '0301')
    codigo_rubro = request.GET.get('codigo_rubro', '')
    ano_filtro = request.GET.get('ano', '')  # Obtener año del filtro
    
    # Imports necesarios al inicio
    from tributario_app.models import Tarifas
    from tributario_app.forms import TarifasForm
    
    # Variables para el contexto
    tarifas = []
    empresa_filtro = None
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        try:
            accion = request.POST.get('accion')
            
            if accion == 'eliminar':
                # Manejar eliminación de tarifa
                empresa_eliminar = request.POST.get('empresa')
                cod_tarifa_eliminar = request.POST.get('cod_tarifa')
                rubro_eliminar = request.POST.get('rubro')
                ano_eliminar = request.POST.get('ano')
                
                if empresa_eliminar and cod_tarifa_eliminar and rubro_eliminar and ano_eliminar:
                    try:
                        tarifa = Tarifas.objects.get(
                            empresa=empresa_eliminar,
                            cod_tarifa=cod_tarifa_eliminar,
                            rubro=rubro_eliminar,
                            ano=ano_eliminar
                        )
                        descripcion_eliminada = tarifa.descripcion
                        tarifa.delete()
                        mensaje = f'Tarifa {cod_tarifa_eliminar} ({descripcion_eliminada}) eliminada correctamente'
                        exito = True
                    except Tarifas.DoesNotExist:
                        mensaje = 'Tarifa no encontrada'
                        exito = False
                else:
                    mensaje = 'Empresa, código de tarifa, rubro y año son obligatorios para eliminar'
                    exito = False
                
                # Preparar formulario después de la eliminación
                # Mantener el rubro de la tarifa eliminada
                initial_data = {'empresa': empresa}
                if rubro_eliminar:
                    initial_data['rubro'] = rubro_eliminar
                elif codigo_rubro:
                    initial_data['rubro'] = codigo_rubro
                form = TarifasForm(initial=initial_data)
                
                # Actualizar los filtros para mantener la consulta filtrada
                if rubro_eliminar:
                    codigo_rubro = rubro_eliminar
                if ano_eliminar:
                    ano_filtro = ano_eliminar
            else:
                # Manejar guardado/actualización de tarifa
                form = TarifasForm(request.POST)
                if form.is_valid():
                    try:
                        # El modelo se encarga de la lógica de actualización vs creación
                        tarifa = form.save(commit=False)
                        tarifa.empresa = empresa
                        tarifa.rubro = request.POST.get('rubro', '').strip() or codigo_rubro
                        tarifa.save()
                        
                        # Determinar si fue creación o actualización
                        if tarifa.pk:
                            mensaje = f"Tarifa {tarifa.cod_tarifa} (Año {tarifa.ano}) procesada exitosamente."
                            exito = True
                        else:
                            mensaje = f"Error al procesar la tarifa."
                            exito = False
                        
                        # Limpiar formulario después de cualquier operación
                        initial_data = {'empresa': empresa}
                        if codigo_rubro:
                            initial_data['rubro'] = codigo_rubro
                        form = TarifasForm(initial=initial_data)
                    except Exception as e:
                        mensaje = f"Error al procesar la tarifa: {str(e)}"
                        exito = False
                else:
                    mensaje = f"Error en el formulario: {form.errors}"
                    exito = False
        except Exception as e:
            mensaje = f"Error al procesar la tarifa: {str(e)}"
            exito = False
    else:
        # Preparar formulario inicial
        initial_data = {'empresa': empresa}
        if codigo_rubro:
            initial_data['rubro'] = codigo_rubro
        form = TarifasForm(initial=initial_data)
    
    # Obtener tarifas del municipio, filtrando por rubro y año si se especifica
    if empresa:
        try:
            tarifas_query = Tarifas.objects.filter(empresa=empresa)
            if codigo_rubro:
                tarifas_query = tarifas_query.filter(rubro=codigo_rubro)
            if ano_filtro:
                tarifas_query = tarifas_query.filter(ano=ano_filtro)
            tarifas = tarifas_query.order_by('rubro', 'ano', 'cod_tarifa')
            empresa_filtro = empresa
        except Exception as e:
            print(f"Error al cargar tarifas: {e}")
            tarifas = []
    
    return render(request, 'formulario_tarifas.html', {
        'form': form,
        'tarifas': tarifas,
        'empresa_filtro': empresa_filtro,
        'ano_filtro': ano_filtro,
        'mensaje': mensaje,
        'exito': exito,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Tarifas'
    })

def plan_arbitrio_crud(request):
    """Vista para CRUD de plan de arbitrios con herencia de parámetros y filtrado del grid"""
    from tributario_app.models import PlanArbitrio, Rubro, Tarifas
    from tributario_app.forms import PlanArbitrioForm
    
    # Obtener parámetros de herencia desde la URL
    # Priorizar el parámetro GET sobre la sesión cuando esté presente
    empresa = request.GET.get('empresa', '') or request.session.get('municipio_id', '')
    
    # Debug: Mostrar valores antes del procesamiento
    print(f"[DEBUG] DEBUG - Valores antes del procesamiento:")
    print(f"   Session municipio_id: '{request.session.get('municipio_id', '')}'")
    print(f"   GET empresa: '{request.GET.get('empresa', '')}'")
    print(f"   Municipio código inicial: '{empresa}'")
    print(f"   Prioridad: GET empresa sobre Session municipio_id")
    
    # Limpiar y formatear el código de municipio
    if empresa:
        empresa = str(empresa).strip()  # Eliminar espacios
        print(f"   Municipio después de strip: '{empresa}'")
        # Solo aplicar zfill si no tiene 4 dígitos ya
        if len(empresa) < 4:
            empresa = empresa.zfill(4)
            print(f"   Municipio después de zfill: '{empresa}'")
        else:
            print(f"   Municipio sin zfill (ya tiene 4 dígitos): '{empresa}'")
    
    rubro_codigo = request.GET.get('rubro', '')
    ano_heredado = request.GET.get('ano', '')
    cod_tarifa_heredado = request.GET.get('cod_tarifa', '')
    
    mensaje = ''
    exito = False
    
    print(f"[DEBUG] Plan de Arbitrio - Parámetros heredados:")
    print(f"   Municipio (raw): {request.session.get('municipio_id', '')} o {request.GET.get('empresa', '')}")
    print(f"   Municipio (formateado): {empresa}")
    print(f"   Rubro: {rubro_codigo}")
    print(f"   Año: {ano_heredado}")
    print(f"   Código Tarifa: {cod_tarifa_heredado}")
    print(f"   URL completa: {request.get_full_path()}")
    print(f"   Método: {request.method}")
    
    # Obtener descripción del rubro si viene heredado
    descripcion_rubro = ''
    if rubro_codigo and empresa:
        try:
            rubro_obj = Rubro.objects.get(empresa=empresa, codigo=rubro_codigo)
            descripcion_rubro = rubro_obj.descripcion
            print(f"[OK] Rubro encontrado: {descripcion_rubro}")
        except Rubro.DoesNotExist:
            print(f"[ERROR] Rubro {rubro_codigo} no encontrado en municipio {empresa}")
    
    # Datos iniciales para el formulario con parámetros heredados
    initial_data = {
        'empresa': empresa,
        'rubro': rubro_codigo,
        'cod_tarifa': cod_tarifa_heredado,
        'ano': ano_heredado if ano_heredado else '',
    }
    
    if request.method == 'POST':
        accion = request.POST.get('action', 'guardar')
        print(f"[DEBUG] Acción solicitada: {accion}")
        
        if accion == 'guardar':
            print(f"🔍 Creando formulario con datos POST...")
            form = PlanArbitrioForm(request.POST, initial=initial_data)
            print(f"🔍 Formulario creado. Datos del formulario: {form.data}")
            print(f"🔍 Formulario bound: {form.is_bound}")
            print(f"🔍 Formulario válido: {form.is_valid()}")
            if not form.is_valid():
                print(f"❌ Errores en formulario: {form.errors}")
                print(f"🔍 Datos del POST recibidos: {dict(request.POST)}")
                print(f"🔍 Datos del formulario: {form.data}")
                print(f"🔍 Campos del formulario: {list(form.fields.keys())}")
                for field_name, field_errors in form.errors.items():
                    print(f"❌ Error en campo '{field_name}': {field_errors}")
                print(f"🔍 Formulario válido: {form.is_valid()}")
                print(f"🔍 Formulario bound: {form.is_bound}")
            if form.is_valid():
                try:
                    # Verificar si ya existe un plan con los mismos parámetros únicos
                    empresa = form.cleaned_data['empresa']
                    rubro = form.cleaned_data['rubro']
                    cod_tarifa = form.cleaned_data['cod_tarifa']
                    ano = form.cleaned_data['ano']
                    codigo = form.cleaned_data['codigo']
                    
                    plan_existente = None
                    try:
                        plan_existente = PlanArbitrio.objects.get(
                            empresa=empresa,
                            rubro=rubro,
                            cod_tarifa=cod_tarifa,
                            ano=ano,
                            codigo=codigo
                        )
                        # Si existe, actualizar usando update() para evitar validación de unique_together
                        print(f"[DEBUG] ✅ REGISTRO EXISTENTE ENCONTRADO: ID={plan_existente.id}")
                        print(f"[DEBUG] 🔄 ACTUALIZANDO REGISTRO EXISTENTE")
                        
                        # Obtener los nuevos valores del formulario
                        nueva_descripcion = form.cleaned_data.get('descripcion', '')
                        nuevo_minimo = form.cleaned_data.get('minimo', 0.00)
                        nuevo_maximo = form.cleaned_data.get('maximo', 0.00)
                        
                        # Calcular el valor automáticamente
                        if nuevo_minimo is not None and nuevo_maximo is not None:
                            nuevo_valor = (nuevo_minimo + nuevo_maximo) / 2
                        elif nuevo_minimo is not None:
                            nuevo_valor = nuevo_minimo
                        elif nuevo_maximo is not None:
                            nuevo_valor = nuevo_maximo
                        else:
                            nuevo_valor = 0.00
                        
                        # Usar update() para evitar la validación de unique_together
                        rows_updated = PlanArbitrio.objects.filter(
                            empresa=empresa,
                            rubro=rubro,
                            cod_tarifa=cod_tarifa,
                            ano=ano,
                            codigo=codigo
                        ).update(
                            descripcion=nueva_descripcion,
                            minimo=nuevo_minimo,
                            maximo=nuevo_maximo,
                            valor=nuevo_valor
                        )
                        
                        if rows_updated > 0:
                            mensaje = f"✅ Plan de arbitrio {codigo} actualizado exitosamente."
                            exito = True
                            print(f"[OK] Plan de arbitrio actualizado: {codigo}")
                        else:
                            mensaje = f"❌ Error: No se pudo actualizar el plan de arbitrio {codigo}."
                            exito = False
                            print(f"[ERROR] No se pudo actualizar: {codigo}")
                            
                    except PlanArbitrio.DoesNotExist:
                        # Si no existe, crear nuevo
                        print(f"[DEBUG] ❌ REGISTRO NO EXISTE")
                        print(f"[DEBUG] 🆕 CREANDO NUEVO REGISTRO")
                        
                        plan_nuevo = form.save()
                        mensaje = f"✅ Plan de arbitrio {plan_nuevo.codigo} creado exitosamente."
                        exito = True
                        print(f"[OK] Plan de arbitrio creado: {plan_nuevo.codigo}")
                        
                except Exception as e:
                    mensaje = f"Error al procesar el plan de arbitrio: {str(e)}"
                    exito = False
                    print(f"[ERROR] Error: {e}")
            else:
                mensaje = "Error en el formulario. Verifique los datos ingresados."
                exito = False
                print(f"[ERROR] Errores en formulario: {form.errors}")
                print(f"🔍 Datos del POST recibidos: {dict(request.POST)}")
                print(f"🔍 Datos del formulario: {form.data}")
                print(f"🔍 Campos del formulario: {list(form.fields.keys())}")
                for field_name, field_errors in form.errors.items():
                    print(f"❌ Error en campo '{field_name}': {field_errors}")
                print(f"🔍 Formulario válido: {form.is_valid()}")
                print(f"🔍 Formulario bound: {form.is_bound}")
        
        elif accion == 'eliminar':
            # Usar los parámetros correctos que envía el JavaScript
            empresa = request.POST.get('empresa_eliminar', '').strip()
            rubro = request.POST.get('rubro_eliminar', '').strip()
            cod_tarifa = request.POST.get('cod_tarifa_eliminar', '').strip()
            ano = request.POST.get('ano_eliminar', '').strip()
            codigo = request.POST.get('codigo_eliminar', '').strip()
            
            print(f"[DEBUG] 🔴 ELIMINANDO PLAN:")
            print(f"  - empresa: '{empresa}'")
            print(f"  - rubro: '{rubro}'")
            print(f"  - cod_tarifa: '{cod_tarifa}'")
            print(f"  - ano: '{ano}'")
            print(f"  - codigo: '{codigo}'")
            
            if empresa and rubro and cod_tarifa and ano and codigo:
                try:
                    # Convertir ano a entero si es necesario
                    ano_int = int(ano) if ano else None
                    print(f"[DEBUG] Buscando plan con año: {ano_int}")
                    
                    plan = PlanArbitrio.objects.get(
                        empresa=empresa,
                        rubro=rubro,
                        cod_tarifa=cod_tarifa,
                        ano=ano_int,
                        codigo=codigo
                    )
                    print(f"[DEBUG] ✅ Plan encontrado: ID={plan.id}")
                    
                    descripcion_eliminada = plan.descripcion
                    plan.delete()
                    mensaje = f'✅ Plan de arbitrio {codigo} ({descripcion_eliminada}) eliminado correctamente'
                    exito = True
                    print(f"[OK] Plan eliminado: {codigo}")
                except PlanArbitrio.DoesNotExist:
                    mensaje = f'❌ Plan de arbitrio {codigo} no encontrado'
                    exito = False
                    print(f"[ERROR] Plan no encontrado: {codigo}")
                except Exception as e:
                    mensaje = f'❌ Error al eliminar el plan: {str(e)}'
                    exito = False
                    print(f"[ERROR] Error al eliminar: {e}")
            else:
                mensaje = '❌ Datos insuficientes para eliminar el plan de arbitrio'
                exito = False
                print(f"[ERROR] Datos insuficientes para eliminar")
        
        elif accion == 'editar':
            # Manejar edición de plan - cargar datos existentes
            empresa_editar = request.POST.get('empresa_editar', '').strip()
            rubro_editar = request.POST.get('rubro_editar', '').strip()
            cod_tarifa_editar = request.POST.get('cod_tarifa_editar', '').strip()
            ano_editar = request.POST.get('ano_editar', '').strip()
            codigo_editar = request.POST.get('codigo_editar', '').strip()
            
            print(f"[DEBUG] 🔵 EDITANDO PLAN:")
            print(f"  - empresa: '{empresa_editar}'")
            print(f"  - rubro: '{rubro_editar}'")
            print(f"  - cod_tarifa: '{cod_tarifa_editar}'")
            print(f"  - ano: '{ano_editar}'")
            print(f"  - codigo: '{codigo_editar}'")
            
            if empresa_editar and rubro_editar and cod_tarifa_editar and ano_editar and codigo_editar:
                try:
                    ano_int = int(ano_editar) if ano_editar else None
                    print(f"[DEBUG] Buscando plan con año: {ano_int}")
                    
                    plan_a_editar = PlanArbitrio.objects.get(
                        empresa=empresa_editar,
                        rubro=rubro_editar,
                        cod_tarifa=cod_tarifa_editar,
                        ano=ano_int,
                        codigo=codigo_editar
                    )
                    print(f"[DEBUG] ✅ Plan encontrado: ID={plan_a_editar.id}")
                    
                    # Cargar los datos del plan en el formulario
                    form = PlanArbitrioForm(initial={
                        'empresa': plan_a_editar.empresa,
                        'rubro': plan_a_editar.rubro,
                        'cod_tarifa': plan_a_editar.cod_tarifa,
                        'ano': plan_a_editar.ano,
                        'codigo': plan_a_editar.codigo,
                        'descripcion': plan_a_editar.descripcion,
                        'minimo': plan_a_editar.minimo,
                        'maximo': plan_a_editar.maximo,
                        'valor': plan_a_editar.valor
                    })
                    mensaje = f"✅ Plan de arbitrio {codigo_editar} cargado para edición."
                    exito = True
                    print(f"[OK] Plan cargado para edición: {codigo_editar}")
                except PlanArbitrio.DoesNotExist:
                    mensaje = f"❌ No se encontró el plan con los criterios especificados."
                    exito = False
                    form = PlanArbitrioForm(initial=initial_data)
                    print(f"[ERROR] Plan no encontrado para editar: {codigo_editar}")
                except Exception as e:
                    mensaje = f"❌ Error al cargar el plan para edición: {str(e)}"
                    exito = False
                    form = PlanArbitrioForm(initial=initial_data)
                    print(f"[ERROR] Error al cargar para editar: {e}")
            else:
                mensaje = "❌ Datos insuficientes para editar el plan."
                exito = False
                form = PlanArbitrioForm(initial=initial_data)
                print(f"[ERROR] Datos insuficientes para editar")
        
        elif accion == 'nuevo':
            # Limpiar formulario pero mantener parámetros heredados
            initial_data = {
                'empresa': empresa,
                'rubro': rubro_codigo,
                'cod_tarifa': cod_tarifa_heredado,
                'ano': ano_heredado if ano_heredado else '',
            }
            mensaje = 'Formulario preparado para nuevo plan de arbitrio'
            exito = True
    
    # Crear formulario con datos iniciales
    form = PlanArbitrioForm(initial=initial_data)
    
    # Filtrar grid de planes de arbitrio según parámetros heredados
    planes_query = PlanArbitrio.objects.filter(empresa=empresa)
    
    # Aplicar filtros adicionales si están presentes
    if rubro_codigo:
        planes_query = planes_query.filter(rubro=rubro_codigo)
        print(f"[DEBUG] Filtrando por rubro: {rubro_codigo}")
    
    if ano_heredado:
        planes_query = planes_query.filter(ano=ano_heredado)
        print(f"[DEBUG] Filtrando por año: {ano_heredado}")
    
    if cod_tarifa_heredado:
        planes_query = planes_query.filter(cod_tarifa=cod_tarifa_heredado)
        print(f"[DEBUG] Filtrando por código de tarifa: {cod_tarifa_heredado}")
    
    # Ordenar planes
    planes_arbitrio = planes_query.order_by('-ano', 'codigo')
    
    print(f"📊 Planes encontrados: {planes_arbitrio.count()}")
    
    context = {
        'form': form,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Plan de Arbitrios',
        'empresa_filtro': empresa,
        'rubro_filtro': rubro_codigo,
        'ano_filtro': ano_heredado,
        'cod_tarifa_filtro': cod_tarifa_heredado,
        'planes_arbitrio': planes_arbitrio,
        'mensaje': mensaje,
        'exito': exito,
    }
    
    return render(request, 'formulario_plan_arbitrio.html', context)

@csrf_exempt
def buscar_rubro_plan_arbitrio(request):
    """Vista AJAX para buscar rubro en plan de arbitrio"""
    if request.method == 'POST':
        try:
            from tributario_app.models import Rubro
            
            # Obtener datos del request (FormData)
            codigo_rubro = request.POST.get('codigo_rubro', '').strip()
            empresa = request.POST.get('empresa', '').strip()
            
            print(f"[DEBUG] Buscando rubro: empresa={empresa}, codigo={codigo_rubro}")
            
            if not codigo_rubro or not empresa:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Código de rubro y empresa son obligatorios'
                })
            
            try:
                # Buscar rubro en la base de datos
                rubro = Rubro.objects.get(empresa=empresa, codigo=codigo_rubro)
                
                print(f"[OK] Rubro encontrado: {rubro.descripcion}")
                return JsonResponse({
                    'exito': True,
                    'rubro': {
                        'codigo': rubro.codigo,
                        'descripcion': rubro.descripcion,
                        'empresa': rubro.empresa
                    },
                    'mensaje': f'Rubro encontrado: {rubro.descripcion}'
                })
            except Rubro.DoesNotExist:
                print(f"[ERROR] Rubro no encontrado: {codigo_rubro}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'No se encontró el rubro {codigo_rubro} en el municipio {empresa}'
                })
        except Exception as e:
            print(f"[ERROR] Error en búsqueda de rubro: {e}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error en la búsqueda: {str(e)}'
            })
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'})

@csrf_exempt
def buscar_tarifa_plan_arbitrio(request):
    """Vista AJAX para buscar tarifa en plan de arbitrio"""
    if request.method == 'POST':
        try:
            from tributario_app.models import Tarifas, Rubro
            
            # Obtener datos del request (FormData)
            codigo_tarifa = request.POST.get('codigo_tarifa', '').strip()
            empresa = request.POST.get('empresa', '').strip()
            
            print(f"[DEBUG] Buscando tarifa: empresa={empresa}, codigo={codigo_tarifa}")
            
            if not codigo_tarifa or not empresa:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Código de tarifa y empresa son obligatorios'
                })
            
            try:
                # Buscar tarifa en la base de datos
                tarifa = Tarifas.objects.filter(
                    empresa=empresa,
                    cod_tarifa=codigo_tarifa
                ).order_by('-ano').first()  # Obtener la más reciente
                
                if tarifa:
                    # Obtener descripción del rubro si existe
                    descripcion_rubro = ''
                    if tarifa.rubro:
                        try:
                            rubro = Rubro.objects.get(empresa=empresa, codigo=tarifa.rubro)
                            descripcion_rubro = rubro.descripcion
                        except Rubro.DoesNotExist:
                            pass
                    
                    print(f"[OK] Tarifa encontrada: {tarifa.descripcion}")
                    return JsonResponse({
                        'exito': True,
                        'tarifa': {
                            'codigo': tarifa.cod_tarifa,
                            'descripcion': tarifa.descripcion,
                            'empresa': tarifa.empresa,
                            'rubro': tarifa.rubro,
                            'descripcion_rubro': descripcion_rubro,
                            'ano': str(tarifa.ano),
                            'valor': str(tarifa.valor),
                            'frecuencia': tarifa.frecuencia,
                            'tipo': tarifa.tipo,
                            'categoria': tarifa.categoria
                        },
                        'mensaje': f'Tarifa encontrada: {tarifa.descripcion}'
                    })
                else:
                    print(f"[ERROR] Tarifa no encontrada: {codigo_tarifa}")
                    return JsonResponse({
                        'exito': False,
                        'mensaje': f'No se encontró la tarifa {codigo_tarifa} en el municipio {empresa}'
                    })
            except Exception as e:
                print(f"[ERROR] Error en búsqueda de tarifa: {e}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'Error al buscar tarifa: {str(e)}'
                })
        except Exception as e:
            print(f"[ERROR] Error general en búsqueda de tarifa: {e}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error en la búsqueda: {str(e)}'
            })
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'})

@csrf_exempt
def buscar_tarifa(request):
    """Vista AJAX para buscar tarifa por empresa y código de tarifa"""
    if request.method == 'POST':
        try:
            empresa = request.POST.get('empresa', '').strip()
            cod_tarifa = request.POST.get('cod_tarifa', '').strip()
            
            print(f"[DEBUG] Buscando tarifa: empresa={empresa}, cod_tarifa={cod_tarifa}")
            
            # Validar que los campos requeridos estén presentes
            if not empresa:
                print("[ERROR] Empresa vacía")
                return JsonResponse({'exito': False, 'mensaje': 'El código de municipio es obligatorio'})
            
            if not cod_tarifa:
                print("[ERROR] Código de tarifa vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El código de tarifa es obligatorio'})
            
            try:
                from tributario_app.models import Tarifas
                # Buscar tarifa por empresa y código de tarifa (más reciente)
                tarifa = Tarifas.objects.filter(
                    empresa=empresa,
                    cod_tarifa=cod_tarifa
                ).order_by('-ano').first()
                
                if tarifa:
                    print(f"[OK] Tarifa encontrada: {tarifa.descripcion}")
                    return JsonResponse({
                        'exito': True,
                        'tarifa': {
                            'codigo': tarifa.cod_tarifa,
                            'descripcion': tarifa.descripcion,
                            'valor': str(tarifa.valor),
                            'frecuencia': tarifa.frecuencia,
                            'tipo': tarifa.tipo,
                            'ano': str(tarifa.ano),
                            'rubro': tarifa.rubro,
                            'empresa': tarifa.empresa
                        },
                        'mensaje': f'Tarifa encontrada: {tarifa.descripcion}'
                    })
                else:
                    print(f"[INFO] Tarifa no encontrada para empresa={empresa}, cod_tarifa={cod_tarifa}")
                    return JsonResponse({
                        'exito': False,
                        'mensaje': f'No se encontró tarifa con código {cod_tarifa} para el municipio {empresa}'
                    })
            except Exception as e:
                print(f"[ERROR] Error al buscar tarifa: {str(e)}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'Error en la búsqueda: {str(e)}'
                })
        except Exception as e:
            print(f"[ERROR] Error en búsqueda AJAX: {e}")
            return JsonResponse({'exito': False, 'mensaje': f'Error en el servidor: {str(e)}'})
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'})

@csrf_exempt
def buscar_tarifa_automatica(request):
    """Vista AJAX para búsqueda automática de tarifa con validación completa"""
    if request.method == 'POST':
        try:
            empresa = request.POST.get('empresa', '').strip()
            rubro = request.POST.get('rubro', '').strip()
            ano = request.POST.get('ano', '').strip()
            codigo = request.POST.get('cod_tarifa', '').strip()
            
            print(f"[DEBUG] Búsqueda automática: empresa={empresa}, rubro={rubro}, año={ano}, codigo={codigo}")
            
            # Validar campos mínimos requeridos
            if not empresa:
                print("[ERROR] Empresa vacía")
                return JsonResponse({'exito': False, 'mensaje': 'El código de municipio es obligatorio'})
            
            if not codigo:
                print("[ERROR] Código de tarifa vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El código de tarifa es obligatorio'})
            
            # Si no hay rubro o año, buscar solo por empresa y código de tarifa
            if not rubro or not ano:
                print(f"[DEBUG] Búsqueda simplificada: empresa={empresa}, codigo={codigo}")
                try:
                    from tributario_app.models import Tarifas
                    # Buscar tarifa solo por empresa y código de tarifa (más reciente)
                    tarifa = Tarifas.objects.filter(
                        empresa=empresa,
                        cod_tarifa=codigo
                    ).order_by('-ano').first()
                    
                    if tarifa:
                        print(f"[OK] Tarifa encontrada: {tarifa.descripcion}")
                        return JsonResponse({
                            'exito': True,
                            'tarifa': {
                                'id': tarifa.id,
                                'codigo': tarifa.cod_tarifa,
                                'descripcion': tarifa.descripcion,
                                'valor': str(tarifa.valor),
                                'frecuencia': tarifa.frecuencia,
                                'tipo': tarifa.tipo,
                                'categoria': tarifa.categoria,
                                'ano': str(tarifa.ano),
                                'rubro': tarifa.rubro,
                                'empresa': tarifa.empresa
                            },
                            'mensaje': f'Tarifa encontrada: {tarifa.descripcion}',
                            'encontrado_en_otro_ano': False
                        })
                    else:
                        print(f"[ERROR] Tarifa no encontrada: empresa={empresa}, codigo={codigo}")
                        return JsonResponse({
                            'exito': False, 
                            'mensaje': f'No se encontró una tarifa con código "{codigo}". Puede crear una nueva tarifa.'
                        })
                except Exception as e:
                    print(f"[ERROR] Error en búsqueda simplificada: {e}")
                    return JsonResponse({'exito': False, 'mensaje': f'Error en el servidor: {str(e)}'})
            
            try:
                from tributario_app.models import Tarifas
                # Buscar tarifa con los cuatro criterios: empresa, rubro, año y código de tarifa
                tarifa = Tarifas.objects.get(
                    empresa=empresa,
                    rubro=rubro,
                    ano=ano,
                    cod_tarifa=codigo
                )
                print(f"[OK] Tarifa encontrada: {tarifa.descripcion}")
                return JsonResponse({
                    'exito': True,
                    'tarifa': {
                        'id': tarifa.id,
                        'codigo': tarifa.cod_tarifa,
                        'descripcion': tarifa.descripcion,
                        'valor': str(tarifa.valor),
                        'frecuencia': tarifa.frecuencia,
                        'tipo': tarifa.tipo,
                        'categoria': tarifa.categoria,
                        'ano': str(tarifa.ano),
                        'rubro': tarifa.rubro,
                        'empresa': tarifa.empresa
                    },
                    'mensaje': f'Tarifa encontrada: {tarifa.descripcion}',
                    'encontrado_en_otro_ano': False
                })
            except Tarifas.DoesNotExist:
                print(f"[ERROR] Tarifa no encontrada: empresa={empresa}, rubro={rubro}, año={ano}, codigo={codigo}")
                return JsonResponse({
                    'exito': False, 
                    'mensaje': f'No se encontró una tarifa con código "{codigo}" para el rubro "{rubro}" en el año "{ano}". Puede crear una nueva tarifa.'
                })
        except Exception as e:
            print(f"[ERROR] Error en búsqueda automática: {e}")
            return JsonResponse({'exito': False, 'mensaje': f'Error en el servidor: {str(e)}'})
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'})

def plan_arbitrio(request):
    """Vista para plan de arbitrios"""
    return render(request, 'formulario_plan_arbitrio.html', {
        'modulo': 'Tributario',
        'descripcion': 'Plan de Arbitrios'
    })

@csrf_exempt
def buscar_plan_arbitrio(request):
    """Vista AJAX para buscar plan de arbitrio según código de tarifa"""
    if request.method == 'POST':
        try:
            empresa = request.POST.get('empresa', '').strip()
            rubro = request.POST.get('rubro', '').strip()
            ano = request.POST.get('ano', '').strip()
            cod_tarifa = request.POST.get('cod_tarifa', '').strip()
            
            print(f"[DEBUG] Búsqueda automática de plan: empresa={empresa}, rubro={rubro}, año={ano}, cod_tarifa={cod_tarifa}")
            
            # Validar que todos los campos requeridos estén presentes
            if not empresa:
                print("[ERROR] Empresa vacía")
                return JsonResponse({'exito': False, 'mensaje': 'El código de municipio es obligatorio'})
            
            if not rubro:
                print("[ERROR] Rubro vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El código de rubro es obligatorio'})
            
            if not ano:
                print("[ERROR] Año vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El año es obligatorio'})
            
            if not cod_tarifa:
                print("[ERROR] Código de tarifa vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El código de tarifa es obligatorio'})
            
            from tributario_app.models import PlanArbitrio
            # Buscar plan con los cuatro criterios: empresa, rubro, año y código de tarifa
            # Usar filter().first() para manejar posibles duplicados
            plan = PlanArbitrio.objects.filter(
                empresa=empresa,
                rubro=rubro,
                ano=ano,
                cod_tarifa=cod_tarifa
            ).first()
            
            if plan:
                print(f"[OK] Plan encontrado: {plan.descripcion}")
                return JsonResponse({
                    'exito': True,
                    'plan': {
                        'id': plan.id,
                        'empresa': plan.empresa,
                        'rubro': plan.rubro,
                        'cod_tarifa': plan.cod_tarifa,
                        'ano': str(plan.ano),
                        'codigo': plan.codigo,
                        'descripcion': plan.descripcion,
                        'minimo': str(plan.minimo),
                        'maximo': str(plan.maximo),
                        'valor': str(plan.valor)
                    },
                    'mensaje': f'Plan encontrado: {plan.descripcion}',
                    'encontrado_en_otro_ano': False
                })
            else:
                print(f"[ERROR] Plan no encontrado: empresa={empresa}, rubro={rubro}, año={ano}, cod_tarifa={cod_tarifa}")
                return JsonResponse({
                    'exito': False, 
                    'mensaje': f'No se encontró un plan con código de tarifa "{cod_tarifa}" para el rubro "{rubro}" en el año "{ano}". Puede crear un nuevo plan.'
                })
        except Exception as e:
            print(f"[ERROR] Error en búsqueda automática: {e}")
            return JsonResponse({'exito': False, 'mensaje': f'Error en el servidor: {str(e)}'})
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'})

@csrf_exempt
def buscar_plan_arbitrio_por_codigo(request):
    """Vista AJAX para buscar plan de arbitrio según código"""
    if request.method == 'POST':
        try:
            empresa = request.POST.get('empresa', '').strip()
            rubro = request.POST.get('rubro', '').strip()
            ano = request.POST.get('ano', '').strip()
            codigo = request.POST.get('codigo', '').strip()
            
            print(f"[DEBUG] Búsqueda automática de plan por código: empresa={empresa}, rubro={rubro}, año={ano}, codigo={codigo}")
            print(f"[DEBUG] Tipos de datos: empresa={type(empresa)}, rubro={type(rubro)}, año={type(ano)}, codigo={type(codigo)}")
            
            # Validar que todos los campos requeridos estén presentes
            if not empresa:
                print("[ERROR] Empresa vacía")
                return JsonResponse({'exito': False, 'mensaje': 'El código de municipio es obligatorio'})
            
            if not rubro:
                print("[ERROR] Rubro vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El código de rubro es obligatorio'})
            
            if not ano:
                print("[ERROR] Año vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El año es obligatorio'})
            
            if not codigo:
                print("[ERROR] Código vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El código es obligatorio'})
            
            from tributario_app.models import PlanArbitrio
            print(f"[DEBUG] Iniciando búsqueda en base de datos...")
            
            # Buscar plan con los cuatro criterios: empresa, rubro, año y código
            plan = PlanArbitrio.objects.filter(
                empresa=empresa,
                rubro=rubro,
                ano=ano,
                codigo=codigo
            ).first()
            
            print(f"[DEBUG] Resultado de búsqueda: {plan}")
            
            if plan:
                print(f"[OK] Plan encontrado: {plan.descripcion}")
                return JsonResponse({
                    'exito': True,
                    'plan': {
                        'id': plan.id,
                        'empresa': plan.empresa,
                        'rubro': plan.rubro,
                        'cod_tarifa': plan.cod_tarifa,
                        'ano': str(plan.ano),
                        'codigo': plan.codigo,
                        'descripcion': plan.descripcion,
                        'minimo': str(plan.minimo),
                        'maximo': str(plan.maximo),
                        'valor': str(plan.valor)
                    },
                    'mensaje': f'Plan encontrado: {plan.descripcion}',
                    'encontrado_en_otro_ano': False
                })
            else:
                print(f"[ERROR] Plan no encontrado: empresa={empresa}, rubro={rubro}, año={ano}, codigo={codigo}")
                return JsonResponse({
                    'exito': False, 
                    'mensaje': f'No se encontró un plan con código "{codigo}" para el rubro "{rubro}" en el año "{ano}". Puede crear un nuevo plan.'
                })
        except Exception as e:
            print(f"[ERROR] Error en búsqueda automática: {e}")
            return JsonResponse({'exito': False, 'mensaje': f'Error en el servidor: {str(e)}'})
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'})

@csrf_exempt
def buscar_rubro(request):
    """Vista AJAX para buscar rubro por empresa y código"""
    if request.method == 'POST':
        try:
            empresa = request.POST.get('empresa', '').strip()
            codigo = request.POST.get('codigo', '').strip()
            
            print(f"[DEBUG] Buscando rubro: empresa={empresa}, codigo={codigo}")
            
            if not empresa or not codigo:
                print("[ERROR] Empresa o código vacíos")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Empresa y código son obligatorios'
                })
            
            # Buscar en la tabla rubro
            try:
                from tributario_app.models import Rubro
                rubro = Rubro.objects.get(empresa=empresa, codigo=codigo)
                
                print(f"[OK] Rubro encontrado: {rubro.descripcion}")
                
                return JsonResponse({
                    'exito': True,
                    'rubro': {
                        'codigo': rubro.codigo,
                        'descripcion': rubro.descripcion,
                        'tipo': rubro.tipo,
                        'cuenta': rubro.cuenta,
                        'cuentarez': rubro.cuentarez,
                        'empresa': rubro.empresa
                    }
                })
            except Rubro.DoesNotExist:
                print(f"[ERROR] Rubro no encontrado: empresa={empresa}, codigo={codigo}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Rubro no encontrado'
                })
                
        except Exception as e:
            print(f"[ERROR] Error en búsqueda AJAX: {e}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error en el servidor: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

@csrf_exempt
def buscar_identificacion(request):
    """Vista AJAX para buscar identificación por DNI"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            identidad = data.get('identidad', '').strip()
            
            if not identidad:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'El número de identidad es obligatorio'
                })
            
            # Buscar en la tabla identificacion
            try:
                from tributario_app.models import Identificacion
                identificacion = Identificacion.objects.get(identidad=identidad)
                
                return JsonResponse({
                    'exito': True,
                    'identificacion': {
                        'identidad': identificacion.identidad,
                        'nombres': identificacion.nombres or '',
                        'apellidos': identificacion.apellidos or '',
                        'nombre_completo': f"{identificacion.nombres or ''} {identificacion.apellidos or ''}".strip()
                    }
                })
            except Identificacion.DoesNotExist:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Identidad no encontrada en la base de datos'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Datos JSON inválidos'
            })
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error en el servidor: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

@require_http_methods(["GET"])
def api_tarifas_ics(request):
    """
    API para obtener las tarifas ICS desde la tabla tarifasimptoics
    URL: /tributario/api/tarifas-ics/?categoria=2
    """
    try:
        from tributario_app.models import TarifasImptoics
        
        categoria = request.GET.get('categoria', '1')
        
        # Obtener tarifas ordenadas por rango1
        tarifas = TarifasImptoics.objects.filter(
            categoria=categoria
        ).order_by('rango1')
        
        # Convertir a lista de diccionarios
        tarifas_data = []
        for tarifa in tarifas:
            tarifas_data.append({
                'id': tarifa.id,
                'categoria': tarifa.categoria,
                'descripcion': tarifa.descripcion or f'Rango {tarifa.rango1} - {tarifa.rango2}',
                'codigo': float(tarifa.codigo) if tarifa.codigo else 0,
                'rango1': float(tarifa.rango1),
                'rango2': float(tarifa.rango2),
                'valor': float(tarifa.valor)
            })
        
        return JsonResponse({
            'success': True,
            'tarifas': tarifas_data,
            'categoria': categoria,
            'total': len(tarifas_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Error al obtener las tarifas ICS'
        }, status=500)

@csrf_exempt
def buscar_identificacion_representante(request):
    """Vista AJAX para buscar identificación del representante legal por DNI"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            identidad = data.get('identidad', '').strip()
            
            if not identidad:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'El número de identidad es obligatorio'
                })
            
            # Buscar en la tabla identificacion
            try:
                from tributario_app.models import Identificacion
                identificacion = Identificacion.objects.get(identidad=identidad)
                
                return JsonResponse({
                    'exito': True,
                    'identificacion': {
                        'identidad': identificacion.identidad,
                        'nombres': identificacion.nombres or '',
                        'apellidos': identificacion.apellidos or '',
                        'nombre_completo': f"{identificacion.nombres or ''} {identificacion.apellidos or ''}".strip()
                    }
                })
            except Identificacion.DoesNotExist:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Identidad del representante no encontrada en la base de datos'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Datos JSON inválidos'
            })
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error en el servidor: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

@require_http_methods(["GET"])
def api_tarifas_ics(request):
    """
    API para obtener las tarifas ICS desde la tabla tarifasimptoics
    URL: /tributario/api/tarifas-ics/?categoria=2
    """
    try:
        from tributario_app.models import TarifasImptoics
        
        categoria = request.GET.get('categoria', '1')
        
        # Obtener tarifas ordenadas por rango1
        tarifas = TarifasImptoics.objects.filter(
            categoria=categoria
        ).order_by('rango1')
        
        # Convertir a lista de diccionarios
        tarifas_data = []
        for tarifa in tarifas:
            tarifas_data.append({
                'id': tarifa.id,
                'categoria': tarifa.categoria,
                'descripcion': tarifa.descripcion or f'Rango {tarifa.rango1} - {tarifa.rango2}',
                'codigo': float(tarifa.codigo) if tarifa.codigo else 0,
                'rango1': float(tarifa.rango1),
                'rango2': float(tarifa.rango2),
                'valor': float(tarifa.valor)
            })
        
        return JsonResponse({
            'success': True,
            'tarifas': tarifas_data,
            'categoria': categoria,
            'total': len(tarifas_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Error al obtener las tarifas ICS'
        }, status=500)

@csrf_exempt
def calcular_tasas_ajax(request):
    """Vista AJAX para calcular tasas basadas en el volumen declarado"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            empresa = data.get('empresa', '')
            rubro = data.get('rubro', '')
            ano = int(data.get('ano', 2024))
            volumen_total = data.get('volumen_total')
            
            if not empresa or not rubro:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Empresa y rubro son requeridos'
                })
            
            from tributario_app.models import PlanArbitrio
            
            # Convertir volumen_total a float si existe
            if volumen_total is not None:
                volumen_total = float(volumen_total)
            
            # Obtener todas las tasas (fijas y variables)
            resultado_tasas = PlanArbitrio.obtener_tasas_por_negocio(
                empresa=empresa,
                rubro=rubro,
                ano=ano,
                volumen_total=volumen_total
            )
            
            if resultado_tasas['exito']:
                return JsonResponse({
                    'exito': True,
                    'tasas_fijas': resultado_tasas['tasas_fijas'],
                    'tasas_variables': resultado_tasas['tasas_variables'],
                    'volumen_total': volumen_total,
                    'rubro': rubro,
                    'ano': ano,
                    'empresa': empresa
                })
            else:
                return JsonResponse({
                    'exito': False,
                    'mensaje': resultado_tasas['mensaje']
                })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Datos JSON inválidos'
            })
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error al calcular tasas: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

@csrf_exempt
def obtener_tarifas_rubro_ajax(request):
    """Vista AJAX para obtener tarifas disponibles para un rubro específico"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            negocio_id = data.get('negocio_id')
            rtm = data.get('rtm')
            expe = data.get('expe')
            rubro = data.get('rubro')
            tarifa_actual_id = data.get('tarifa_actual_id')
            
            print(f"[DEBUG] Buscando tarifas: negocio_id={negocio_id}, rtm={rtm}, expe={expe}, rubro={rubro}, tarifa_actual_id={tarifa_actual_id}")
            
            if not negocio_id or not rtm or not expe or not rubro:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'ID del negocio, RTM, Expediente y Rubro son requeridos'
                })
            
            # Obtener tarifas disponibles en tarifasics para este RTM, Expediente y Rubro específicos
            from tributario_app.models import TarifasICS
            tarifas_disponibles = TarifasICS.objects.filter(
                rtm=rtm,
                expe=expe,
                rubro=rubro
            )
            
            print(f"📊 Tarifas encontradas antes de excluir: {tarifas_disponibles.count()}")
            
            # Excluir la tarifa actual si se proporciona
            if tarifa_actual_id:
                tarifas_disponibles = tarifas_disponibles.exclude(id=tarifa_actual_id)
                print(f"📊 Tarifas encontradas después de excluir: {tarifa_actual_id}: {tarifas_disponibles.count()}")
            
            tarifas_disponibles = tarifas_disponibles.order_by('cod_tarifa')
            
            # Crear lista de opciones con información más detallada
            opciones = []
            for tarifa in tarifas_disponibles:
                # Crear una descripción más informativa
                descripcion = f"Tarifa {tarifa.cod_tarifa} (L. {tarifa.valor:.2f})"
                
                opciones.append({
                    'codigo': tarifa.cod_tarifa,
                    'descripcion': descripcion,
                    'valor': str(tarifa.valor),
                    'rtm': tarifa.rtm,
                    'expe': tarifa.expe,
                    'rubro': tarifa.rubro
                })
            
            print(f"[OK] Opciones generadas: {len(opciones)}")
            for opcion in opciones:
                print(f"   - {opcion['codigo']}: {opcion['descripcion']} (RTM: {opcion['rtm']}, Expe: {opcion['expe']})")
            
            return JsonResponse({
                'exito': True,
                'tarifas': opciones,
                'total_encontradas': len(opciones)
            })
            
        except Exception as e:
            print(f"[ERROR] Error en obtener_tarifas_rubro_ajax: {str(e)}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error al obtener tarifas: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

def obtener_tarifas_escalonadas(request):
    return JsonResponse({'exito': True, 'mensaje': 'Vista funcionando'})

@csrf_exempt
def buscar_rubro(request):
    """Vista AJAX para buscar rubro por empresa y código"""
    if request.method == 'POST':
        try:
            empresa = request.POST.get('empresa', '').strip()
            codigo = request.POST.get('codigo', '').strip()
            
            print(f"🔍 Buscando rubro: empresa={empresa}, codigo={codigo}")
            
            if not empresa or not codigo:
                print("❌ Empresa o código vacíos")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Empresa y código son obligatorios'
                })
            
            # Buscar en la tabla rubros
            try:
                from tributario_app.models import Rubro
                rubro = Rubro.objects.get(empresa=empresa, codigo=codigo)
                
                print(f"✅ Rubro encontrado: {rubro.descripcion}")
                
                return JsonResponse({
                    'exito': True,
                    'rubro': {
                        'codigo': rubro.codigo,
                        'descripcion': rubro.descripcion or '',
                        'tipo': rubro.tipo or '',
                        'cuenta': rubro.cuenta or '',
                        'cuentarez': rubro.cuentarez or ''
                    },
                    'mensaje': 'Rubro encontrado'
                })
            except Rubro.DoesNotExist:
                print(f"❌ Rubro no encontrado: empresa={empresa}, codigo={codigo}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Rubro no encontrado'
                })
                
        except Exception as e:
            print(f"❌ Error en búsqueda AJAX: {e}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error en el servidor: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

