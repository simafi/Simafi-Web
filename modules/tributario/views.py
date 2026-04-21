from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

@login_required
def tributario_login_old(request):
    """Vista de login/dashboard del módulo tributario"""
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    context = {
        'municipio_codigo': municipio_codigo,
        'modulo': 'Tributario',
        'descripcion': 'Sistema de Gestión Tributaria Municipal'
    }
    
    return render(request, 'tributario/dashboard.html', context)

@csrf_exempt
def maestro_negocios(request):
    """Vista para el maestro de negocios"""
    # Obtener el municipio del usuario desde la sesión
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    # Manejar solicitudes POST (formulario tradicional y/o AJAX JSON)
    if request.method == 'POST':
        try:
            # Diferenciar entre JSON y formulario tradicional
            is_json = request.content_type and 'application/json' in request.content_type
            if is_json:
                data = json.loads(request.body or '{}')
                accion = data.get('accion')
                rtm = data.get('rtm', '')
                expe = data.get('expe', '')
            else:
                data = request.POST
                accion = data.get('accion')
                rtm = data.get('rtm', '')
                expe = data.get('expe', '')
            
            if accion == 'salvar' and is_json:
                return handle_salvar_negocio(request, data)
            elif accion == 'eliminar' and is_json:
                return handle_eliminar_negocio(request, data)
            elif accion == 'configuracion':
                # Redirigir a la página de configuración de tasas
                if rtm and expe:
                    url = f'/tributario/configurar-tasas-negocio/?rtm={rtm}&expe={expe}'
                    return JsonResponse({'exito': True, 'redirect': url}) if is_json else redirect(url)
                else:
                    return JsonResponse({
                        'exito': False,
                        'mensaje': 'RTM y Expediente son requeridos para configurar tasas'
                    })
            elif accion == 'declaracion':
                # Redirigir a la página de declaración de volumen
                if rtm and expe:
                    url = f'/tributario/declaracion-volumen/?rtm={rtm}&expe={expe}'
                    return JsonResponse({'exito': True, 'redirect': url}) if is_json else redirect(url)
                else:
                    return JsonResponse({
                        'exito': False,
                        'mensaje': 'RTM y Expediente son requeridos para declaración de volumen'
                    })
            elif accion == 'estado':
                # Redirigir al Estado de Cuenta
                if rtm and expe:
                    # Obtener empresa desde la sesión o desde los datos
                    empresa_estado = data.get('empresa', '') if isinstance(data, dict) else request.POST.get('empresa', '')
                    if not empresa_estado:
                        empresa_estado = municipio_codigo
                    url = f'/tributario/estado-cuenta/?empresa={empresa_estado}&rtm={rtm}&expe={expe}'
                    return JsonResponse({'exito': True, 'redirect': url}) if is_json else redirect(url)
                else:
                    return JsonResponse({
                        'exito': False,
                        'mensaje': 'RTM y Expediente son requeridos para Estado de Cuenta'
                    })
            else:
                # Para formularios tradicionales, no devolver JSON de error
                if not is_json:
                    return redirect('tributario:maestro_negocios')
                return JsonResponse({'exito': False, 'mensaje': 'Acción no válida'})
        
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error en el servidor: {str(e)}'
            })
    
    # Manejar solicitudes GET para mostrar el formulario
    # Verificar si se está regresando desde otro formulario con parámetros
    rtm_regreso = request.GET.get('rtm', '').strip()
    expe_regreso = request.GET.get('expe', '').strip()
    empresa_regreso = request.GET.get('empresa', '').strip() or municipio_codigo
    
    # Crear un objeto negocio vacío para el formulario
    negocio = {
        'empresa': municipio_codigo,
        'empre': municipio_codigo,
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
    
    # Si hay parámetros de regreso, cargar el negocio completo
    if rtm_regreso and expe_regreso:
        try:
            from tributario.models import Negocio
            negocio_existente = Negocio.objects.get(
                empresa=empresa_regreso,
                rtm=rtm_regreso,
                expe=expe_regreso
            )
            # Convertir el objeto Negocio a diccionario para el template
            negocio = {
                'empresa': negocio_existente.empresa,
                'empre': negocio_existente.empresa,
                'rtm': negocio_existente.rtm,
                'expe': negocio_existente.expe,
                'fecha_ini': negocio_existente.fecha_ini.strftime('%Y-%m-%d') if negocio_existente.fecha_ini else '',
                'fecha_can': negocio_existente.fecha_can.strftime('%Y-%m-%d') if negocio_existente.fecha_can else '',
                'identidad': negocio_existente.identidad or '',
                'rtnpersonal': negocio_existente.rtnpersonal or '',
                'comerciante': negocio_existente.comerciante or '',
                'rtnnego': negocio_existente.rtnnego or '',
                'nombrenego': negocio_existente.nombrenego or '',
                'actividad': negocio_existente.actividad or '',
                'identidadrep': negocio_existente.identidadrep or '',
                'representante': negocio_existente.representante or '',
                'estatus': negocio_existente.estatus or 'A',
                'catastral': negocio_existente.catastral or '',
                'cx': str(negocio_existente.cx) if negocio_existente.cx else '0.0000000',
                'cy': str(negocio_existente.cy) if negocio_existente.cy else '0.0000000',
                'direccion': negocio_existente.direccion or '',
                'telefono': negocio_existente.telefono or '',
                'celular': negocio_existente.celular or '',
                'correo': negocio_existente.correo or '',
                'pagweb': negocio_existente.pagweb or '',
                'socios': negocio_existente.socios or '',
                'comentario': negocio_existente.comentario or ''
            }
        except Exception:
            # Si no se encuentra, usar los valores básicos de rtm y expe
            negocio['empresa'] = empresa_regreso
            negocio['empre'] = empresa_regreso
            negocio['rtm'] = rtm_regreso
            negocio['expe'] = expe_regreso
    
    # Obtener actividades económicas desde la tabla actividad
    try:
        from tributario.models import Actividad
        actividades = Actividad.objects.filter(empresa=municipio_codigo).order_by('codigo')
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
    
    return render(request, 'maestro_negocios.html', {
        'negocio': negocio,
        'actividades': actividades_list,
        'empresa': municipio_codigo,
        'municipio_codigo': municipio_codigo,
        'modulo': 'Tributario',
        'descripcion': 'Maestro de Negocios'
    })

def handle_salvar_negocio(request, data):
    """Maneja el guardado de un negocio"""
    try:
        from tributario.models import Negocio
        
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
        from tributario.models import Negocio
        
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

def oficina_crud(request):
    """Vista para CRUD de oficinas"""
    # Obtener el municipio del usuario desde la sesión
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    # Variables para el contexto
    oficinas = []
    empresa_filtro = None
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        try:
            from tributario.models import Oficina
            
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
    if municipio_codigo:
        try:
            from tributario.models import Oficina
            oficinas = Oficina.objects.filter(empresa=municipio_codigo).order_by('codigo')
            empresa_filtro = municipio_codigo
        except Exception as e:
            print(f"Error al cargar oficinas: {e}")
            oficinas = []
    
    return render(request, 'oficina.html', {
        'empresa': municipio_codigo,
        'oficinas': oficinas,
        'empresa_filtro': empresa_filtro,
        'mensaje': mensaje,
        'exito': exito,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Oficinas'
    })

def actividad_crud(request):
    """Vista para CRUD de actividades"""
    # Obtener la empresa del usuario desde la sesión (viene del login)
    # Unificar: usar 'empresa' de la sesión (establecido en login)
    empresa = request.session.get('empresa', '0301')
    
    # Variables para el contexto - simplificar y unificar
    actividades = []
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        try:
            from tributario.models import Actividad
            
            # CRÍTICO: Capturar la acción del POST
            accion = request.POST.get('accion', '').strip()
            print(f"\n{'='*60}")
            print(f"🔍 [POST RECIBIDO] Acción detectada: '{accion}'")
            print(f"{'='*60}")
            print(f"   Método: {request.method}")
            print(f"   Todos los keys POST: {list(request.POST.keys())}")
            print(f"   ¿accion en POST?: {'accion' in request.POST}")
            if 'accion' in request.POST:
                print(f"   Valor de accion: '{request.POST.get('accion')}'")
            print(f"{'='*60}\n")
            
            # CRÍTICO: Usar empresa de la sesión como base, y solo usar POST si viene
            # Esto evita conflictos de variables
            empresa_sesion = request.session.get('empresa', '0301')
            empresa_post = request.POST.get('empresa', '').strip()
            # Usar empresa del POST si está presente, sino usar la de la sesión
            empresa = empresa_post if empresa_post else empresa_sesion
            
            print(f"🔍 [VARIABLE EMPRESA]")
            print(f"   - empresa_sesion: '{empresa_sesion}'")
            print(f"   - empresa_post: '{empresa_post}'")
            print(f"   - empresa (final): '{empresa}'")
            
            # Cuenta y código son el mismo campo - priorizar cuenta del formulario
            cuenta = request.POST.get('cuenta', '').strip()
            codigo = request.POST.get('codigo', '').strip()
            # Usar cuenta si está disponible, sino usar codigo (para compatibilidad con eliminación)
            codigo = cuenta if cuenta else codigo
            
            print(f"🔍 [VARIABLE CODIGO/CUENTA]")
            print(f"   - cuenta (POST): '{cuenta}'")
            print(f"   - codigo (POST): '{codigo}'")
            print(f"   - codigo (final): '{codigo}'")
            # Capturar campos del POST - asegurar que cuentarec se capture correctamente
            # IMPORTANTE: Usar get() con valor por defecto '' para capturar campos vacíos también
            # CRÍTICO: Capturar cuentarec de múltiples formas para asegurar que se obtenga
            cuentarez_raw = request.POST.get('cuentarez', '')
            cuentarec_raw = request.POST.get('cuentarec', '')
            
            # Si cuentarec no está en POST, intentar obtenerlo de otra forma
            if 'cuentarec' not in request.POST and cuentarec_raw == '':
                # Intentar obtener de request.POST.getlist() por si hay múltiples valores
                cuentarec_list = request.POST.getlist('cuentarec')
                if cuentarec_list:
                    cuentarec_raw = cuentarec_list[-1]  # Tomar el último valor si hay múltiples
                    print(f"⚠️ [ADVERTENCIA] cuentarec obtenido de getlist(): {repr(cuentarec_raw)}")
            
            cuentarez = cuentarez_raw.strip() if cuentarez_raw else ''
            cuentarec = cuentarec_raw.strip() if cuentarec_raw else ''
            descripcion = request.POST.get('descripcion', '').strip()
            
            # Log específico para cuentarec antes de procesar
            print(f"\n🔍 [CAPTURA CAMPOS] Valores capturados del POST:")
            print(f"   cuentarez (raw): {repr(cuentarez_raw)}")
            print(f"   cuentarec (raw): {repr(cuentarec_raw)}")
            print(f"   cuentarez (procesado): {repr(cuentarez)}")
            print(f"   cuentarec (procesado): {repr(cuentarec)}")
            print(f"   ¿cuentarec en POST?: {'cuentarec' in request.POST}")
            print(f"   Todos los keys POST: {list(request.POST.keys())}")
            
            # Verificar si hay múltiples valores de cuentarec
            cuentarec_list = request.POST.getlist('cuentarec')
            if len(cuentarec_list) > 1:
                print(f"⚠️ [ADVERTENCIA] Hay {len(cuentarec_list)} valores de cuentarec en POST:")
                for i, val in enumerate(cuentarec_list):
                    print(f"      cuentarec[{i}]: {repr(val)}")
                print(f"   Usando el último valor: {repr(cuentarec_list[-1])}")
                cuentarec = cuentarec_list[-1].strip() if cuentarec_list[-1] else ''
            
            # Log de depuración: verificar todos los campos POST
            print(f"\n{'='*60}")
            print(f"🔍 [DEBUG POST] Todos los campos recibidos:")
            print(f"{'='*60}")
            for key, value in request.POST.items():
                print(f"   {key}: '{value}'")
            print(f"{'='*60}\n")
            
            # Verificación específica de cuentarec
            if 'cuentarec' not in request.POST:
                print(f"⚠️  [ADVERTENCIA] Campo 'cuentarec' NO está en request.POST")
                print(f"   Campos disponibles: {list(request.POST.keys())}")
            else:
                cuentarec_val = request.POST.get('cuentarec')
                print(f"✅ Campo 'cuentarec' encontrado en POST: '{cuentarec_val}'")
                print(f"   Tipo: {type(cuentarec_val)}, Longitud: {len(cuentarec_val) if cuentarec_val else 0}")
            
            if not accion:
                print(f"⚠️ [ADVERTENCIA] No se recibió acción en POST")
                print(f"   Campos disponibles: {list(request.POST.keys())}")
                mensaje = 'Error: No se recibió la acción del formulario'
                exito = False
            elif accion == 'nuevo':
                # Limpiar campos para nuevo registro
                print(f"✅ [ACCIÓN] Preparando formulario para nueva actividad")
                mensaje = 'Formulario preparado para nueva actividad'
                exito = True
                
            elif accion == 'guardar':
                # SIN VALIDACIONES - PERMITIR GUARDAR SIEMPRE
                # Usar valores por defecto si están vacíos
                if not empresa or str(empresa).strip() == '':
                    empresa = empresa_sesion
                
                if not codigo or str(codigo).strip() == '':
                    codigo = cuenta if cuenta and str(cuenta).strip() != '' else ''
                
                # Normalizar valores
                empresa = str(empresa).strip() if empresa else empresa_sesion
                codigo = str(codigo).strip() if codigo else ''
                descripcion = str(descripcion).strip() if descripcion else ''
                cuentarez = str(cuentarez).strip() if cuentarez else ''
                cuentarec = str(cuentarec).strip() if cuentarec else ''
                
                # GUARDAR - SIN VALIDACIONES
                try:
                    if codigo and Actividad.objects.filter(empresa=empresa, codigo=codigo).exists():
                        # Actualizar
                        actividad = Actividad.objects.get(empresa=empresa, codigo=codigo)
                        actividad.descripcion = descripcion
                        actividad.cuentarez = cuentarez
                        actividad.cuentarec = cuentarec
                        actividad.save()
                        mensaje = f'Actividad {codigo} actualizada correctamente'
                        exito = True
                    elif codigo:
                        # Crear
                        Actividad.objects.create(
                            empresa=empresa,
                            codigo=codigo,
                            descripcion=descripcion,
                            cuentarez=cuentarez,
                            cuentarec=cuentarec
                        )
                        mensaje = f'Actividad {codigo} creada correctamente'
                        exito = True
                    else:
                        mensaje = 'Error: El código/cuenta es necesario para guardar'
                        exito = False
                except Exception as e:
                    mensaje = f'Error al guardar: {str(e)}'
                    exito = False
                        
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
    
    # Cargar actividades usando la empresa de la sesión
    try:
        from tributario.models import Actividad
        actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
    except Exception as e:
        print(f"Error al cargar actividades: {e}")
        actividades = []
    
    # Contexto unificado - usar 'empresa' y 'empresa_filtro' con el mismo valor
    return render(request, 'actividad.html', {
        'empresa': empresa,
        'empresa_filtro': empresa,  # Mismo valor para evitar conflictos
        'actividades': actividades,
        'mensaje': mensaje,
        'exito': exito,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Actividades'
    })

def rubros_crud(request):
    """Vista para CRUD de rubros"""
    # Obtener el municipio del usuario desde la sesión
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    # Variables para el contexto
    rubros = []
    actividades = []
    empresa_filtro = None
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        try:
            from tributario.models import Rubro, Actividad
            
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
                    else:
                        try:
                            # Crear nuevo rubro
                            Rubro.objects.create(
                                empresa=empresa,
                                codigo=codigo,
                                descripcion=descripcion.strip() if descripcion else '',
                                tipo=tipo.strip() if tipo else '',
                                cuenta=cuenta.strip() if cuenta else '',
                                cuentarez=cuentarez.strip() if cuentarez else ''
                            )
                            mensaje = f'Rubro {codigo} creado correctamente'
                            exito = True
                        except Exception as e:
                            mensaje = f'Error al crear rubro: {str(e)}'
                            exito = False
                        
            elif action == 'eliminar':
                codigo_eliminar = request.POST.get('codigo')
                empresa_eliminar = request.POST.get('empresa')
                
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
                    mensaje = 'Código y empresa son obligatorios para eliminar'
                    exito = False
                    
        except Exception as e:
            mensaje = f'Error: {str(e)}'
            exito = False
    
    # Cargar rubros si hay un municipio seleccionado
    if municipio_codigo:
        try:
            from tributario.models import Rubro, Actividad
            rubros = Rubro.objects.filter(empresa=municipio_codigo).order_by('codigo')
            actividades = Actividad.objects.filter(empresa=municipio_codigo).order_by('codigo')
            empresa_filtro = municipio_codigo
        except Exception as e:
            print(f"Error al cargar rubros: {e}")
            rubros = []
            actividades = []
    
    return render(request, 'formulario_rubros.html', {
        'empresa': municipio_codigo,
        'rubros': rubros,
        'actividades': actividades,
        'empresa_filtro': empresa_filtro,
        'mensaje': mensaje,
        'exito': exito,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Rubros'
    })

@csrf_exempt
def buscar_negocio_ajax(request):
    """Vista AJAX para buscar negocio por RTM y expediente"""
    try:
        # Obtener datos tanto de GET como de POST
        if request.method == 'GET':
            rtm = request.GET.get('rtm', '')
            expe = request.GET.get('expe', '')
            municipio_codigo = request.GET.get('empre', '0301')
        elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                rtm = data.get('rtm', '')
                expe = data.get('expe', '')
                municipio_codigo = data.get('municipio_codigo', '0301')
            except json.JSONDecodeError:
                # Si no es JSON, intentar con form data
                rtm = request.POST.get('rtm', '')
                expe = request.POST.get('expe', '')
                municipio_codigo = request.POST.get('empre', '0301')
        else:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Método no permitido'
            })
        
        print(f"🔍 Buscando negocio: empre={municipio_codigo}, rtm={rtm}, expe={expe}")
        
        if rtm and expe:
            from tributario.models import Negocio
            try:
                negocio = Negocio.objects.get(
                    empre=municipio_codigo,
                    rtm=rtm,
                    expe=expe
                )
                
                print(f"✅ Negocio encontrado: {negocio.nombrenego}")
                
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
                print(f"❌ Negocio no encontrado: empre={municipio_codigo}, rtm={rtm}, expe={expe}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Negocio no encontrado'
                })
            except Exception as e:
                print(f"❌ Error al buscar negocio: {e}")
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
        print(f"❌ Error general en buscar_negocio_ajax: {e}")
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error en el servidor: {str(e)}'
        })


def estado_cuenta(request):
    """Estado de Cuenta por negocio con filtros por rango de periodo y mora acumulativa"""
    from django.db.models import Sum, Coalesce, Value, F
    from django.contrib import messages
    from tributario.models import Negocio, TransaccionesIcs

    # Obtener empresa: priorizar GET sobre sesión, pero validar que coincidan
    empresa_get = request.GET.get('empresa', '').strip()
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    rtm = request.GET.get('rtm', '').strip()
    expe = request.GET.get('expe', '').strip()
    
    # Si no viene empresa en la URL pero hay rtm y expe, redirigir agregando empresa
    if not empresa_get and rtm and expe:
        # Redirigir agregando empresa desde la sesión
        from django.http import HttpResponseRedirect
        from urllib.parse import urlencode
        query_params = request.GET.copy()
        query_params['empresa'] = municipio_codigo
        redirect_url = f"{request.path}?{query_params.urlencode()}"
        return HttpResponseRedirect(redirect_url)
    
    # Usar empresa de GET si viene, sino usar la de sesión
    empresa_filtro = empresa_get if empresa_get else municipio_codigo
    
    # Validación de seguridad: si viene empresa por GET, debe coincidir con sesión
    if empresa_get and empresa_get != municipio_codigo:
        messages.error(request, f'⚠️ Error de seguridad: La empresa especificada ({empresa_get}) no coincide con su sesión ({municipio_codigo}).')
        empresa_filtro = municipio_codigo  # Forzar uso de sesión por seguridad

    # Validación: RTM, EXPE y Empresa son obligatorios
    if not rtm or not expe:
        messages.error(request, '⚠️ RTM y Expediente son obligatorios para consultar el Estado de Cuenta.')
    
    if not empresa_filtro:
        messages.error(request, '⚠️ Empresa es obligatoria para consultar el Estado de Cuenta.')

    # Filtros de periodo
    ano_desde = request.GET.get('ano_desde')
    mes_desde = request.GET.get('mes_desde')
    ano_hasta = request.GET.get('ano_hasta')
    mes_hasta = request.GET.get('mes_hasta')

    negocio = None
    transacciones = []
    totales = {'recargos': 0, 'intereses': 0, 'mora_total': 0, 'saldo_final': 0, 'saldo_anterior': 0}
    error_mensaje = None

    if rtm and expe and empresa_filtro:
        try:
            # Buscar negocio filtrando SIEMPRE por empresa para evitar conflictos entre municipios
            negocio = Negocio.objects.filter(empresa=empresa_filtro, rtm=rtm, expe=expe).first()
            
            if not negocio:
                error_mensaje = f'❌ No se encontró un negocio con RTM={rtm}, EXPE={expe} y Empresa={empresa_filtro}. Verifique que los datos sean correctos.'
            else:
                # Validar que el negocio pertenezca a la empresa correcta (doble validación)
                if negocio.empresa != empresa_filtro and negocio.empre != empresa_filtro:
                    error_mensaje = f'❌ Error: El negocio encontrado no pertenece a la empresa {empresa_filtro}.'
                    negocio = None

            # Filtrar transacciones SIEMPRE por empresa, rtm y expe (empresa es OBLIGATORIO)
            qs = TransaccionesIcs.objects.filter(
                empresa=empresa_filtro,  # OBLIGATORIO: filtro por empresa
                rtm=rtm,
                expe=expe
            )

            # Aplicar rango de periodos si se proporcionan
            # Convertir a tupla comparable (ano, mes) asumiendo mes como 2 dígitos
            def periodo_tuple(ano_val, mes_val):
                try:
                    return (int(ano_val), int(mes_val))
                except Exception:
                    return None

            if ano_desde and mes_desde:
                qs = qs.filter(ano__gte=ano_desde)
            if ano_hasta and mes_hasta:
                qs = qs.filter(ano__lte=ano_hasta)
            if mes_desde:
                qs = qs.filter(mes__gte=mes_desde)
            if mes_hasta:
                qs = qs.filter(mes__lte=mes_hasta)

            qs = qs.order_by('ano', 'mes', 'fecha', 'id')

            # Calcular acumulados antes de procesar transacciones
            acumulados = qs.aggregate(
                total_monto=Sum('monto')  # Suma de todos los montos (cargos positivos, pagos negativos)
            )

            # Convertir QuerySet a lista ANTES de agregar descripciones
            transacciones_lista = list(qs)
            
            # Agregar descripciones de rubros a cada transacción
            # VINCULACIÓN: rubros.empresa = transaccionesics.empresa AND rubros.codigo = transaccionesics.rubro
            from django.db import connection
            
            # Inicializar todas las transacciones con "-" por defecto
            for trans in transacciones_lista:
                trans.rubro_descripcion = "-"
            
            # Obtener valores únicos de empresa y rubro de las transacciones
            empresas_rubros = set()
            for trans in transacciones_lista:
                if trans.empresa and trans.rubro:
                    empresa_str = str(trans.empresa).strip()
                    rubro_str = str(trans.rubro).strip()
                    if empresa_str and rubro_str:
                        empresas_rubros.add((empresa_str, rubro_str))
            
            # Cargar todos los rubros necesarios usando una sola consulta SQL optimizada
            rubros_cache = {}
            if empresas_rubros:
                try:
                    with connection.cursor() as cursor:
                        # Crear lista de condiciones para la consulta IN
                        condiciones = []
                        params = []
                        for empresa_val, rubro_val in empresas_rubros:
                            condiciones.append("(TRIM(empresa) = TRIM(%s) AND TRIM(codigo) = TRIM(%s))")
                            params.extend([empresa_val, rubro_val])
                        
                        if condiciones:
                            # Consulta SQL optimizada: obtener todas las descripciones en una sola query
                            query = f"""
                                SELECT TRIM(empresa) as empresa, TRIM(codigo) as codigo, TRIM(descripcion) as descripcion
                                FROM rubros 
                                WHERE {' OR '.join(condiciones)}
                            """
                            
                            cursor.execute(query, params)
                            resultados = cursor.fetchall()
                            
                            # Construir el cache de descripciones
                            for row in resultados:
                                if row and len(row) >= 3:
                                    empresa_db = str(row[0]).strip() if row[0] else ''
                                    codigo_db = str(row[1]).strip() if row[1] else ''
                                    descripcion_db = str(row[2]).strip() if row[2] else ''
                                    
                                    if empresa_db and codigo_db and descripcion_db:
                                        rubros_cache[(empresa_db, codigo_db)] = descripcion_db
                                    
                except Exception as e:
                    print(f"[ESTADO_CUENTA] Error al cargar descripciones de rubros: {str(e)}")
            
            # Asignar descripciones a cada transacción desde el cache
            for trans in transacciones_lista:
                try:
                    if trans.empresa and trans.rubro:
                        empresa_val = str(trans.empresa).strip()
                        rubro_val = str(trans.rubro).strip()
                        
                        if empresa_val and rubro_val:
                            # Obtener descripción del cache
                            descripcion = rubros_cache.get((empresa_val, rubro_val), "-")
                            
                            # Si no está en cache, intentar búsqueda individual
                            if descripcion == "-":
                                try:
                                    with connection.cursor() as cursor:
                                        cursor.execute("""
                                            SELECT TRIM(descripcion) 
                                            FROM rubros 
                                            WHERE TRIM(empresa) = TRIM(%s) AND TRIM(codigo) = TRIM(%s)
                                            LIMIT 1
                                        """, [empresa_val, rubro_val])
                                        
                                        resultado = cursor.fetchone()
                                        if resultado and resultado[0]:
                                            descripcion_temp = str(resultado[0]).strip()
                                            if descripcion_temp:
                                                descripcion = descripcion_temp
                                                rubros_cache[(empresa_val, rubro_val)] = descripcion
                                except Exception:
                                    pass
                            
                            # Asignar la descripción
                            if descripcion and descripcion != "-" and descripcion.strip():
                                trans.rubro_descripcion = descripcion.strip()
                            else:
                                trans.rubro_descripcion = "-"
                        else:
                            trans.rubro_descripcion = "-"
                    else:
                        trans.rubro_descripcion = "-"
                except Exception as e:
                    trans.rubro_descripcion = "-"
            
            transacciones = transacciones_lista
            
            # Calcular totales basados en monto
            total_monto = float(acumulados.get('total_monto') or 0)
            totales['saldo_final'] = total_monto
            totales['recargos'] = 0.0  # Campo no existe en el nuevo esquema
            totales['intereses'] = 0.0  # Campo no existe en el nuevo esquema
            totales['mora_total'] = 0.0
            totales['saldo_anterior'] = 0.0  # Campo no existe en el nuevo esquema
        except Exception as e:
            error_mensaje = f'❌ Error al consultar transacciones: {str(e)}'
    
    # Si hay error, agregar al sistema de mensajes
    if error_mensaje:
        messages.error(request, error_mensaje)

    context = {
        'municipio_codigo': empresa_filtro,  # Usar empresa_filtro para consistencia
        'empresa': empresa_filtro,
        'rtm': rtm,
        'expe': expe,
        'negocio': negocio,
        'transacciones': transacciones,
        'totales': totales,
        'error_mensaje': error_mensaje,
        'modulo': 'Tributario',
        'descripcion': 'Estado de Cuenta'
    }

    return render(request, 'estado_cuenta.html', context)


@csrf_exempt
def buscar_negocios_listado(request):
    """Vista AJAX para buscar negocios con múltiples criterios para el modal de búsqueda"""
    try:
        from django.db.models import Q
        # Usar el mismo import que estado_cuenta para consistencia
        from tributario.models import Negocio
        
        # Obtener empresa desde sesión
        municipio_codigo = request.session.get('municipio_codigo', '0301')
        empresa_filtro = request.GET.get('empresa', municipio_codigo)
        
        # Obtener criterios de búsqueda
        criterio_busqueda = request.GET.get('criterio', '').strip()
        tipo_busqueda = request.GET.get('tipo', 'todo').strip()
        
        # Inicializar queryset filtrando por empresa
        negocios = Negocio.objects.filter(empresa=empresa_filtro)
        
        # Aplicar filtros según el tipo de búsqueda
        if criterio_busqueda:
            if tipo_busqueda == 'todo':
                # Búsqueda en todos los campos
                negocios = negocios.filter(
                    Q(identidad__icontains=criterio_busqueda) |
                    Q(comerciante__icontains=criterio_busqueda) |
                    Q(nombrenego__icontains=criterio_busqueda) |
                    Q(direccion__icontains=criterio_busqueda) |
                    Q(rtm__icontains=criterio_busqueda) |
                    Q(expe__icontains=criterio_busqueda)
                )
            elif tipo_busqueda == 'dni':
                # Búsqueda por DNI (identidad)
                negocios = negocios.filter(identidad__icontains=criterio_busqueda)
            elif tipo_busqueda == 'comerciante':
                # Búsqueda por nombre del comerciante
                negocios = negocios.filter(comerciante__icontains=criterio_busqueda)
            elif tipo_busqueda == 'nombre':
                # Búsqueda por nombre del negocio
                negocios = negocios.filter(nombrenego__icontains=criterio_busqueda)
            elif tipo_busqueda == 'direccion':
                # Búsqueda por dirección
                negocios = negocios.filter(direccion__icontains=criterio_busqueda)
            elif tipo_busqueda == 'rtm':
                # Búsqueda por RTM
                negocios = negocios.filter(rtm__icontains=criterio_busqueda)
            elif tipo_busqueda == 'expe':
                # Búsqueda por Expediente
                negocios = negocios.filter(expe__icontains=criterio_busqueda)
        
        # Limitar resultados a 100 para evitar sobrecarga
        negocios = negocios.order_by('nombrenego', 'comerciante')[:100]
        
        # Convertir a lista de diccionarios
        resultados = []
        for negocio in negocios:
            resultados.append({
                'empresa': negocio.empresa,
                'rtm': negocio.rtm,
                'expe': negocio.expe,
                'nombrenego': negocio.nombrenego or '',
                'comerciante': negocio.comerciante or '',
                'identidad': negocio.identidad or '',
                'direccion': negocio.direccion or '',
            })
        
        return JsonResponse({
            'exito': True,
            'resultados': resultados,
            'total': len(resultados)
        })
        
    except ImportError as e:
        print(f"❌ Error de importación en buscar_negocios_listado: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al importar modelo: {str(e)}',
            'resultados': []
        }, status=500)
    except Exception as e:
        print(f"❌ Error en buscar_negocios_listado: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error en el servidor: {str(e)}',
            'resultados': []
        }, status=500)


@csrf_exempt
def calcular_transaccion_pago(request):
    """Vista AJAX para calcular transacción de pago desde lo más antiguo hasta lo más reciente"""
    from django.http import JsonResponse
    from tributario.models import TransaccionesIcs, Rubro, Negocio
    from decimal import Decimal
    from datetime import datetime
    
    try:
        empresa = request.GET.get('empresa', '').strip()
        rtm = request.GET.get('rtm', '').strip()
        expe = request.GET.get('expe', '').strip()
        tipo = request.GET.get('tipo', 'cuota').strip()
        
        if not empresa or not rtm or not expe:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Empresa, RTM y Expediente son obligatorios'
            }, status=400)
        
        # Obtener todas las transacciones pendientes (operación 'D' = Débito/Cargo)
        # Ordenadas por fecha (más antiguo primero)
        transacciones_pendientes = TransaccionesIcs.objects.filter(
            empresa=empresa,
            rtm=rtm,
            expe=expe,
            operacion='D'  # Solo cargos (débitos)
        ).order_by('fecha', 'ano', 'mes', 'rubro')
        
        if not transacciones_pendientes.exists():
            return JsonResponse({
                'exito': False,
                'mensaje': 'No hay transacciones pendientes para este negocio'
            })
        
        # Convertir a lista para trabajar con ella
        transacciones_lista = list(transacciones_pendientes)
        
        # Determinar qué transacciones incluir
        transacciones_a_pagar = []
        
        if tipo == 'cuota':
            cuota_hasta = int(request.GET.get('cuota_hasta', 1))
            if cuota_hasta < 1:
                cuota_hasta = 1

            transacciones_a_pagar = []
            periodos_seleccionados = []

            for trans in transacciones_lista:
                ano_trans = None
                mes_trans = None

                if getattr(trans, 'ano', None):
                    try:
                        ano_trans = int(float(trans.ano))
                    except (TypeError, ValueError):
                        ano_trans = None

                if getattr(trans, 'mes', None):
                    try:
                        mes_trans = int(str(trans.mes))
                    except (TypeError, ValueError):
                        mes_trans = None

                periodo_valido = ano_trans is not None and mes_trans is not None

                if periodo_valido:
                    periodo = (ano_trans, mes_trans)

                    if periodo not in periodos_seleccionados:
                        if len(periodos_seleccionados) >= cuota_hasta:
                            break
                        periodos_seleccionados.append(periodo)

                    transacciones_a_pagar.append(trans)
                else:
                    # Si la transacción no tiene periodo definido, la incluimos mientras
                    # no se haya alcanzado el número máximo de periodos válidos.
                    if len(periodos_seleccionados) < cuota_hasta or not periodos_seleccionados:
                        transacciones_a_pagar.append(trans)
                    else:
                        break
        else:  # parcial
            monto_abono = Decimal(str(request.GET.get('monto', '0')))
            monto_restante = monto_abono
            
            for trans in transacciones_lista:
                if monto_restante <= 0:
                    break
                
                # Calcular el saldo pendiente de esta transacción (monto positivo = cargo pendiente)
                saldo_pendiente = Decimal(str(trans.monto)) if trans.monto and trans.monto > 0 else Decimal('0')
                
                if saldo_pendiente > 0:
                    # Determinar cuánto se puede pagar de esta transacción
                    monto_a_aplicar = min(monto_restante, saldo_pendiente)
                    transacciones_a_pagar.append({
                        'transaccion': trans,
                        'monto_a_aplicar': monto_a_aplicar
                    })
                    monto_restante -= monto_a_aplicar
        
        # Agrupar por rubro (independiente de la cuenta)
        agrupado_por_rubro = {}
        periodos_globales = set()

        for item in transacciones_a_pagar:
            if tipo == 'cuota':
                trans = item
                monto = Decimal(str(trans.monto)) if trans.monto and trans.monto > 0 else Decimal('0')
            else:
                trans = item['transaccion']
                monto = item['monto_a_aplicar']

            rubro = (trans.rubro or '').strip() or 'SIN_RUBRO'
            cuenta_trans = (getattr(trans, 'cuenta', '') or '').strip()

            if rubro not in agrupado_por_rubro:
                descripcion = '-'
                cuenta_representativa = cuenta_trans

                try:
                    rubro_obj = Rubro.objects.filter(empresa=empresa, codigo=rubro).first()
                    if rubro_obj:
                        if rubro_obj.descripcion:
                            descripcion = rubro_obj.descripcion
                        if not cuenta_representativa and rubro_obj.cuenta:
                            cuenta_representativa = rubro_obj.cuenta.strip()
                except Exception:
                    descripcion = '-'

                agrupado_por_rubro[rubro] = {
                    'rubro': rubro,
                    'cuenta': cuenta_representativa,
                    'descripcion': descripcion,
                    'valor': Decimal('0'),
                    'periodos': set(),
                }

            if not agrupado_por_rubro[rubro]['cuenta'] and cuenta_trans:
                agrupado_por_rubro[rubro]['cuenta'] = cuenta_trans

            agrupado_por_rubro[rubro]['valor'] += monto

            ano_trans = None
            mes_trans = None
            if getattr(trans, 'ano', None):
                try:
                    ano_trans = int(float(trans.ano))
                except (TypeError, ValueError):
                    ano_trans = None
            if getattr(trans, 'mes', None):
                try:
                    mes_trans = int(str(trans.mes))
                except (TypeError, ValueError):
                    mes_trans = None

            if ano_trans and mes_trans:
                periodo_tuple = (ano_trans, mes_trans)
                periodos_globales.add(periodo_tuple)
                agrupado_por_rubro[rubro]['periodos'].add(periodo_tuple)

        # Construir lista final ordenada por rubro
        transacciones_rubro_list = []
        total_valor = Decimal('0')

        for rubro, datos in agrupado_por_rubro.items():
            valor_decimal = datos['valor']
            total_valor += valor_decimal

            transacciones_rubro_list.append({
                'rubro': rubro,
                'cuenta': datos['cuenta'],
                'descripcion': datos['descripcion'],
                'valor': float(valor_decimal),
                'periodos': [
                    {'ano': p[0], 'mes': p[1]}
                    for p in sorted(datos['periodos'])
                ],
            })

        transacciones_rubro_list.sort(key=lambda item: item['rubro'])

        # Preparar listado detallado para depuración
        transacciones_detalle = []
        for item in transacciones_a_pagar:
            if tipo == 'cuota':
                trans = item
                monto = float(Decimal(str(trans.monto)) if trans.monto else Decimal('0'))
            else:
                trans = item['transaccion']
                monto = float(item['monto_a_aplicar'])

            rubro_detalle = (getattr(trans, 'rubro', '') or '').strip()
            cuenta_detalle = (getattr(trans, 'cuenta', '') or '').strip()
            descripcion_detalle = '-'

            rubro_lookup = rubro_detalle or 'SIN_RUBRO'
            if rubro_lookup in agrupado_por_rubro:
                descripcion_detalle = agrupado_por_rubro[rubro_lookup]['descripcion']

            transacciones_detalle.append({
                'rubro': rubro_detalle,
                'cuenta': cuenta_detalle,
                'descripcion': descripcion_detalle,
                'ano': getattr(trans, 'ano', ''),
                'mes': getattr(trans, 'mes', ''),
                'monto': monto,
            })

        # Logs temporales para diagnóstico
        # Obtener datos del negocio para mostrarlos en el recibo
        negocio = Negocio.objects.filter(empresa=empresa, rtm=rtm, expe=expe).first()
        datos_negocio = {}
        if negocio:
            datos_negocio = {
                'rtm': negocio.rtm or '',
                'expe': negocio.expe or '',
                'nombre_negocio': negocio.nombrenego or '',
                'comerciante': negocio.comerciante or '',
                'direccion': negocio.direccion or ''
            }
        
        periodos_info = [
            {'ano': ano, 'mes': mes}
            for ano, mes in sorted(periodos_globales)
        ]
        
        return JsonResponse({
            'exito': True,
            'transacciones_por_rubro': transacciones_rubro_list,
            'transacciones_detalle': transacciones_detalle,
            'total_transacciones': len(transacciones_a_pagar),
            'total_rubros': len(transacciones_rubro_list),
            'total_periodos': len(periodos_globales),
            'total_valor': float(total_valor),
            'periodos_info': periodos_info,
            'datos_negocio': datos_negocio
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al calcular transacción: {str(e)}'
        }, status=500)


@csrf_exempt
def guardar_transaccion_pago(request):
    """Vista AJAX para guardar transacción de pago que puede ser cobrada en módulo de caja"""
    from django.http import JsonResponse
    from tributario.models import TransaccionesIcs, Rubro
    from decimal import Decimal
    from django.utils import timezone
    import json
    
    try:
        if request.method != 'POST':
            return JsonResponse({
                'exito': False,
                'mensaje': 'Método no permitido'
            }, status=405)
        
        data = json.loads(request.body)
        empresa = data.get('empresa', '').strip()
        rtm = data.get('rtm', '').strip()
        expe = data.get('expe', '').strip()
        tipo = data.get('tipo', 'cuota').strip()
        
        if not empresa or not rtm or not expe:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Empresa, RTM y Expediente son obligatorios'
            }, status=400)
        
        # Obtener usuario de la sesión
        usuario = request.session.get('usuario', 'SISTEMA')
        
        # Obtener negocio
        from tributario.models import Negocio
        negocio = Negocio.objects.filter(empresa=empresa, rtm=rtm, expe=expe).first()
        if not negocio:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Negocio no encontrado'
            }, status=404)
        
        # Obtener transacciones pendientes ordenadas por fecha
        transacciones_pendientes = TransaccionesIcs.objects.filter(
            empresa=empresa,
            rtm=rtm,
            expe=expe,
            operacion='D'
        ).order_by('fecha', 'ano', 'mes', 'rubro')
        
        transacciones_lista = list(transacciones_pendientes)
        
        # Determinar qué transacciones pagar
        transacciones_a_pagar = []
        
        if tipo == 'cuota':
            cuota_hasta = int(data.get('cuota_hasta', 1))
            transacciones_a_pagar = transacciones_lista[:cuota_hasta]
        else:
            monto_abono = Decimal(str(data.get('monto', '0')))
            monto_restante = monto_abono
            
            for trans in transacciones_lista:
                if monto_restante <= 0:
                    break
                saldo_pendiente = Decimal(str(trans.monto)) if trans.monto and trans.monto > 0 else Decimal('0')
                if saldo_pendiente > 0:
                    monto_a_aplicar = min(monto_restante, saldo_pendiente)
                    transacciones_a_pagar.append({
                        'transaccion': trans,
                        'monto_a_aplicar': monto_a_aplicar
                    })
                    monto_restante -= monto_a_aplicar
        
        # Agrupar transacciones por rubro para calcular rangos de meses
        pagos_por_rubro = {}
        
        for item in transacciones_a_pagar:
            if tipo == 'cuota':
                trans_original = item
                monto_pago = Decimal(str(trans_original.monto)) if trans_original.monto and trans_original.monto > 0 else Decimal('0')
            else:
                trans_original = item['transaccion']
                monto_pago = item['monto_a_aplicar']
            
            rubro = trans_original.rubro or ''
            ano_trans = int(float(trans_original.ano)) if trans_original.ano else 0
            mes_trans = int(trans_original.mes) if trans_original.mes and trans_original.mes.isdigit() else 0
            
            if rubro not in pagos_por_rubro:
                pagos_por_rubro[rubro] = {
                    'montos': [],
                    'anos': [],
                    'meses': [],
                    'transacciones': []
                }
            
            pagos_por_rubro[rubro]['montos'].append(monto_pago)
            pagos_por_rubro[rubro]['anos'].append(ano_trans)
            pagos_por_rubro[rubro]['meses'].append(mes_trans)
            pagos_por_rubro[rubro]['transacciones'].append(trans_original)
        
        # Crear transacciones de pago agrupadas por rubro
        transacciones_creadas = []
        rangos_info = []
        
        for rubro, datos in pagos_por_rubro.items():
            # Calcular rango de meses (desde el más antiguo hasta el más reciente)
            anos_meses = list(zip(datos['anos'], datos['meses']))
            anos_meses_ordenados = sorted(anos_meses, key=lambda x: (x[0], x[1]))
            
            if anos_meses_ordenados:
                # Primer periodo (más antiguo)
                ano_desde, mes_desde = anos_meses_ordenados[0]
                # Último periodo (más reciente)
                ano_hasta, mes_hasta = anos_meses_ordenados[-1]
                
                # Calcular monto total del pago para este rubro
                monto_total_rubro = sum(datos['montos'])
                
                # Formatear rango de meses para nodeclara: "ANO-MES|ANO-MES"
                # Ejemplo: "2024-01|2024-03" significa desde enero 2024 hasta marzo 2024
                mes_desde_str = str(mes_desde).zfill(2)
                mes_hasta_str = str(mes_hasta).zfill(2)
                rango_meses = f"{ano_desde}-{mes_desde_str}|{ano_hasta}-{mes_hasta_str}"
                
                # Usar el año y mes del periodo más reciente para la transacción de pago
                ano_pago = ano_hasta
                mes_pago = mes_hasta_str
                
                # Crear transacción de pago (monto negativo)
                transaccion_pago = TransaccionesIcs(
                    idneg=negocio.id if negocio else 0,
                    empresa=empresa,
                    rtm=rtm,
                    expe=expe,
                    ano=ano_pago,
                    mes=mes_pago,
                    operacion='F',  # Pago
                    rubro=rubro,
                    fecha=timezone.now().date(),
                    monto=-monto_total_rubro,  # Negativo porque es un pago
                    tasa=Decimal('0'),
                    nodeclara=rango_meses[:20] if len(rango_meses) <= 20 else rango_meses[:20],  # Guardar rango en nodeclara
                    usuario=usuario,
                    fechasys=timezone.now()
                )
                transaccion_pago.save()
                # Forzar tasa a 0 después de guardar (protección para recargos moratorios)
                TransaccionesIcs.objects.filter(id=transaccion_pago.id).update(tasa=Decimal('0.00'))
                transacciones_creadas.append(transaccion_pago.id)
                
                # Guardar información del rango para la respuesta
                rangos_info.append({
                    'rubro': rubro,
                    'ano_desde': ano_desde,
                    'mes_desde': mes_desde,
                    'ano_hasta': ano_hasta,
                    'mes_hasta': mes_hasta,
                    'monto': float(monto_total_rubro),
                    'rango_str': rango_meses
                })
        
        # Construir mensaje con información de rangos
        mensaje = f'Transacción de pago guardada exitosamente. {len(transacciones_creadas)} registro(s) creado(s).'
        if rangos_info:
            mensaje += '\n\nRangos cubiertos:'
            for rango in rangos_info:
                mensaje += f'\n- Rubro {rango["rubro"]}: {rango["mes_desde"]:02d}/{rango["ano_desde"]} hasta {rango["mes_hasta"]:02d}/{rango["ano_hasta"]}'
        
        return JsonResponse({
            'exito': True,
            'mensaje': mensaje,
            'transaccion_id': transacciones_creadas[0] if transacciones_creadas else None,
            'total_transacciones': len(transacciones_creadas),
            'rangos': rangos_info
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al guardar transacción: {str(e)}'
        }, status=500)
