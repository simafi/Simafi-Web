def estado_cuenta(request):
    """Estado de Cuenta por negocio con filtros por rango de periodo y mora acumulativa"""
    from django.db.models import Sum
    from django.contrib import messages
    from tributario.models import Negocio, TransaccionesIcs

    # Obtener empresa: priorizar GET sobre sesión, pero validar que coincidan
    empresa_get = request.GET.get('empresa', '').strip()
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    # Usar empresa de GET si viene, sino usar la de sesión
    empresa_filtro = empresa_get if empresa_get else municipio_codigo
    
    # Validación de seguridad: si viene empresa por GET, debe coincidir con sesión
    if empresa_get and empresa_get != municipio_codigo:
        messages.error(request, f'⚠️ Error de seguridad: La empresa especificada ({empresa_get}) no coincide con su sesión ({municipio_codigo}).')
        empresa_filtro = municipio_codigo  # Forzar uso de sesión por seguridad

    rtm = request.GET.get('rtm', '').strip()
    expe = request.GET.get('expe', '').strip()

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
    totales = {'recargos': 0.0, 'intereses': 0.0, 'mora_total': 0.0, 'saldo_final': 0.0}
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
            # Mostrar solo cuotas pendientes: ocultar transacciones ya saldadas (monto <= 0)
            # Control tributario determina pendiente por `monto__gt=0`.
            qs = qs.filter(monto__gt=0)

            if ano_desde:
                qs = qs.filter(ano__gte=ano_desde)
            if ano_hasta:
                qs = qs.filter(ano__lte=ano_hasta)
            if mes_desde:
                qs = qs.filter(mes__gte=mes_desde)
            if mes_hasta:
                qs = qs.filter(mes__lte=mes_hasta)

            qs = qs.order_by('ano', 'mes', 'fecha', 'id')

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

            acumulados = qs.aggregate(
                total_monto=Sum('monto')  # Suma de todos los montos (cargos positivos, pagos negativos)
            )
            total_monto = float(acumulados.get('total_monto') or 0)
            totales['saldo_final'] = total_monto
            totales['recargos'] = 0.0  # Campo no existe en el nuevo esquema
            totales['intereses'] = 0.0  # Campo no existe en el nuevo esquema
            totales['mora_total'] = 0.0
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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .buscar_identificacion import buscar_identificacion


def historial_pagos(request):
    """
    Historial de pagos (cobrados en Caja) para un negocio.
    Se filtra por `teso_cobro_caja.observacion` (guardada al cobrar) para RTM/EXPE.
    """
    from tesoreria.models import CobroCaja
    from django.db import connection

    if request.session.get("user_id") is None:
        return redirect("modules_core:login_principal")

    empresa_get = (request.GET.get("empresa") or "").strip()
    municipio_codigo = (
        request.session.get("municipio_codigo")
        or request.session.get("empresa")
        or "0301"
    )
    municipio_codigo = str(municipio_codigo).strip() or "0301"
    empresa = empresa_get or municipio_codigo

    if empresa_get and empresa_get != municipio_codigo:
        messages.error(
            request,
            f"⚠️ Error de seguridad: La empresa especificada ({empresa_get}) no coincide con su sesión ({municipio_codigo}).",
        )
        empresa = municipio_codigo

    rtm = (request.GET.get("rtm") or "").strip()
    expe = (request.GET.get("expe") or "").strip()

    def _parse_obs(texto: str) -> dict:
        data = {"descripcion": "", "comentario": "", "metodo_pago": "", "rtm": "", "expe": "", "cocata1": "", "tipo": ""}
        raw = (texto or "").strip()
        if not raw:
            return data
        for chunk in raw.split("|"):
            for part in chunk.split(";"):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                k = k.strip()
                v = v.strip()
                if k in data:
                    data[k] = v
        return data

    pagos = []
    if empresa and rtm and expe:
        cobros = []
        # Preferir vínculo estructurado si existe
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT to_regclass('public.teso_cobro_caja_vinculo')")
                if cursor.fetchone()[0]:
                    cursor.execute(
                        """
                        SELECT c.id, c.fecha, c.total_cobrado, c.referencia, c.cajero, c.observacion
                        FROM teso_cobro_caja c
                        JOIN teso_cobro_caja_vinculo v ON v.cobro_id = c.id
                        WHERE c.empresa = %s AND c.fuente = 'CAJA' AND c.is_active = true
                          AND v.tipo = 'N' AND v.rtm = %s AND v.expe = %s
                        ORDER BY c.fecha DESC, c.id DESC
                        LIMIT 200
                        """,
                        [empresa, rtm, expe],
                    )
                    rows = cursor.fetchall()
                    # map a objetos mínimos compatibles con el resto del código
                    class _CobroMini:
                        __slots__ = ("id", "fecha", "total_cobrado", "referencia", "cajero", "observacion", "metodos")
                    for (cid, fecha, total_cobrado, referencia, cajero, observacion) in rows:
                        o = _CobroMini()
                        o.id = cid
                        o.fecha = fecha
                        o.total_cobrado = total_cobrado
                        o.referencia = referencia
                        o.cajero = cajero
                        o.observacion = observacion
                        o.metodos = None
                        cobros.append(o)
        except Exception:
            cobros = []

        # Fallback legacy: búsqueda por observación
        if not cobros:
            patron = f"tipo=N;rtm={rtm};expe={expe}"
            cobros = list(
                CobroCaja.objects.filter(
                    empresa=empresa,
                    fuente="CAJA",
                    observacion__icontains=patron,
                )
                .order_by("-fecha", "-id")[:200]
            )

        # Traer observaciones del resumen (pagos_factura) si existe
        refs = [str(c.referencia or "").strip() for c in cobros if c.referencia]
        obs_pf = {}
        if refs:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT to_regclass('public.pagos_factura')")
                    if cursor.fetchone()[0]:
                        placeholders = ", ".join(["%s"] * len(refs))
                        cursor.execute(
                            f"SELECT numero_recibo, observaciones FROM pagos_factura WHERE numero_recibo IN ({placeholders})",
                            refs,
                        )
                        for numero_recibo, observaciones in cursor.fetchall():
                            obs_pf[str(numero_recibo)] = observaciones or ""
            except Exception:
                obs_pf = {}

        # Construir filas para template (igual al resumen de caja)
        pagos = []
        for c in cobros:
            metodos = []
            try:
                if getattr(c, "metodos", None) is not None:
                    metodos = sorted({(m.forma_pago or "").upper() for m in c.metodos.all() if m.forma_pago})
            except Exception:
                metodos = []
            metodo_txt = " + ".join(metodos) if metodos else "EFECTIVO"

            parsed_pf = _parse_obs(obs_pf.get(str(c.referencia or ""), ""))
            parsed_cobro = _parse_obs(c.observacion or "")
            merged = {**parsed_pf, **{k: v for k, v in parsed_cobro.items() if v}}

            pagos.append(
                {
                    "fecha": c.fecha,
                    "referencia": c.referencia or "",
                    "cajero": c.cajero or "",
                    "total": c.total_cobrado,
                    "metodo_pago": merged.get("metodo_pago") or metodo_txt,
                    "descripcion": merged.get("descripcion") or "",
                    "comentario": merged.get("comentario") or "",
                }
            )
    else:
        messages.error(request, "⚠️ Empresa, RTM y Expediente son obligatorios para ver el historial de pagos.")

    return render(
        request,
        "historial_pagos.html",
        {"empresa": empresa, "rtm": rtm, "expe": expe, "pagos": pagos},
    )


def historial_pagos_bienes(request):
    """
    Historial de pagos (cobrados en Caja) para Bienes Inmuebles.
    Se filtra por Clave Catastral (cocata1) usando tabla vínculo si existe.
    """
    from tesoreria.models import CobroCaja
    from django.db import connection

    if request.session.get("user_id") is None:
        return redirect("modules_core:login_principal")

    empresa_get = (request.GET.get("empresa") or "").strip()
    municipio_codigo = (
        request.session.get("municipio_codigo")
        or request.session.get("empresa")
        or "0301"
    )
    municipio_codigo = str(municipio_codigo).strip() or "0301"
    empresa = empresa_get or municipio_codigo

    if empresa_get and empresa_get != municipio_codigo:
        messages.error(
            request,
            f"⚠️ Error de seguridad: La empresa especificada ({empresa_get}) no coincide con su sesión ({municipio_codigo}).",
        )
        empresa = municipio_codigo

    cocata1 = (request.GET.get("cocata1") or "").strip()

    def _parse_obs(texto: str) -> dict:
        data = {"descripcion": "", "comentario": "", "metodo_pago": "", "rtm": "", "expe": "", "cocata1": "", "tipo": ""}
        raw = (texto or "").strip()
        if not raw:
            return data
        for chunk in raw.split("|"):
            for part in chunk.split(";"):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                k = k.strip()
                v = v.strip()
                if k in data:
                    data[k] = v
        return data

    pagos = []
    if empresa and cocata1:
        cobros = []
        # Preferir vínculo estructurado si existe
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT to_regclass('public.teso_cobro_caja_vinculo')")
                if cursor.fetchone()[0]:
                    cursor.execute(
                        """
                        SELECT c.id, c.fecha, c.total_cobrado, c.referencia, c.cajero, c.observacion
                        FROM teso_cobro_caja c
                        JOIN teso_cobro_caja_vinculo v ON v.cobro_id = c.id
                        WHERE c.empresa = %s AND c.fuente = 'CAJA' AND c.is_active = true
                          AND v.tipo = 'B' AND v.cocata1 = %s
                        ORDER BY c.fecha DESC, c.id DESC
                        LIMIT 200
                        """,
                        [empresa, cocata1],
                    )
                    rows = cursor.fetchall()
                    class _CobroMini:
                        __slots__ = ("id", "fecha", "total_cobrado", "referencia", "cajero", "observacion", "metodos")
                    for (cid, fecha, total_cobrado, referencia, cajero, observacion) in rows:
                        o = _CobroMini()
                        o.id = cid
                        o.fecha = fecha
                        o.total_cobrado = total_cobrado
                        o.referencia = referencia
                        o.cajero = cajero
                        o.observacion = observacion
                        o.metodos = None
                        cobros.append(o)
        except Exception:
            cobros = []

        # Fallback legacy: búsqueda por observación
        if not cobros:
            patron = f"tipo=B;cocata1={cocata1}"
            cobros = list(
                CobroCaja.objects.filter(
                    empresa=empresa,
                    fuente="CAJA",
                    observacion__icontains=patron,
                )
                .order_by("-fecha", "-id")[:200]
            )

        # Traer observaciones del resumen (pagos_factura) si existe
        refs = [str(c.referencia or "").strip() for c in cobros if c.referencia]
        obs_pf = {}
        if refs:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT to_regclass('public.pagos_factura')")
                    if cursor.fetchone()[0]:
                        placeholders = ", ".join(["%s"] * len(refs))
                        cursor.execute(
                            f"SELECT numero_recibo, observaciones FROM pagos_factura WHERE numero_recibo IN ({placeholders})",
                            refs,
                        )
                        for numero_recibo, observaciones in cursor.fetchall():
                            obs_pf[str(numero_recibo)] = observaciones or ""
            except Exception:
                obs_pf = {}

        pagos = []
        for c in cobros:
            metodos = []
            try:
                if getattr(c, "metodos", None) is not None:
                    metodos = sorted({(m.forma_pago or "").upper() for m in c.metodos.all() if m.forma_pago})
            except Exception:
                metodos = []
            metodo_txt = " + ".join(metodos) if metodos else "EFECTIVO"

            parsed_pf = _parse_obs(obs_pf.get(str(c.referencia or ""), ""))
            parsed_cobro = _parse_obs(c.observacion or "")
            merged = {**parsed_pf, **{k: v for k, v in parsed_cobro.items() if v}}

            pagos.append(
                {
                    "fecha": c.fecha,
                    "referencia": c.referencia or "",
                    "cajero": c.cajero or "",
                    "total": c.total_cobrado,
                    "metodo_pago": merged.get("metodo_pago") or metodo_txt,
                    "descripcion": merged.get("descripcion") or "",
                    "comentario": merged.get("comentario") or "",
                }
            )
    else:
        messages.error(request, "⚠️ Empresa y Clave Catastral son obligatorios para ver el historial de pagos de Bienes.")

    return render(
        request,
        "historial_pagos_bienes.html",
        {"empresa": empresa, "cocata1": cocata1, "pagos": pagos},
    )

def tributario_login(request):
    """Vista de login del módulo tributario"""
    # Redirigir directamente al menú general del tributario
    return redirect('tributario:tributario_menu_principal')

def tributario_logout(request):
    """Vista de logout del módulo tributario"""
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('modules_core:menu_principal')

def tributario_menu_principal(request):
    """Menú principal del módulo tributario con diseño dashboard"""
    from .models import ParametrosTributarios
    
    # Obtener municipio/empresa de la sesión
    empresa = request.session.get('municipio_codigo') or request.session.get('empresa', '0301')
    usuario = request.session.get('usuario') or request.user.username if request.user.is_authenticated else 'Invitado'
    
    # Verificar amnistía activa para mostrar el banner
    amnistia = ParametrosTributarios.amnistia_activa(empresa)
    
    context = {
        'modulo': 'Tributario',
        'descripcion': 'Gestión integral de impuestos y tasas municipales',
        'empresa': empresa,
        'usuario': usuario,
        'amnistia_activa': amnistia,
    }
    
    try:
        return render(request, 'menugeneral.html', context)
    except Exception as e:
        print(f"Error en tributario_menu_principal: {e}")
        return render(request, 'menugeneral.html', context)

# Vistas para las funcionalidades del menugeneral.html
@csrf_exempt
def maestro_negocios(request):
    """Vista para maestro de negocios"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Manejar solicitudes POST para acciones AJAX
    if request.method == 'POST':
        import logging
        import sys
        logger = logging.getLogger(__name__)
        
        logger.error("=" * 80)
        logger.error("🔵 EJECUTANDO: venv/Scripts/tributario/views.py -> maestro_negocios")
        logger.error("=" * 80)
        print("=" * 80, file=sys.stderr)
        print("🔵 EJECUTANDO: venv/Scripts/tributario/views.py -> maestro_negocios", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        
        # SOLUCIÓN: SIEMPRE procesar form-urlencoded primero
        data = None
        
        # Paso 1: Intentar usar request.POST (Django ya lo parseó)
        if request.POST and len(request.POST) > 0:
            data = request.POST
            logger.error(f"✅ Usando request.POST. Acción: {data.get('accion', 'No encontrada')}")
            print(f"✅ Usando request.POST. Acción: {data.get('accion', 'No encontrada')}", file=sys.stderr)
        # Paso 2: Si no hay POST, intentar parsear como JSON
        elif request.body:
            try:
                data = json.loads(request.body)
                logger.error(f"✅ Body parseado como JSON. Acción: {data.get('accion', 'No encontrada')}")
                print(f"✅ Body parseado como JSON. Acción: {data.get('accion', 'No encontrada')}", file=sys.stderr)
            except json.JSONDecodeError:
                # Paso 3: Si no es JSON, parsear como form-urlencoded manualmente
                try:
                    from urllib.parse import parse_qs, unquote_plus
                    from django.http import QueryDict
                    
                    body_str = request.body.decode('utf-8')
                    logger.error(f"📥 Body decodificado (primeros 500 chars): {body_str[:500]}")
                    print(f"📥 Body decodificado (primeros 500 chars): {body_str[:500]}", file=sys.stderr)
                    
                    parsed_data = parse_qs(body_str, keep_blank_values=True)
                    
                    data = QueryDict('', mutable=True)
                    for key, value_list in parsed_data.items():
                        decoded_values = [unquote_plus(v) for v in value_list]
                        if len(decoded_values) == 1:
                            data[key] = decoded_values[0]
                        else:
                            data.setlist(key, decoded_values)
                    
                    logger.error(f"✅ Body parseado manualmente. Acción: {data.get('accion', 'No encontrada')}")
                    print(f"✅ Body parseado manualmente. Acción: {data.get('accion', 'No encontrada')}", file=sys.stderr)
                except Exception as e:
                    logger.error(f"❌ Error al parsear body: {str(e)}")
                    import traceback
                    traceback_str = traceback.format_exc()
                    logger.error(f"❌ Traceback: {traceback_str}")
                    print(f"❌ Error al parsear body: {str(e)}", file=sys.stderr)
                    print(f"❌ Traceback completo:\n{traceback_str}", file=sys.stderr)
                    return JsonResponse({
                        'exito': False,
                        'mensaje': f'Error al parsear datos del formulario: {str(e)}. Tipo: {type(e).__name__}'
                    })
        
        # Si no hay datos, devolver error
        if not data:
            logger.error("❌ No se recibieron datos")
            print("❌ No se recibieron datos", file=sys.stderr)
            return JsonResponse({
                'exito': False,
                'mensaje': 'No se recibieron datos en la solicitud'
            })
        
        # Procesar acciones
        try:
            accion = data.get('accion')
            
            if accion == 'salvar':
                logger.error("🚀 Llamando a handle_salvar_negocio")
                print("🚀 Llamando a handle_salvar_negocio", file=sys.stderr)
                return handle_salvar_negocio(request, data)
            elif accion == 'nuevo':
                # El botón "Nuevo" limpia el formulario en el frontend.
                # En backend solo devolvemos OK para evitar "Acción no válida".
                return JsonResponse({
                    'exito': True,
                    'mensaje': 'OK',
                })
            elif accion == 'eliminar':
                return handle_eliminar_negocio(request, data)
            elif accion == 'configuracion':
                rtm = data.get('rtm', '')
                expe = data.get('expe', '')
                if rtm and expe:
                    target = f'/tributario/configurar-tasas-negocio/?rtm={rtm}&expe={expe}'
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'exito': True, 'redirect': target})
                    return redirect(target)
                else:
                    return JsonResponse({
                        'exito': False,
                        'mensaje': 'RTM y Expediente son requeridos para configurar tasas'
                    })
            elif accion == 'declaracion':
                rtm = data.get('rtm', '')
                expe = data.get('expe', '')
                if rtm and expe:
                    target = f'/tributario/declaraciones/?rtm={rtm}&expe={expe}'
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'exito': True, 'redirect': target})
                    return redirect(target)
                else:
                    return JsonResponse({
                        'exito': False,
                        'mensaje': 'RTM y Expediente son requeridos para declaración de volumen'
                    })
            elif accion == 'estado':
                rtm = data.get('rtm', '')
                expe = data.get('expe', '')
                empre = data.get('empresa', '') or request.session.get('municipio_codigo') or request.session.get('empresa') or ''
                if rtm and expe:
                    target = f'/tributario/estado-cuenta/?empresa={empre}&rtm={rtm}&expe={expe}'
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'exito': True, 'redirect': target})
                    return redirect(target)
                return JsonResponse({'exito': False, 'mensaje': 'RTM y Expediente son obligatorios para estado de cuenta'})
            elif accion == 'historial':
                rtm = data.get('rtm', '')
                expe = data.get('expe', '')
                empre = data.get('empresa', '') or request.session.get('municipio_codigo') or request.session.get('empresa') or ''
                if rtm and expe:
                    target = f'/tributario/historial-pagos/?empresa={empre}&rtm={rtm}&expe={expe}'
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'exito': True, 'redirect': target})
                    return redirect(target)
                return JsonResponse({'exito': False, 'mensaje': 'RTM y Expediente son obligatorios para historial'})
            elif accion == 'verificar_permiso':
                from .services_permisos import verificar_requisitos_permiso
                from .models import Negocio
                rtm = data.get('rtm', '')
                expe = data.get('expe', '')
                empre = data.get('empresa', '') or request.session.get('municipio_codigo') or request.session.get('empresa', '0301')
                ano = int(data.get('ano') or datetime.now().year)
                
                negocio = Negocio.objects.filter(empresa=empre, rtm=rtm, expe=expe).first()
                if not negocio:
                    return JsonResponse({'exito': False, 'mensaje': 'Negocio no encontrado'})
                
                res = verificar_requisitos_permiso(negocio, ano)
                return JsonResponse(res)
            elif accion == 'guardar_requisitos':
                from .models import Negocio, PermisoOperacionRequisito
                from .services_permisos import verificar_requisitos_permiso
                rtm = data.get('rtm', '')
                expe = data.get('expe', '')
                empre = data.get('empresa', '') or request.session.get('municipio_codigo') or request.session.get('empresa', '0301')
                ano = int(data.get('ano') or datetime.now().year)
                
                negocio = Negocio.objects.filter(empresa=empre, rtm=rtm, expe=expe).first()
                if not negocio:
                    return JsonResponse({'exito': False, 'mensaje': 'Negocio no encontrado'})
                
                requisitos, created = PermisoOperacionRequisito.objects.get_or_create(
                    negocio=negocio,
                    ano=ano
                )
                requisitos.bomberos = data.get('bomberos') == 'true' or data.get('bomberos') is True
                requisitos.salud = data.get('salud') == 'true' or data.get('salud') is True
                requisitos.ambiente = data.get('ambiente') == 'true' or data.get('ambiente') is True
                requisitos.usuario = request.session.get('usuario', 'admin')
                requisitos.save()
                
                res = verificar_requisitos_permiso(negocio, ano)
                return JsonResponse(res)
            else:
                logger.error(f"⚠️ Acción no válida: {accion}")
                print(f"⚠️ Acción no válida: {accion}", file=sys.stderr)
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'Acción no válida: {accion}'
                })
        except Exception as e:
            logger.error(f"❌ Error al procesar acción '{accion}': {str(e)}")
            import traceback
            traceback_str = traceback.format_exc()
            logger.error(f"❌ Traceback: {traceback_str}")
            print(f"❌ Error al procesar acción '{accion}': {str(e)}", file=sys.stderr)
            print(f"❌ Traceback completo:\n{traceback_str}", file=sys.stderr)
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error al procesar la solicitud ({type(e).__name__}): {str(e)}'
            })
    
    # Manejar solicitudes GET para mostrar el formulario
    # Verificar si se está regresando desde otro formulario con parámetros
    rtm_regreso = request.GET.get('rtm', '').strip()
    expe_regreso = request.GET.get('expe', '').strip()
    empresa_regreso = request.GET.get('empresa', '').strip() or empresa
    
    # Crear un objeto negocio vacío para el formulario
    negocio = {
        'empresa': empresa,
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
        'comentario': '',
        'fecha_nacimiento': ''
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
                'comentario': negocio_existente.comentario or '',
                'fecha_nacimiento': negocio_existente.fecha_nacimiento.strftime('%Y-%m-%d') if negocio_existente.fecha_nacimiento else ''
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
    
    return render(request, 'maestro_negocios.html', {
        'negocio': negocio,
        'actividades': actividades_list,
        'empresa': empresa,
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
        empresa = negocio_data.get('empresa') or negocio_data.get('empre', '0301')
        
        if rtm and expe:
            negocio, created = Negocio.objects.get_or_create(
                empresa=empresa,
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
                    'comentario': truncar_campo(negocio_data.get('comentario', ''), 500),
                    'fecha_nacimiento': negocio_data.get('fecha_nacimiento') if negocio_data.get('fecha_nacimiento') else None
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
                negocio.fecha_nacimiento = negocio_data.get('fecha_nacimiento') if negocio_data.get('fecha_nacimiento') else None
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
        empresa = negocio_data.get('empresa') or negocio_data.get('empre', '0301')
        
        if rtm and expe:
            try:
                negocio = Negocio.objects.get(
                    empresa=empresa,
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
            # Compatibilidad: el frontend usa `empresa`, pero algunos flujos legacy usan `empre`.
            empresa = request.GET.get('empresa') or request.GET.get('empre') or '0301'
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
                empresa = request.POST.get('empresa') or request.POST.get('empre') or '0301'
        else:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Método no permitido'
            })
        
        print(f"[DEBUG] Buscando negocio: empre={empresa}, rtm={rtm}, expe={expe}")
        
        if rtm and expe:
            from tributario.models import Negocio
            try:
                negocio = Negocio.objects.get(
                    empresa=empresa,
                    rtm=rtm,
                    expe=expe
                )
                
                print(f"[OK] Negocio encontrado: {negocio.nombrenego}")

                negocio_data = {
                    'empresa': negocio.empresa,
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
                    'comentario': negocio.comentario,
                    'fecha_nacimiento': negocio.fecha_nacimiento.strftime('%Y-%m-%d') if negocio.fecha_nacimiento else None
                }

                # Compatibilidad con frontend actual: devolver campos también a nivel raíz
                return JsonResponse({
                    'exito': True,
                    **negocio_data,
                    'negocio': negocio_data,
                })
            except Negocio.DoesNotExist:
                print(f"[ERROR] Negocio no encontrado: empresa={empresa}, rtm={rtm}, expe={expe}")
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
            from tributario.models import Negocio
            if negocio_id:
                negocio = Negocio.objects.get(id=negocio_id)
            else:
                negocio = Negocio.objects.get(
                    empresa=empresa,
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
            from .tributario_app.forms import TarifasICSForm
            from tributario.models import TarifasICS, Rubro, Tarifas
            
            accion = request.POST.get('accion')
            
            if accion == 'agregar_tarifa':
                # Agregar nueva tarifa ICS
                form = TarifasICSForm(request.POST, empresa=empresa, negocio=negocio)
                if form.is_valid():
                    # Obtener datos del formulario (misma lógica que otros campos)
                    rubro = form.cleaned_data.get('rubro')
                    tarifa_rubro = form.cleaned_data.get('tarifa_rubro')
                    valor_personalizado = form.cleaned_data.get('valor_personalizado')
                    
                    # Obtener cuenta y cuentarez del formulario Django
                    cuenta = form.cleaned_data.get('cuenta', '')
                    cuentarez = form.cleaned_data.get('cuentarez', '')
                    
                    # Debug para verificar qué datos llegan
                    print("="*80)
                    print("[DEBUG] DATOS RECIBIDOS EN EL BACKEND:")
                    print(f"[DEBUG] Cuenta del formulario: '{cuenta}'")
                    print(f"[DEBUG] Cuentarez del formulario: '{cuentarez}'")
                    print(f"[DEBUG] Cuenta del POST: '{request.POST.get('cuenta', '')}'")
                    print(f"[DEBUG] Cuentarez del POST: '{request.POST.get('cuentarez', '')}'")
                    print("="*80)
                    
                    # Buscar la tarifa seleccionada para obtener su valor por defecto
                    try:
                        from tributario.models import Tarifas
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
                            empresa=empresa,
                            idneg=negocio.id,
                            rtm=negocio.rtm,
                            expe=negocio.expe,
                            rubro=rubro,
                            cod_tarifa=tarifa_rubro,
                            valor=valor_final,
                            cuenta=cuenta or '',
                            cuentarez=cuentarez or ''
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
        from tributario.models import TarifasICS
        tarifas_ics = TarifasICS.objects.filter(idneg=negocio.id).order_by('cod_tarifa')
    except Exception as e:
        tarifas_ics = []
        if not mensaje:
            mensaje = f"Error al cargar tarifas: {str(e)}"
            exito = False
    
    # Crear formulario inicial
    try:
        from .tributario_app.forms import TarifasICSForm
        form = TarifasICSForm(initial={
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe
        }, empresa=empresa, negocio=negocio)
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
        
        from tributario.models import Tarifas
        
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

@csrf_exempt
def obtener_cuenta_rezago(request):
    """Vista AJAX para obtener la cuenta rezago de una cuenta específica"""
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        cuenta_codigo = request.POST.get('cuenta', '').strip()
        empresa = request.session.get('empresa', '0301')
        
        if not cuenta_codigo:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Código de cuenta requerido'
            })
        
        from tributario.models import Actividad
        
        # Buscar la actividad por empresa y código
        actividad = Actividad.objects.filter(
            empresa=empresa,
            codigo=cuenta_codigo
        ).first()
        
        if not actividad:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Actividad no encontrada'
            })
        
        # Obtener la cuenta rezago
        cuentarez = actividad.obtener_cuenta_rezago()
        
        return JsonResponse({
            'exito': True,
            'cuentarez': cuentarez,
            'descripcion': actividad.descripcion or ''
        })
        
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al obtener cuenta rezago: {str(e)}'
        })

@csrf_exempt
def verificar_tarifa_existente(request):
    """Vista AJAX para verificar si existe una tarifa para un rubro específico"""
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        rubro = request.POST.get('rubro', '').strip()
        rtm = request.POST.get('rtm', '').strip()
        expe = request.POST.get('expe', '').strip()
        empresa = request.session.get('empresa', '0301')
        
        if not rubro or not rtm:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Rubro y RTM requeridos'
            })
        
        from tributario.models import TarifasICS
        tarifa_existente = TarifasICS.objects.filter(
            empresa=empresa,
            rtm=rtm,
            expe=expe,
            rubro=rubro
        ).first()
        
        if tarifa_existente:
            return JsonResponse({
                'exito': True,
                'existe': True,
                'tarifa': {
                    'id': tarifa_existente.id,
                    'rubro': tarifa_existente.rubro,
                    'cod_tarifa': tarifa_existente.cod_tarifa,
                    'valor': float(tarifa_existente.valor),
                    'cuenta': tarifa_existente.cuenta or '',
                    'cuentarez': tarifa_existente.cuentarez or ''
                }
            })
        else:
            return JsonResponse({
                'exito': True,
                'existe': False,
                'mensaje': 'No existe tarifa para este rubro'
            })
        
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al verificar tarifa: {str(e)}'
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
    tarifas_ics = []  # Inicializar tarifas_ics
    declaracion_info = None  # Datos informativos de la declaración
    rtm = request.GET.get('rtm', '')
    expe = request.GET.get('expe', '')

    if request.method == 'POST':
        try:
            from tributario.models import DeclaracionVolumen, Negocio
            from .tributario_app.forms import DeclaracionVolumenForm
            accion = request.POST.get('accion')
            
            # Debug: Verificar si es petición AJAX
            print("="*80)
            print("[BACKEND] Peticion POST recibida")
            print(f"[BACKEND] Accion: {accion}")
            print(f"[BACKEND] Es AJAX: {request.headers.get('X-Requested-With') == 'XMLHttpRequest'}")
            print(f"[BACKEND] Content-Type: {request.headers.get('Content-Type')}")
            print("="*80)
            
            if accion == 'nuevo':
                mensaje = 'Formulario preparado para nueva declaración'
                exito = True
            elif accion == 'guardar':
                # Limpiar valores con separadores de miles (comas) antes de validar
                datos_limpiados = request.POST.copy()
                campos_numericos = ['ano', 'ventai', 'ventac', 'ventas', 'valorexcento', 'controlado', 
                                   'unidad', 'factor', 'multadecla', 'impuesto', 'ajuste']
                
                print("="*80)
                print("BACKEND - Limpiando valores con separadores de miles:")
                for campo in campos_numericos:
                    if campo in datos_limpiados and datos_limpiados[campo]:
                        valor_original = datos_limpiados[campo]
                        # Remover comas (separadores de miles) antes de validar
                        valor_limpio = str(datos_limpiados[campo]).replace(',', '').strip()
                        datos_limpiados[campo] = valor_limpio
                        if ',' in str(valor_original):
                            print(f"  {campo}: '{valor_original}' → '{valor_limpio}'")
                
                form = DeclaracionVolumenForm(datos_limpiados)
                
                if form.is_valid():
                    declaracion = form.save(commit=False)
                    declaracion.empresa = empresa  # IMPORTANTE: Establecer la empresa desde la sesión
                    declaracion.usuario = request.session.get('usuario', 'SISTEMA')
                    
                    # Buscar el negocio para obtener el idneg
                    try:
                        negocio_obj = Negocio.objects.get(empresa=empresa, rtm=declaracion.rtm, expe=declaracion.expe)
                        declaracion.idneg = negocio_obj.id
                    except Negocio.DoesNotExist:
                        declaracion.idneg = 0
                    
                    declaracion_existente = DeclaracionVolumen.objects.filter(
                        empresa=declaracion.empresa,
                        rtm=declaracion.rtm, expe=declaracion.expe,
                        ano=declaracion.ano, mes=declaracion.mes
                    ).first()
                    
                    if declaracion_existente:
                        declaracion_existente.empresa = empresa  # Asegurar que la empresa esté correcta
                        declaracion_existente.tipo = declaracion.tipo
                        declaracion_existente.ventai = declaracion.ventai
                        declaracion_existente.ventac = declaracion.ventac
                        declaracion_existente.ventas = declaracion.ventas
                        declaracion_existente.valorexcento = declaracion.valorexcento
                        declaracion_existente.controlado = declaracion.controlado
                        declaracion_existente.unidad = declaracion.unidad
                        declaracion_existente.factor = declaracion.factor
                        declaracion_existente.multadecla = declaracion.multadecla
                        declaracion_existente.impuesto = declaracion.impuesto
                        declaracion_existente.usuario = request.session.get('usuario', 'SISTEMA')
                        declaracion_existente.save()
                        mensaje = f'Declaración {declaracion.ano}/{declaracion.mes:02d} actualizada correctamente'
                    else:
                        declaracion.save()
                        mensaje = f'Declaración {declaracion.ano}/{declaracion.mes:02d} creada correctamente'
                    exito = True
                    print(f"✅ Declaración guardada correctamente: {mensaje}")
                    print("="*80)
                else:
                    mensaje = 'Error en el formulario: ' + ', '.join([str(error) for error in form.errors.values()])
                    exito = False
                    print("❌ Errores en el formulario:")
                    for campo, errores in form.errors.items():
                        print(f"  {campo}: {errores}")
                    print("="*80)
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
                        from tributario.models import TarifasICS
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
                cuenta = request.POST.get('cuenta', '')
                cuentarez = request.POST.get('cuentarez', '')
                if tarifa_id and codigo_tarifa and valor:
                    try:
                        from tributario.models import TarifasICS
                        tarifa_ics = TarifasICS.objects.get(id=tarifa_id, idneg=negocio.id)
                        tarifa_ics.cod_tarifa = codigo_tarifa
                        tarifa_ics.valor = valor
                        tarifa_ics.cuenta = cuenta
                        tarifa_ics.cuentarez = cuentarez
                        tarifa_ics.save()
                        mensaje = f'Tarifa actualizada correctamente'
                        exito = True
                    except TarifasICS.DoesNotExist:
                        mensaje = 'Tarifa no encontrada'
                        exito = False
                else:
                    mensaje = 'ID de tarifa, código y valor son requeridos'
                    exito = False
            elif accion == 'buscar_existente':
                # Manejar petición AJAX para buscar declaración existente
                print("="*80)
                print("[BACKEND] Busqueda de declaracion existente")
                print(f"[BACKEND] Empresa: {empresa}")
                print(f"[BACKEND] RTM: {rtm}")
                print(f"[BACKEND] EXPE: {expe}")
                
                ano = request.POST.get('ano')
                print(f"[BACKEND] Ano solicitado: {ano}")
                
                if ano:
                    try:
                        from tributario.models import DeclaracionVolumen
                        from django.http import JsonResponse
                        
                        print(f"[BACKEND] Buscando declaracion para: empresa={empresa}, rtm={rtm}, expe={expe}, ano={ano}")
                        
                        declaracion_existente = DeclaracionVolumen.objects.filter(
                            empresa=empresa,
                            rtm=rtm, 
                            expe=expe,
                            ano=int(ano)  # Solo validar por año
                        ).first()
                        
                        if declaracion_existente:
                            print(f"[BACKEND] Declaracion encontrada: {declaracion_existente.ano}/{declaracion_existente.mes:02d}")
                            
                            declaracion_data = {
                                'ano': declaracion_existente.ano,
                                'mes': declaracion_existente.mes,
                                'tipo': declaracion_existente.tipo,
                                'ventai': float(declaracion_existente.ventai) if declaracion_existente.ventai else 0,
                                'ventac': float(declaracion_existente.ventac) if declaracion_existente.ventac else 0,
                                'ventas': float(declaracion_existente.ventas) if declaracion_existente.ventas else 0,
                                'valorexcento': float(declaracion_existente.valorexcento) if declaracion_existente.valorexcento else 0,
                                'controlado': float(declaracion_existente.controlado) if declaracion_existente.controlado else 0,
                                'unidad': int(declaracion_existente.unidad) if declaracion_existente.unidad else 0,
                                'factor': float(declaracion_existente.factor) if declaracion_existente.factor else 0,
                                'multadecla': float(declaracion_existente.multadecla) if declaracion_existente.multadecla else 0,
                                'impuesto': float(declaracion_existente.impuesto) if declaracion_existente.impuesto else 0,
                                'ajuste': float(declaracion_existente.ajuste) if declaracion_existente.ajuste else 0,
                            }
                            
                            print(f"[BACKEND] Datos preparados: {declaracion_data}")
                            
                            response_data = {
                                'exito': True,
                                'declaracion': declaracion_data,
                                'mensaje': f'Declaracion {declaracion_existente.ano}/{declaracion_existente.mes:02d} encontrada'
                            }
                            
                            print(f"[BACKEND] Enviando respuesta JSON: {response_data}")
                            print("="*80)
                            
                            return JsonResponse(response_data)
                        else:
                            print(f"[BACKEND] No hay declaracion para el ano {ano}")
                            response_data = {
                                'exito': False,
                                'mensaje': f'No hay declaracion para el ano {ano}'
                            }
                            print(f"[BACKEND] Enviando respuesta JSON: {response_data}")
                            print("="*80)
                            return JsonResponse(response_data)
                    except Exception as e:
                        print(f"[BACKEND] ERROR al buscar declaracion: {str(e)}")
                        import traceback
                        traceback.print_exc()
                        response_data = {
                            'exito': False,
                            'mensaje': f'Error al buscar declaracion: {str(e)}'
                        }
                        print(f"[BACKEND] Enviando respuesta JSON: {response_data}")
                        print("="*80)
                        return JsonResponse(response_data)
                else:
                    print("[BACKEND] Ano no proporcionado en la peticion")
                    response_data = {
                        'exito': False,
                        'mensaje': 'Ano es requerido para buscar declaracion'
                    }
                    print(f"[BACKEND] Enviando respuesta JSON: {response_data}")
                    print("="*80)
                    return JsonResponse(response_data)
        except Exception as e:
            mensaje = f'Error: {str(e)}'
            exito = False

    if rtm and expe:
        try:
            from tributario.models import Negocio
            print(f"[DEBUG] Buscando negocio: empresa={empresa}, rtm={rtm}, expe={expe}")
            negocio = Negocio.objects.get(empresa=empresa, rtm=rtm, expe=expe)
            print(f"[DEBUG] Negocio encontrado: {negocio.nombrenego if negocio else 'None'}")
        except Negocio.DoesNotExist:
            print(f"[DEBUG] ERROR: Negocio no encontrado para empresa={empresa}, rtm={rtm}, expe={expe}")
            mensaje = 'Negocio no encontrado'
            exito = False
            negocio = None

        if negocio:
            try:
                from tributario.models import DeclaracionVolumen, TarifasICS, Rubro
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

    from .tributario_app.forms import DeclaracionVolumenForm
    from datetime import datetime
    
    # Configurar datos iniciales del formulario
    initial_data = {}
    
    # Configurar datos básicos si hay negocio
    if negocio and rtm and expe:
        initial_data = {'idneg': negocio.id, 'rtm': negocio.rtm, 'expe': negocio.expe}
        
        # Obtener año para buscar declaración existente
        ano_cargar = request.GET.get('ano_cargar')  # Parámetro de URL para año específico
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Usar año específico si se proporciona, sino usar año actual
        ano_buscar = int(ano_cargar) if ano_cargar else current_year
        
        print("="*80)
        print(f"[CARGA AUTO] Negocio: {negocio.nombrenego}")
        print(f"[CARGA AUTO] Ano cargar: {ano_cargar}")
        print(f"[CARGA AUTO] Ano buscar: {ano_buscar}")
        print("="*80)
        
        # Verificar si ya existe una declaración para el año especificado (SIN validar mes)
        try:
            from tributario.models import DeclaracionVolumen
            declaracion_actual = DeclaracionVolumen.objects.filter(
                empresa=empresa,
                rtm=negocio.rtm, 
                expe=negocio.expe,
                ano=ano_buscar  # Solo validar por año
            ).first()
            
            if declaracion_actual:
                print(f"[CARGA AUTO] EXITO - Declaracion encontrada para ano {ano_buscar}")
                print(f"[CARGA AUTO] Mes: {declaracion_actual.mes} (tipo: {type(declaracion_actual.mes)})")
                
                try:
                    initial_data.update({
                        'ano': int(declaracion_actual.ano),  # Convertir Decimal a int
                        'mes': int(declaracion_actual.mes),  # Convertir Decimal a int
                        'tipo': int(declaracion_actual.tipo) if declaracion_actual.tipo else 1,
                        'ventai': float(declaracion_actual.ventai) if declaracion_actual.ventai else 0,
                        'ventac': float(declaracion_actual.ventac) if declaracion_actual.ventac else 0,
                        'ventas': float(declaracion_actual.ventas) if declaracion_actual.ventas else 0,
                        'valorexcento': float(declaracion_actual.valorexcento) if declaracion_actual.valorexcento else 0,
                        'controlado': float(declaracion_actual.controlado) if declaracion_actual.controlado else 0,
                        'unidad': int(declaracion_actual.unidad) if declaracion_actual.unidad else 0,
                        'factor': float(declaracion_actual.factor) if declaracion_actual.factor else 0,
                        'multadecla': float(declaracion_actual.multadecla) if declaracion_actual.multadecla else 0,
                        'impuesto': float(declaracion_actual.impuesto) if declaracion_actual.impuesto else 0,
                        'ajuste': float(declaracion_actual.ajuste) if declaracion_actual.ajuste else 0
                    })
                    print(f"[CARGA AUTO] initial_data actualizado correctamente")
                    
                    mensaje = f'Declaracion {declaracion_actual.ano}/{int(declaracion_actual.mes or 0):02d} cargada desde la base de datos'
                    print(f"[CARGA AUTO] Mensaje creado: {mensaje}")
                    exito = True
                    
                    # Datos informativos de la declaración
                    declaracion_info = {
                        'id': declaracion_actual.id,
                        'usuario': declaracion_actual.usuario or 'N/A',
                        'fechssys': declaracion_actual.fechssys
                    }
                except Exception as e:
                    print(f"[CARGA AUTO] ERROR al actualizar initial_data: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"[CARGA AUTO] No hay declaracion para ano {ano_buscar} - usando valores por defecto")
                # Establecer año y mes por defecto
                initial_data.update({
                    'ano': ano_buscar,  # Usar el año que se está buscando
                    'mes': current_month,
                    'tipo': 1  # Normal por defecto
                })
        except Exception as e:
            print(f"[CARGA AUTO] ERROR: {e}")
            # En caso de error, usar valores por defecto
            initial_data.update({
                'ano': current_year,
                'mes': current_month,
                'tipo': 1
            })
    else:
        print(f"[CARGA AUTO] ERROR: negocio es None")
    
        form = DeclaracionVolumenForm(initial=initial_data)
    
    # Generar años disponibles (2020-2030)
    anos_disponibles = [{'ano': str(year)} for year in range(2020, 2031)]

    return render(request, 'declaracion_volumen.html', {
        'form': form, 'negocio': negocio, 'declaraciones': declaraciones,
        'tarifas_ics': tarifas_ics, 'mensaje': mensaje, 'exito': exito, 
        'empresa': empresa, 'anos_disponibles': anos_disponibles,
        'declaracion_info': declaracion_info,
        'modulo': 'Tributario', 'descripcion': 'Declaración de Volumen de Ventas'
    })

def miscelaneos(request):
    """Vista para misceláneos"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Cargar oficinas disponibles
    oficinas = []
    try:
        from tributario.models import Oficina
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
            from tributario.models import Actividad
            
            accion = request.POST.get('accion')
            empresa = request.POST.get('empresa', '')
            codigo = request.POST.get('codigo', '')
            descripcion = request.POST.get('descripcion', '')
            
            if accion == 'nuevo':
                # Limpiar campos para nuevo registro
                mensaje = 'Formulario preparado para nueva actividad'
                exito = True
                
            elif accion == 'guardar':
                # Capturar todos los campos
                cuenta = request.POST.get('cuenta', '').strip()
                cuentarez = request.POST.get('cuentarez', '').strip()
                cuentarec = request.POST.get('cuentarec', '').strip()
                cuentaint = request.POST.get('cuentaint', '').strip()
                
                # Usar cuenta si codigo está vacío
                if not codigo and cuenta:
                    codigo = cuenta
                
                # Usar empresa de sesión si está vacía
                if not empresa:
                    empresa = request.session.get('empresa', '0301')
                
                # Normalizar valores
                empresa = empresa if empresa else request.session.get('empresa', '0301')
                codigo = codigo if codigo else ''
                descripcion = descripcion if descripcion else ''
                cuentarez = cuentarez if cuentarez else ''
                cuentarec = cuentarec if cuentarec else ''
                cuentaint = cuentaint if cuentaint else ''
                
                # Validar campos obligatorios: Municipio, Cuenta y Descripción
                campos_faltantes = []
                if not empresa or empresa.strip() == '':
                    campos_faltantes.append('Municipio')
                if not codigo or codigo.strip() == '':
                    campos_faltantes.append('Cuenta')
                if not descripcion or descripcion.strip() == '':
                    campos_faltantes.append('Descripción')
                
                if campos_faltantes:
                    mensaje = f'Los siguientes campos son obligatorios: {", ".join(campos_faltantes)}'
                    exito = False
                else:
                    # GUARDAR - Validación pasada
                    if Actividad.objects.filter(empresa=empresa, codigo=codigo).exists():
                        # Actualizar actividad existente
                        actividad = Actividad.objects.get(empresa=empresa, codigo=codigo)
                        actividad.descripcion = descripcion
                        actividad.cuentarez = cuentarez
                        actividad.cuentarec = cuentarec
                        actividad.cuentaint = cuentaint
                        actividad.save()
                        mensaje = f'Actividad {codigo} actualizada correctamente'
                        exito = True
                    else:
                        # Crear nueva actividad
                        Actividad.objects.create(
                            empresa=empresa,
                            codigo=codigo,
                            descripcion=descripcion,
                            cuentarez=cuentarez,
                            cuentarec=cuentarec,
                            cuentaint=cuentaint
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
            from tributario.models import Actividad
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
    if empresa:
        try:
            from tributario.models import Oficina
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
            from tributario.models import Rubro, Actividad
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
    # Importar modelos y formularios
    # El modelo Tarifas está en models.py (tributario), no en tributario_app
    from tributario.models import Tarifas
    from tributario_app.forms import TarifasForm
    
    # Obtener empresa (municipio) de la sesión o GET
    # Convertir a string antes de aplicar strip para evitar errores con int
    empresa_get = request.GET.get('empresa', '')
    empresa = str(empresa_get).strip() if empresa_get else ''
    if not empresa:
        municipio_codigo = request.session.get('municipio_codigo', '')
        municipio_id = request.session.get('municipio_id', '')
        empresa = str(municipio_codigo).strip() if municipio_codigo else ''
        if not empresa:
            empresa = str(municipio_id).strip() if municipio_id else ''
    if not empresa:
        empresa = '0301'  # Valor por defecto
    
    # Obtener rubro de GET (parámetro codigo_rubro)
    codigo_rubro_get = request.GET.get('codigo_rubro', '')
    codigo_rubro = str(codigo_rubro_get).strip() if codigo_rubro_get else ''
    if not codigo_rubro:
        rubro_get = request.GET.get('rubro', '')
        codigo_rubro = str(rubro_get).strip() if rubro_get else ''
    
    # Obtener año (puede venir como int o string)
    ano_filtro_get = request.GET.get('ano', '')
    ano_filtro = str(ano_filtro_get).strip() if ano_filtro_get else ''
    
    print(f"[TARIFAS_CRUD] Empresa: '{empresa}', Rubro: '{codigo_rubro}', Año: '{ano_filtro}'")
    
    # Variables iniciales
    tarifas = []
    empresa_filtro = empresa
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
                
                # Preparar formulario después de la eliminación manteniendo empresa y rubro
                # Mantener el rubro de la tarifa eliminada o el heredado
                initial_data = {'empresa': empresa}
                if rubro_eliminar:
                    initial_data['rubro'] = rubro_eliminar
                    codigo_rubro = rubro_eliminar  # Actualizar para mantener en contexto
                elif codigo_rubro:
                    initial_data['rubro'] = codigo_rubro
                form = TarifasForm(initial=initial_data)
                
                # Actualizar los filtros para mantener la consulta filtrada
                if ano_eliminar:
                    ano_filtro = ano_eliminar
            else:
                # Manejar guardado/actualización de tarifa
                form = TarifasForm(request.POST)
                
                # Debug: Ver qué datos vienen en el POST
                print(f"[TARIFAS_CRUD] Datos POST recibidos:")
                print(f"   - valor (raw): '{request.POST.get('valor', 'NO_ENVIADO')}'")
                print(f"   - cod_tarifa: '{request.POST.get('cod_tarifa', 'NO_ENVIADO')}'")
                print(f"   - ano: '{request.POST.get('ano', 'NO_ENVIADO')}'")
                print(f"   - descripcion: '{request.POST.get('descripcion', 'NO_ENVIADO')}'")
                
                if form.is_valid():
                    try:
                        # Obtener datos del formulario validado
                        cleaned_data = form.cleaned_data
                        empresa_tarifa = empresa or cleaned_data.get('empresa', '').strip()
                        rubro_tarifa = (cleaned_data.get('rubro', '').strip() or codigo_rubro or '')
                        cod_tarifa = cleaned_data.get('cod_tarifa', '').strip()
                        ano = cleaned_data.get('ano')
                        descripcion = cleaned_data.get('descripcion', '').strip()
                        valor = cleaned_data.get('valor')
                        frecuencia = cleaned_data.get('frecuencia', '').strip()
                        tipo = cleaned_data.get('tipo', '').strip()
                        tipomodulo = cleaned_data.get('tipomodulo', '').strip()
                        
                        print(f"[TARIFAS_CRUD] Datos del formulario validado:")
                        print(f"   - valor (cleaned): {valor} (tipo: {type(valor)})")
                        print(f"   - cod_tarifa: {cod_tarifa}")
                        print(f"   - ano: {ano} (tipo: {type(ano)})")
                        print(f"   - descripcion: {descripcion}")
                        
                        if not empresa_tarifa:
                            raise ValueError("Empresa (municipio) es obligatoria")
                        if not cod_tarifa:
                            raise ValueError("Código de tarifa es obligatorio")
                        if not ano:
                            raise ValueError("Año es obligatorio")
                        
                        # Convertir año a Decimal si es necesario
                        from decimal import Decimal, InvalidOperation
                        if isinstance(ano, (int, float)):
                            ano = Decimal(str(int(ano)))
                        elif isinstance(ano, str):
                            ano = Decimal(ano)
                        
                        # Convertir valor a Decimal si es necesario
                        valor_original = valor
                        print(f"[TARIFAS_CRUD] Procesando valor:")
                        print(f"   - Valor recibido: {valor} (tipo: {type(valor)})")
                        
                        # Si el valor es None o vacío, usar 0.00
                        if valor is None:
                            print(f"   ⚠️ Valor es None, usando 0.00")
                            valor = Decimal('0.00')
                        elif isinstance(valor, Decimal):
                            print(f"   ✅ Valor ya es Decimal: {valor}")
                            # Ya es Decimal, no hacer nada
                            pass
                        elif isinstance(valor, (int, float)):
                            valor = Decimal(str(valor))
                            print(f"   ✅ Valor convertido de {type(valor_original)} a Decimal: {valor}")
                        elif isinstance(valor, str):
                            if valor.strip():
                                try:
                                    valor = Decimal(valor.strip())
                                    print(f"   ✅ Valor convertido de string '{valor_original}' a Decimal: {valor}")
                                except (ValueError, InvalidOperation) as e:
                                    print(f"   ❌ Error al convertir string a Decimal: {e}")
                                    valor = Decimal('0.00')
                            else:
                                print(f"   ⚠️ Valor string vacío, usando 0.00")
                                valor = Decimal('0.00')
                        else:
                            try:
                                valor = Decimal(str(valor))
                                print(f"   ✅ Valor convertido de {type(valor_original)} a Decimal: {valor}")
                            except (ValueError, InvalidOperation) as e:
                                print(f"   ❌ Error al convertir {type(valor_original)} a Decimal: {e}")
                                valor = Decimal('0.00')
                        
                        print(f"   ✅ Valor final procesado: {valor} (tipo: {type(valor)})")
                        
                        print(f"[TARIFAS_CRUD] Valor procesado:")
                        print(f"   - Valor original: {valor_original} (tipo: {type(valor_original)})")
                        print(f"   - Valor convertido: {valor} (tipo: {type(valor)})")
                        
                        # Buscar si existe una tarifa con los mismos criterios (unique_together: empresa, ano, cod_tarifa)
                        tarifa_existente = None
                        try:
                            tarifa_existente = Tarifas.objects.get(
                                empresa=empresa_tarifa,
                                ano=ano,
                                cod_tarifa=cod_tarifa
                            )
                            print(f"[TARIFAS_CRUD] Tarifa existente encontrada: ID={tarifa_existente.id}, Valor actual={tarifa_existente.valor}")
                        except Tarifas.DoesNotExist:
                            tarifa_existente = None
                            print(f"[TARIFAS_CRUD] Tarifa no existe, se creará nueva")
                        except Tarifas.MultipleObjectsReturned:
                            # Si hay múltiples, tomar el primero
                            tarifa_existente = Tarifas.objects.filter(
                                empresa=empresa_tarifa,
                                ano=ano,
                                cod_tarifa=cod_tarifa
                            ).first()
                            print(f"[TARIFAS_CRUD] Múltiples tarifas encontradas, usando la primera: ID={tarifa_existente.id}")
                        
                        if tarifa_existente:
                            # Actualizar tarifa existente
                            valor_antes = tarifa_existente.valor
                            tarifa_existente.rubro = rubro_tarifa
                            tarifa_existente.descripcion = descripcion
                            tarifa_existente.valor = valor
                            tarifa_existente.frecuencia = frecuencia
                            tarifa_existente.tipo = tipo
                            tarifa_existente.tipomodulo = tipomodulo
                            
                            print(f"💾 [TARIFAS_CRUD] Actualizando tarifa:")
                            print(f"   - Valor antes: {valor_antes}")
                            print(f"   - Valor nuevo: {valor}")
                            print(f"   - Descripción: {descripcion}")
                            print(f"   - Frecuencia: {frecuencia}")
                            print(f"   - Tipo: {tipo}")
                            
                            tarifa_existente.save()
                            
                            # Verificar que se guardó correctamente
                            tarifa_verificada = Tarifas.objects.get(pk=tarifa_existente.pk)
                            print(f"✅ [TARIFAS_CRUD] Tarifa guardada. Valor en BD: {tarifa_verificada.valor}")
                            
                            mensaje = f"Tarifa {cod_tarifa} (Año {ano}) actualizada exitosamente. Valor: {valor}"
                            exito = True
                        else:
                            # Crear nueva tarifa
                            tarifa = Tarifas(
                                empresa=empresa_tarifa,
                                rubro=rubro_tarifa,
                                cod_tarifa=cod_tarifa,
                                ano=ano,
                                descripcion=descripcion,
                                valor=valor,
                                frecuencia=frecuencia,
                                tipo=tipo,
                                tipomodulo=tipomodulo
                            )
                            tarifa.save()
                            mensaje = f"Tarifa {cod_tarifa} (Año {ano}) creada exitosamente."
                            exito = True

                        # Limpiar formulario después de cualquier operación manteniendo empresa y rubro
                        initial_data = {'empresa': empresa}
                        if codigo_rubro:
                            initial_data['rubro'] = codigo_rubro
                        form = TarifasForm(initial=initial_data)
                    except Exception as e:
                        import traceback
                        error_detail = traceback.format_exc()
                        print(f"❌ [TARIFAS_CRUD] Error al guardar: {str(e)}")
                        print(f"❌ [TARIFAS_CRUD] Detalle: {error_detail}")
                        mensaje = f"Error al procesar la tarifa: {str(e)}"
                        exito = False
                        # Mantener formulario con empresa y rubro
                        initial_data = {'empresa': empresa}
                        if codigo_rubro:
                            initial_data['rubro'] = codigo_rubro
                        form = TarifasForm(initial=initial_data)
                else:
                    mensaje = f"Error en el formulario: {form.errors}"
                    exito = False
                    # Mantener formulario con empresa y rubro aunque haya error
                    initial_data = {'empresa': empresa}
                    if codigo_rubro:
                        initial_data['rubro'] = codigo_rubro
                    form = TarifasForm(initial=initial_data)
        except Exception as e:
            mensaje = f"Error al procesar la tarifa: {str(e)}"
            exito = False
            # Mantener formulario con empresa y rubro
            initial_data = {'empresa': empresa}
            if codigo_rubro:
                initial_data['rubro'] = codigo_rubro
            form = TarifasForm(initial=initial_data)
    else:
        # Preparar formulario inicial con empresa y rubro heredados
        initial_data = {'empresa': empresa}
        if codigo_rubro:
            initial_data['rubro'] = codigo_rubro
        print(f"📋 [TARIFAS_CRUD] Formulario inicial - empresa: '{empresa}', rubro: '{codigo_rubro}'")
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
        'codigo_rubro': codigo_rubro,  # Pasar rubro al contexto para el template
        'ano_filtro': ano_filtro,
        'mensaje': mensaje,
        'exito': exito,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Tarifas'
    })

def plan_arbitrio_crud(request):
    """Vista para CRUD de plan de arbitrios con herencia de parámetros y filtrado del grid"""
    from tributario.models import PlanArbitrio, Rubro, Tarifas
    from .tributario_app.forms import PlanArbitrioForm
    
    # Obtener empresa (municipio) de la sesión o GET
    # Convertir a string antes de aplicar strip para evitar errores con int
    empresa_get = request.GET.get('empresa', '')
    empresa = str(empresa_get).strip() if empresa_get else ''
    if not empresa:
        municipio_codigo = request.session.get('municipio_codigo', '')
        municipio_id = request.session.get('municipio_id', '')
        empresa = str(municipio_codigo).strip() if municipio_codigo else ''
        if not empresa:
            empresa = str(municipio_id).strip() if municipio_id else ''
    if not empresa:
        empresa = '0301'  # Valor por defecto
    
    # Asegurar que tenga 4 dígitos
    if empresa and len(empresa) < 4:
        empresa = empresa.zfill(4)
    
    # Debug: Mostrar valores antes del procesamiento
    print(f"[DEBUG] Plan Arbitrio - Valores antes del procesamiento:")
    print(f"   GET empresa: '{request.GET.get('empresa', '')}'")
    print(f"   Session municipio_codigo: '{request.session.get('municipio_codigo', '')}'")
    print(f"   Session municipio_id: '{request.session.get('municipio_id', '')}'")
    print(f"   Municipio final: '{empresa}'")
    
    # Obtener rubro (puede venir como 'rubro' o 'codigo_rubro')
    rubro_get = request.GET.get('rubro', '')
    codigo_rubro_get = request.GET.get('codigo_rubro', '')
    rubro_codigo = str(rubro_get).strip() if rubro_get else ''
    if not rubro_codigo:
        rubro_codigo = str(codigo_rubro_get).strip() if codigo_rubro_get else ''
    # Obtener año (puede venir como int o string)
    ano_get = request.GET.get('ano', '')
    ano_heredado = str(ano_get).strip() if ano_get else ''
    
    # Obtener código de tarifa (puede venir como 'cod_tarifa' o 'codigo_tarifa')
    cod_tarifa_get = request.GET.get('cod_tarifa', '')
    codigo_tarifa_get = request.GET.get('codigo_tarifa', '')
    cod_tarifa_heredado = str(cod_tarifa_get).strip() if cod_tarifa_get else ''
    if not cod_tarifa_heredado:
        cod_tarifa_heredado = str(codigo_tarifa_get).strip() if codigo_tarifa_get else ''
    
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
        'empresa': empresa if empresa else '0301',
        'rubro': rubro_codigo if rubro_codigo else '',
        'cod_tarifa': cod_tarifa_heredado if cod_tarifa_heredado else '',
        'ano': ano_heredado if ano_heredado else '',
    }
    
    print(f"[DEBUG] Initial data para formulario:")
    print(f"   empresa: '{initial_data['empresa']}'")
    print(f"   rubro: '{initial_data['rubro']}'")
    print(f"   cod_tarifa: '{initial_data['cod_tarifa']}'")
    print(f"   ano: '{initial_data['ano']}'")
    
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
                    # Debug: Ver todos los datos del formulario
                    print(f"🔍 [PLAN_ARBITRIO] Todos los datos del formulario validado:")
                    for key, value in form.cleaned_data.items():
                        print(f"   - {key}: {value} (tipo: {type(value)})")
                    
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
                        nuevo_valor_manual = form.cleaned_data.get('valor')  # Valor ingresado manualmente
                        
                        print(f"🔍 [PLAN_ARBITRIO] Valores del formulario:")
                        print(f"   - mínimo: {nuevo_minimo} (tipo: {type(nuevo_minimo)})")
                        print(f"   - máximo: {nuevo_maximo} (tipo: {type(nuevo_maximo)})")
                        print(f"   - valor manual: {nuevo_valor_manual} (tipo: {type(nuevo_valor_manual)})")
                        
                        # Convertir tipos a Decimal si es necesario
                        from decimal import Decimal
                        if isinstance(nuevo_minimo, (int, float)):
                            nuevo_minimo = Decimal(str(nuevo_minimo))
                        elif isinstance(nuevo_minimo, str):
                            nuevo_minimo = Decimal(nuevo_minimo) if nuevo_minimo.strip() else Decimal('0.00')
                        elif not isinstance(nuevo_minimo, Decimal):
                            nuevo_minimo = Decimal('0.00')
                        
                        if isinstance(nuevo_maximo, (int, float)):
                            nuevo_maximo = Decimal(str(nuevo_maximo))
                        elif isinstance(nuevo_maximo, str):
                            nuevo_maximo = Decimal(nuevo_maximo) if nuevo_maximo.strip() else Decimal('0.00')
                        elif not isinstance(nuevo_maximo, Decimal):
                            nuevo_maximo = Decimal('0.00')
                        
                        # Si el usuario ingresó un valor manualmente, usar ese valor
                        # Si no, calcular como promedio de mínimo y máximo
                        if nuevo_valor_manual is not None and nuevo_valor_manual != '':
                            # Convertir valor manual a Decimal
                            if isinstance(nuevo_valor_manual, (int, float)):
                                nuevo_valor = Decimal(str(nuevo_valor_manual))
                            elif isinstance(nuevo_valor_manual, str):
                                nuevo_valor = Decimal(nuevo_valor_manual) if nuevo_valor_manual.strip() else Decimal('0.00')
                            elif isinstance(nuevo_valor_manual, Decimal):
                                nuevo_valor = nuevo_valor_manual
                            else:
                                nuevo_valor = Decimal('0.00')
                            print(f"   ✅ Usando valor manual ingresado: {nuevo_valor}")
                        else:
                            # Calcular el valor automáticamente como promedio
                            if nuevo_minimo is not None and nuevo_maximo is not None:
                                nuevo_valor = (nuevo_minimo + nuevo_maximo) / 2
                            elif nuevo_minimo is not None:
                                nuevo_valor = nuevo_minimo
                            elif nuevo_maximo is not None:
                                nuevo_valor = nuevo_maximo
                            else:
                                nuevo_valor = Decimal('0.00')
                            print(f"   ✅ Calculando valor automáticamente (promedio): {nuevo_valor}")
                        
                        # Asegurar que ano sea Decimal para la comparación
                        if isinstance(ano, (int, float)):
                            ano_decimal = Decimal(str(int(ano)))
                        elif isinstance(ano, str):
                            ano_decimal = Decimal(ano)
                        else:
                            ano_decimal = ano
                        
                        # Usar update() para evitar la validación de unique_together
                        rows_updated = PlanArbitrio.objects.filter(
                            empresa=empresa,
                            rubro=rubro,
                            cod_tarifa=cod_tarifa,
                            ano=ano_decimal,
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
                        
                        # Obtener datos del formulario validado
                        cleaned_data = form.cleaned_data
                        empresa_plan = cleaned_data.get('empresa', '').strip()
                        rubro_plan = cleaned_data.get('rubro', '').strip()
                        cod_tarifa_plan = cleaned_data.get('cod_tarifa', '').strip()
                        ano_plan = cleaned_data.get('ano')
                        codigo_plan = cleaned_data.get('codigo', '').strip()
                        descripcion_plan = cleaned_data.get('descripcion', '').strip()
                        minimo_plan = cleaned_data.get('minimo', 0.00)
                        maximo_plan = cleaned_data.get('maximo', 0.00)
                        valor_manual_plan = cleaned_data.get('valor')  # Valor ingresado manualmente
                        
                        print(f"🔍 [PLAN_ARBITRIO] Creando nuevo registro:")
                        print(f"   - mínimo: {minimo_plan} (tipo: {type(minimo_plan)})")
                        print(f"   - máximo: {maximo_plan} (tipo: {type(maximo_plan)})")
                        print(f"   - valor manual: {valor_manual_plan} (tipo: {type(valor_manual_plan)})")
                        
                        # Validar campos obligatorios
                        if not empresa_plan:
                            raise ValueError("Empresa (municipio) es obligatoria")
                        if not rubro_plan:
                            raise ValueError("Rubro es obligatorio")
                        if not cod_tarifa_plan:
                            raise ValueError("Código de tarifa es obligatorio")
                        if not ano_plan:
                            raise ValueError("Año es obligatorio")
                        if not codigo_plan:
                            raise ValueError("Código es obligatorio")
                        
                        # Convertir tipos si es necesario
                        from decimal import Decimal
                        if isinstance(ano_plan, (int, float)):
                            ano_plan = Decimal(str(int(ano_plan)))
                        elif isinstance(ano_plan, str):
                            ano_plan = Decimal(ano_plan)
                        
                        if isinstance(minimo_plan, (int, float)):
                            minimo_plan = Decimal(str(minimo_plan))
                        elif isinstance(minimo_plan, str):
                            minimo_plan = Decimal(minimo_plan) if minimo_plan.strip() else Decimal('0.00')
                        
                        if isinstance(maximo_plan, (int, float)):
                            maximo_plan = Decimal(str(maximo_plan))
                        elif isinstance(maximo_plan, str):
                            maximo_plan = Decimal(maximo_plan) if maximo_plan.strip() else Decimal('0.00')
                        
                        # Si el usuario ingresó un valor manualmente, usar ese valor
                        # Si no, calcular como promedio de mínimo y máximo
                        if valor_manual_plan is not None and valor_manual_plan != '':
                            # Convertir valor manual a Decimal
                            if isinstance(valor_manual_plan, (int, float)):
                                valor_plan = Decimal(str(valor_manual_plan))
                            elif isinstance(valor_manual_plan, str):
                                valor_plan = Decimal(valor_manual_plan) if valor_manual_plan.strip() else Decimal('0.00')
                            elif isinstance(valor_manual_plan, Decimal):
                                valor_plan = valor_manual_plan
                            else:
                                valor_plan = Decimal('0.00')
                            print(f"   ✅ Usando valor manual ingresado: {valor_plan}")
                        else:
                            # Calcular el valor automáticamente como promedio
                            if minimo_plan is not None and maximo_plan is not None:
                                valor_plan = (minimo_plan + maximo_plan) / 2
                            elif minimo_plan is not None:
                                valor_plan = minimo_plan
                            elif maximo_plan is not None:
                                valor_plan = maximo_plan
                            else:
                                valor_plan = Decimal('0.00')
                            print(f"   ✅ Calculando valor automáticamente (promedio): {valor_plan}")
                        
                        # Crear nueva instancia del modelo
                        plan_nuevo = PlanArbitrio(
                            empresa=empresa_plan,
                            rubro=rubro_plan,
                            cod_tarifa=cod_tarifa_plan,
                            ano=ano_plan,
                            codigo=codigo_plan,
                            descripcion=descripcion_plan,
                            minimo=minimo_plan,
                            maximo=maximo_plan,
                            valor=valor_plan
                        )
                        plan_nuevo.save()
                        
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
    # Si no hay datos iniciales previos, asegurar que empresa siempre tenga un valor
    if not initial_data.get('empresa'):
        initial_data['empresa'] = empresa if empresa else '0301'
    
    form = PlanArbitrioForm(initial=initial_data)
    
    # Debug: Verificar valores del formulario
    print(f"[DEBUG] Valores del formulario después de crear:")
    print(f"   form.initial.get('empresa'): '{form.initial.get('empresa', 'NO DEFINIDO')}'")
    if 'empresa' in form.fields:
        print(f"   form['empresa'].value(): '{form['empresa'].value()}'")
        # Forzar el valor inicial del campo empresa
        if form['empresa'].value() != initial_data.get('empresa', ''):
            form.fields['empresa'].initial = initial_data.get('empresa', '0301')
            print(f"   form.fields['empresa'].initial actualizado a: '{form.fields['empresa'].initial}'")
    
    # Filtrar grid de planes de arbitrio según parámetros heredados
    from decimal import Decimal
    
    # Inicializar consulta con filtro de empresa (obligatorio)
    if empresa:
        planes_query = PlanArbitrio.objects.filter(empresa=empresa)
        print(f"[DEBUG] Filtrando por empresa: '{empresa}'")
    else:
        # Si no hay empresa, no mostrar nada o mostrar error
        planes_query = PlanArbitrio.objects.none()
        print(f"[WARNING] No se proporcionó empresa, no se mostrarán planes")
    
    # Aplicar filtros adicionales si están presentes
    if rubro_codigo and planes_query:
        planes_query = planes_query.filter(rubro=rubro_codigo)
        print(f"[DEBUG] Filtrando por rubro: '{rubro_codigo}'")
    
    if ano_heredado and planes_query:
        # Convertir año a Decimal para coincidir con el tipo del modelo
        try:
            ano_decimal = Decimal(str(ano_heredado))
            planes_query = planes_query.filter(ano=ano_decimal)
            print(f"[DEBUG] Filtrando por año: {ano_decimal}")
        except (ValueError, TypeError) as e:
            print(f"[WARNING] Error al convertir año '{ano_heredado}': {e}")
    
    if cod_tarifa_heredado and planes_query:
        planes_query = planes_query.filter(cod_tarifa=cod_tarifa_heredado)
        print(f"[DEBUG] Filtrando por código de tarifa: '{cod_tarifa_heredado}'")
    
    # Ordenar planes por Año, Rubro, Código de Tarifa, Categoría y Código para el grid
    planes_arbitrio = planes_query.order_by('ano', 'rubro', 'cod_tarifa', 'tipocat', 'codigo') if planes_query else PlanArbitrio.objects.none()
    
    total_planes = planes_arbitrio.count()
    print(f"📊 Planes encontrados: {total_planes}")
    if total_planes > 0:
        print(f"📋 Primeros planes: {list(planes_arbitrio[:3].values_list('codigo', 'rubro', 'cod_tarifa', 'tipocat', 'ano'))}")
    
    context = {
        'form': form,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Plan de Arbitrios',
        'empresa_filtro': empresa if empresa else '0301',
        'rubro_filtro': rubro_codigo,
        'ano_filtro': ano_heredado,
        'cod_tarifa_filtro': cod_tarifa_heredado,
        'planes_arbitrio': planes_arbitrio,
        'mensaje': mensaje,
        'exito': exito,
    }
    
    # Debug final
    print(f"[DEBUG] Context enviado al template:")
    print(f"   empresa_filtro: '{context['empresa_filtro']}'")
    
    return render(request, 'formulario_plan_arbitrio.html', context)

@csrf_exempt
def buscar_rubro_plan_arbitrio(request):
    """Vista AJAX para buscar rubro en plan de arbitrio"""
    if request.method == 'POST':
        try:
            from tributario.models import Rubro
            
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
            from tributario.models import Tarifas, Rubro
            
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
                from tributario.models import Tarifas
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
    """Vista AJAX para búsqueda automática de tarifa con validación completa
    REQUIERE: empresa, rubro, cod_tarifa y ano para evitar mezclas entre rubros
    """
    if request.method == 'POST':
        try:
            empresa = request.POST.get('empresa', '').strip()
            rubro = request.POST.get('rubro', '').strip()
            ano = request.POST.get('ano', '').strip()
            codigo = request.POST.get('cod_tarifa', '').strip()
            
            print(f"[DEBUG] Búsqueda automática: empresa={empresa}, rubro={rubro}, año={ano}, codigo={codigo}")
            
            # Validar que TODOS los campos requeridos estén presentes
            if not empresa:
                print("[ERROR] Empresa vacía")
                return JsonResponse({'exito': False, 'mensaje': 'El código de municipio es obligatorio'})
            
            if not rubro:
                print("[ERROR] Rubro vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El código de rubro es obligatorio para la búsqueda automática'})
            
            if not ano:
                print("[ERROR] Año vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El año es obligatorio para la búsqueda automática'})
            
            if not codigo:
                print("[ERROR] Código de tarifa vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El código de tarifa es obligatorio'})
            
            # Convertir año a Decimal si es necesario para la búsqueda
            from decimal import Decimal, InvalidOperation
            try:
                if isinstance(ano, str):
                    ano_decimal = Decimal(ano)
                elif isinstance(ano, (int, float)):
                    ano_decimal = Decimal(str(int(ano)))
                else:
                    ano_decimal = ano
            except (InvalidOperation, ValueError):
                print(f"[ERROR] Año inválido: {ano}")
                return JsonResponse({'exito': False, 'mensaje': f'Año inválido: {ano}'})
            
            try:
                from tributario.models import Tarifas
                # Buscar tarifa con los CUATRO criterios obligatorios: empresa, rubro, ano y cod_tarifa
                print(f"[DEBUG] Buscando tarifa con criterios: empresa={empresa}, rubro={rubro}, ano={ano_decimal}, codigo={codigo}")
                
                tarifa = Tarifas.objects.filter(
                    empresa=empresa,
                    rubro=rubro,
                    ano=ano_decimal,
                    cod_tarifa=codigo
                ).first()
                
                if tarifa:
                    print(f"[OK] Tarifa encontrada: {tarifa.descripcion} (Rubro: {tarifa.rubro}, Año: {tarifa.ano})")
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
                    print(f"[ERROR] Tarifa no encontrada: empresa={empresa}, rubro={rubro}, año={ano_decimal}, codigo={codigo}")
                    return JsonResponse({
                        'exito': False, 
                        'mensaje': f'No se encontró una tarifa con código "{codigo}" para el rubro "{rubro}" en el año "{ano}". Puede crear una nueva tarifa.'
                    })
            except Exception as e:
                print(f"[ERROR] Error al buscar tarifa: {str(e)}")
                import traceback
                traceback.print_exc()
                return JsonResponse({'exito': False, 'mensaje': f'Error en el servidor: {str(e)}'})
        except Exception as e:
            print(f"[ERROR] Error en búsqueda automática: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'exito': False, 'mensaje': f'Error en el servidor: {str(e)}'})
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'})

def plan_arbitrio(request):
    """Vista para plan de arbitrios"""
    return render(request, 'formulario_plan_arbitrio.html', {
        'modulo': 'Tributario',
        'descripcion': 'Plan de Arbitrios'
    })

@csrf_exempt
@csrf_exempt
def buscar_plan_arbitrio(request):
    """Vista AJAX para buscar plan de arbitrio según código de tarifa"""
    if request.method == 'POST':
        try:
            import json
            # Intentar obtener datos como JSON primero
            try:
                data = json.loads(request.body)
                empresa = data.get('empresa', '').strip()
                rubro = data.get('rubro', '').strip()
                ano = data.get('ano', '').strip()
                cod_tarifa = data.get('cod_tarifa', '').strip()
                codigo = data.get('codigo', '').strip()
                tipocat = data.get('tipocat', '').strip()
                tipomodulo = data.get('tipomodulo', '').strip()
            except (json.JSONDecodeError, AttributeError):
                # Si no es JSON, usar FormData
                empresa = request.POST.get('empresa', '').strip()
                rubro = request.POST.get('rubro', '').strip()
                ano = request.POST.get('ano', '').strip()
                cod_tarifa = request.POST.get('cod_tarifa', '').strip()
                codigo = request.POST.get('codigo', '').strip()
                tipocat = request.POST.get('tipocat', '').strip()
                tipomodulo = request.POST.get('tipomodulo', '').strip()
            
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
            
            from tributario.models import PlanArbitrio, Tarifas
            from decimal import Decimal
            
            # FALLBACK: Si tipomodulo no viene pero hay tipocat, intentar obtenerlo de la tarifa
            if not tipomodulo and tipocat and empresa and cod_tarifa:
                try:
                    tarifa = Tarifas.objects.filter(
                        empresa=empresa,
                        cod_tarifa=cod_tarifa,
                        rubro=rubro if rubro else None,
                        ano=ano if ano else None
                    ).first()
                    if not tarifa and ano:
                        tarifa = Tarifas.objects.filter(
                            empresa=empresa,
                            cod_tarifa=cod_tarifa
                        ).order_by('-ano').first()
                    if tarifa and hasattr(tarifa, 'tipomodulo'):
                        tipomodulo = tarifa.tipomodulo or ''
                except Exception:
                    pass
            
            # Construir filtros según tipomodulo
            if tipomodulo and tipomodulo.strip().upper() == 'D':
                # Para tarifa Doméstica: incluir tipocat
                # CRÍTICO: tipocat es CHAR(1), usar string directamente
                import re
                tipocat_valor_str = ''
                if tipocat:
                    match = re.match(r'^([123])', tipocat)
                    if match:
                        tipocat_valor_str = match.group(1)  # '1', '2' o '3'
                filtros = {
                    'empresa': empresa,
                    'rubro': rubro,
                    'cod_tarifa': cod_tarifa,
                    'tipocat': tipocat_valor_str,  # String: '1', '2', '3' o ''
                    'ano': Decimal(str(ano)) if ano else None,
                    'codigo': codigo if codigo else None
                }
            else:
                # Para otras tarifas: sin tipocat (usar string vacío)
                filtros = {
                    'empresa': empresa,
                    'rubro': rubro,
                    'cod_tarifa': cod_tarifa,
                    'tipocat': '',  # String vacío para no-domésticas
                    'ano': Decimal(str(ano)) if ano else None,
                    'codigo': codigo if codigo else None
                }
            
            # Si no hay codigo, quitar del filtro
            if not codigo:
                filtros.pop('codigo', None)
            
            # Buscar plan con los criterios correspondientes
            plan = PlanArbitrio.objects.filter(**filtros).first()
            
            if plan:
                print(f"[OK] Plan encontrado: {plan.descripcion}")
                concepto_data = {
                    'empresa': plan.empresa or '',
                    'rubro': plan.rubro or '',
                    'cod_tarifa': plan.cod_tarifa or '',
                    'tipocat': str(plan.tipocat) if hasattr(plan, 'tipocat') and plan.tipocat is not None and plan.tipocat else '',  # CHAR(1): '1', '2', '3' o ''
                    'ano': str(plan.ano) if plan.ano else '',
                    'codigo': plan.codigo or '',
                    'descripcion': plan.descripcion or '',
                    'minimo': str(plan.minimo) if plan.minimo else '0.00',
                    'maximo': str(plan.maximo) if plan.maximo else '0.00',
                    'valor': str(plan.valor) if plan.valor else '0.00'
                }
                return JsonResponse({
                    'exito': True,
                    'existe': True,
                    'concepto': concepto_data
                })
            else:
                print(f"[ERROR] Plan no encontrado: empresa={empresa}, rubro={rubro}, año={ano}, cod_tarifa={cod_tarifa}")
                return JsonResponse({
                    'exito': True,
                    'existe': False,
                    'mensaje': 'Plan de arbitrio no encontrado'
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
            cod_tarifa = request.POST.get('cod_tarifa', '').strip()
            ano = request.POST.get('ano', '').strip()
            codigo = request.POST.get('codigo', '').strip()
            tipocat = request.POST.get('tipocat', '').strip()
            tipomodulo = request.POST.get('tipomodulo', '').strip()
            
            print(f"[DEBUG] ========== BÚSQUEDA AUTOMÁTICA - PARÁMETROS RECIBIDOS ==========")
            print(f"[DEBUG] empresa={empresa}, rubro={rubro}, cod_tarifa={cod_tarifa}, año={ano}, codigo={codigo}")
            print(f"[DEBUG] tipocat={tipocat}, tipomodulo={tipomodulo}")
            print(f"[DEBUG] ⚠️ VALIDACIÓN CRÍTICA: tipomodulo='{tipomodulo}' (tipo: {type(tipomodulo)}, longitud: {len(tipomodulo) if tipomodulo else 0})")
            print(f"[DEBUG] ⚠️ VALIDACIÓN CRÍTICA: tipocat='{tipocat}' (tipo: {type(tipocat)}, longitud: {len(tipocat) if tipocat else 0})")
            if tipomodulo:
                print(f"[DEBUG] ✅ tipomodulo recibido: '{tipomodulo}'")
                if tipomodulo == 'D':
                    print(f"[DEBUG] ✅✅✅ tipomodulo ES 'D' - DEBE incluir tipocat en filtros")
                else:
                    print(f"[DEBUG] ⚠️ tipomodulo NO es 'D' (es '{tipomodulo}') - NO incluirá tipocat")
            else:
                print(f"[DEBUG] ❌❌❌ PROBLEMA: tipomodulo está VACÍO o None - NO se incluirá tipocat")
                print(f"[DEBUG] ❌ Esto significa que el frontend NO está enviando tipomodulo correctamente")
            
            # Validar que todos los campos requeridos estén presentes
            if not empresa:
                print("[ERROR] Empresa vacía")
                return JsonResponse({'exito': False, 'mensaje': 'El código de municipio es obligatorio'})
            
            if not rubro:
                print("[ERROR] Rubro vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El código de rubro es obligatorio'})
            
            if not cod_tarifa:
                print("[ERROR] Código de tarifa vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El código de tarifa es obligatorio'})
            
            if not ano:
                print("[ERROR] Año vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El año es obligatorio'})
            
            if not codigo:
                print("[ERROR] Código vacío")
                return JsonResponse({'exito': False, 'mensaje': 'El código es obligatorio'})
            
            from tributario.models import PlanArbitrio, Tarifas
            
            # FALLBACK: Si tipomodulo no viene pero hay tipocat, intentar obtenerlo de la tarifa
            if not tipomodulo and tipocat and empresa and cod_tarifa:
                print(f"[DEBUG] ⚠️ tipomodulo no recibido pero hay tipocat, intentando obtenerlo de la tarifa...")
                try:
                    tarifa = Tarifas.objects.filter(
                        empresa=empresa,
                        cod_tarifa=cod_tarifa,
                        rubro=rubro if rubro else None,
                        ano=ano if ano else None
                    ).first()
                    if not tarifa and ano:
                        tarifa = Tarifas.objects.filter(
                            empresa=empresa,
                            cod_tarifa=cod_tarifa
                        ).order_by('-ano').first()
                    if tarifa and hasattr(tarifa, 'tipomodulo'):
                        tipomodulo = tarifa.tipomodulo or ''
                        print(f"[DEBUG] ✅ tipomodulo obtenido de tarifa: '{tipomodulo}'")
                    else:
                        print(f"[DEBUG] ⚠️ No se encontró tarifa para obtener tipomodulo")
                except Exception as e:
                    print(f"[DEBUG] ⚠️ Error al obtener tipomodulo de tarifa: {str(e)}")
            
            print(f"[DEBUG] Iniciando construcción de filtros de búsqueda...")
            print(f"[DEBUG] ⚠️ VALIDANDO tipomodulo antes de construir filtros: tipomodulo='{tipomodulo}'")
            print(f"[DEBUG] ⚠️ Comparación: tipomodulo == 'D' ? {tipomodulo and tipomodulo.strip().upper() == 'D'}")
            
            # Para tarifa Doméstica: SIEMPRE incluir tipocat en la búsqueda (OBLIGATORIO)
            # BÚSQUEDA AUTOMÁTICA DOMÉSTICA: empresa, rubro, cod_tarifa, tipocat, ano, codigo
            # CRÍTICO: tipocat es CHAR(1), usar string directamente
            import re
            if tipomodulo and tipomodulo.strip().upper() == 'D':
                # Construir filtros con tipocat (SIEMPRE requerida para Doméstica)
                tipocat_valor_str = ''
                if tipocat:
                    match = re.match(r'^([123])', tipocat)
                    if match:
                        tipocat_valor_str = match.group(1)  # '1', '2' o '3'
                filtros = {
                    'empresa': empresa,
                    'rubro': rubro,
                    'cod_tarifa': cod_tarifa,
                    'tipocat': tipocat_valor_str,  # String: '1', '2', '3' o '' (OBLIGATORIO para Doméstica)
                    'ano': ano,
                    'codigo': codigo
                }
                print(f"[DEBUG] ========== ✅✅✅ BÚSQUEDA AUTOMÁTICA DOMÉSTICA - TIPOCAT OBLIGATORIA ✅✅✅ ==========")
                print(f"[DEBUG] ⚠️ IMPORTANTE: La búsqueda INCLUYE tipocat como parámetro obligatorio")
                print(f"[DEBUG] ✅✅✅ FILTROS CONSTRUIDOS CON TIPOCAT: tipocat='{tipocat_valor_str}'")
                print(f"[DEBUG] Parámetros de búsqueda EXACTOS: empresa={empresa}, rubro={rubro}, cod_tarifa={cod_tarifa}, tipocat='{tipocat_valor_str}', ano={ano}, codigo={codigo}")
                print(f"[DEBUG] Solo se encontrará un registro si TODOS estos parámetros coinciden EXACTAMENTE")
                print(f"[DEBUG] Si existe un registro con tipocat diferente, NO se encontrará")
            else:
                # Para otras tarifas: búsqueda sin tipocat
                # BÚSQUEDA AUTOMÁTICA NO-DOMÉSTICA: empresa, rubro, cod_tarifa, ano, codigo
                print(f"[DEBUG] ⚠️⚠️⚠️ ENTRANDO A BLOQUE NO-DOMÉSTICA ⚠️⚠️⚠️")
                print(f"[DEBUG] ⚠️ tipomodulo='{tipomodulo}' NO es 'D', por lo que NO se incluirá tipocat")
                filtros = {
                    'empresa': empresa,
                    'rubro': rubro,
                    'cod_tarifa': cod_tarifa,
                    'tipocat': '',  # String vacío para no-domésticas
                    'ano': ano,
                    'codigo': codigo
                }
                print(f"[DEBUG] ❌❌❌ BÚSQUEDA AUTOMÁTICA NO-DOMÉSTICA - TIPOCAT VACÍO ❌❌❌")
                print(f"[DEBUG] Parámetros de búsqueda: empresa={empresa}, rubro={rubro}, cod_tarifa={cod_tarifa}, tipocat='', ano={ano}, codigo={codigo}")
                print(f"[DEBUG] ⚠️ Si esto es una tarifa Doméstica, hay un PROBLEMA: el frontend NO está enviando tipomodulo='D'")
            
            # Buscar plan con los criterios correspondientes
            plan = PlanArbitrio.objects.filter(**filtros).first()
            
            print(f"[DEBUG] ========== RESULTADO DE BÚSQUEDA ==========")
            if plan:
                print(f"[DEBUG] ✅ Plan encontrado: ID={plan.id}, tipocat={plan.tipocat}")
            else:
                print(f"[DEBUG] ❌ NO se encontró ningún plan con los filtros especificados")
                if tipomodulo == 'D' and tipocat_valor_str:
                    print(f"[DEBUG] ⚠️ Para tarifa Doméstica, se requiere coincidencia EXACTA en todos los parámetros incluyendo tipocat='{tipocat_valor_str}'")
            print(f"[DEBUG] Filtros utilizados: {filtros}")
            
            if plan:
                print(f"[OK] Plan encontrado: {plan.descripcion}")
                plan_data = {
                    'id': plan.id,
                    'empresa': plan.empresa,
                    'rubro': plan.rubro,
                    'cod_tarifa': plan.cod_tarifa,
                    'tipocat': str(plan.tipocat) if hasattr(plan, 'tipocat') and plan.tipocat is not None and plan.tipocat else '',  # CHAR(1): '1', '2', '3' o ''
                    'ano': str(plan.ano),
                    'codigo': plan.codigo,
                    'descripcion': plan.descripcion,
                    'minimo': str(plan.minimo),
                    'maximo': str(plan.maximo),
                    'valor': str(plan.valor)
                }
                return JsonResponse({
                    'exito': True,
                    'plan': plan_data,
                    'mensaje': f'Plan encontrado: {plan.descripcion}',
                    'encontrado_en_otro_ano': False
                })
            else:
                tipocat_msg = f' con tipocat "{tipocat}"' if tipomodulo == 'D' and tipocat else ''
                print(f"[ERROR] Plan no encontrado: empresa={empresa}, rubro={rubro}, cod_tarifa={cod_tarifa}, año={ano}, codigo={codigo}{tipocat_msg}")
                return JsonResponse({
                    'exito': False, 
                    'mensaje': f'No se encontró un plan con código "{codigo}" para el rubro "{rubro}" en el año "{ano}"{tipocat_msg}. Puede crear un nuevo plan.'
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
                from tributario.models import Rubro
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
                from tributario.models import Identificacion
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
            # Si no es JSON, intentar procesar como form-urlencoded
            try:
                data = request.POST
                accion = data.get('accion')
                if accion == 'salvar':
                    return handle_salvar_negocio(request, data)
                elif accion == 'eliminar':
                    return handle_eliminar_negocio(request, data)
            except:
                pass
            return JsonResponse({
                'exito': False,
                'mensaje': 'Error al procesar los datos. Por favor, intente nuevamente.'
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
        from tributario.models import TarifasImptoics
        
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
                from tributario.models import Identificacion
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
            # Si no es JSON, intentar procesar como form-urlencoded
            try:
                data = request.POST
                accion = data.get('accion')
                if accion == 'salvar':
                    return handle_salvar_negocio(request, data)
                elif accion == 'eliminar':
                    return handle_eliminar_negocio(request, data)
            except:
                pass
            return JsonResponse({
                'exito': False,
                'mensaje': 'Error al procesar los datos. Por favor, intente nuevamente.'
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
        from tributario.models import TarifasImptoics
        
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
            
            from tributario.models import PlanArbitrio
            
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
            # Si no es JSON, intentar procesar como form-urlencoded
            try:
                data = request.POST
                accion = data.get('accion')
                if accion == 'salvar':
                    return handle_salvar_negocio(request, data)
                elif accion == 'eliminar':
                    return handle_eliminar_negocio(request, data)
            except:
                pass
            return JsonResponse({
                'exito': False,
                'mensaje': 'Error al procesar los datos. Por favor, intente nuevamente.'
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
            from tributario.models import TarifasICS
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
                from tributario.models import Rubro
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

@csrf_exempt
def buscar_identificacion(request):
    """Vista AJAX para buscar identificación por DNI"""
    from .buscar_identificacion import buscar_identificacion as buscar_identificacion_func
    return buscar_identificacion_func(request)

def miscelaneos(request):
    """Vista para misceláneos del sistema tributario"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Cargar oficinas para el combobox
    try:
        from tributario.models import Oficina
        oficinas = Oficina.objects.filter(empresa=empresa).order_by('codigo')
        oficinas_list = [
            {'codigo': oficina.codigo, 'descripcion': oficina.descripcion}
            for oficina in oficinas
        ]
    except Exception as e:
        # Si hay error, usar datos de ejemplo
        oficinas_list = [
            {'codigo': '001', 'descripcion': 'Oficina Principal'},
            {'codigo': '002', 'descripcion': 'Oficina Secundaria'},
            {'codigo': '003', 'descripcion': 'Oficina Regional'},
        ]
    
    return render(request, 'miscelaneos.html', {
        'modulo': 'Tributario',
        'descripcion': 'Misceláneos',
        'empresa': empresa,
        'oficinas': oficinas_list
    })

@csrf_exempt
def buscar_actividad(request):
    """Vista AJAX para buscar actividad por empresa y código"""
    if request.method == 'GET':
        try:
            empresa = request.GET.get('empresa', '').strip()
            codigo = request.GET.get('codigo', '').strip()
            
            if not empresa or not codigo:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Empresa y código son obligatorios'
                })
            
            from tributario.models import Actividad
            try:
                actividad = Actividad.objects.get(empresa=empresa, codigo=codigo)
                return JsonResponse({
                    'exito': True,
                    'existe': True,
                    'actividad': {
                        'codigo': actividad.codigo,
                        'descripcion': actividad.descripcion
                    }
                })
            except Actividad.DoesNotExist:
                return JsonResponse({
                    'exito': True,
                    'existe': False,
                    'mensaje': 'Actividad no encontrada'
                })
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

@csrf_exempt
def cargar_actividades(request):
    """Vista AJAX para cargar actividades por empresa"""
    if request.method == 'GET':
        try:
            empresa = request.GET.get('empresa', '').strip()
            
            if not empresa:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Empresa es obligatoria'
                })
            
            from tributario.models import Actividad
            actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
            actividades_list = [
                {'codigo': act.codigo, 'descripcion': act.descripcion}
                for act in actividades
            ]
            
            return JsonResponse({
                'exito': True,
                'actividades': actividades_list
            })
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

@csrf_exempt
def buscar_concepto_miscelaneos(request):
    """Vista AJAX para buscar concepto de misceláneos"""
    if request.method == 'POST':
        try:
            empresa = request.POST.get('empresa', '').strip()
            cod_tarifa = request.POST.get('cod_tarifa', '').strip()
            
            if not empresa or not cod_tarifa:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Empresa y código de tarifa son obligatorios'
                })
            
            from tributario.models import Tarifas
            try:
                tarifa = Tarifas.objects.get(empresa=empresa, cod_tarifa=cod_tarifa)
                return JsonResponse({
                    'exito': True,
                    'concepto': {
                        'codigo': tarifa.cod_tarifa,
                        'descripcion': tarifa.descripcion,
                        'valor': str(tarifa.valor)
                    }
                })
            except Tarifas.DoesNotExist:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Concepto no encontrado'
                })
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

@csrf_exempt
def enviar_a_caja(request):
    """Vista AJAX para enviar transacción a caja e insertar en pagovariostemp"""
    if request.method == 'POST':
        try:
            from datetime import datetime
            from decimal import Decimal
            from tributario.models import PagoVariosTemp
            
            # Procesar datos del formulario
            empresa = request.POST.get('empresa', '').strip()
            fecha_str = request.POST.get('fecha', '').strip()
            dni = request.POST.get('dni', '').strip()
            nombre = request.POST.get('nombre', '').strip()
            direccion = request.POST.get('direccion', '').strip()
            comentario = request.POST.get('comentario', '').strip()
            oficina = request.POST.get('oficina', '').strip()
            
            # Validar campos obligatorios
            if not empresa or not fecha_str or not dni or not nombre:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Empresa, fecha, DNI y nombre son obligatorios'
                })
            
            # Convertir fecha
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Formato de fecha inválido. Use YYYY-MM-DD'
                })
            
            # Generar número de recibo usando la secuencia de norecibos
            from tributario.models import NoRecibos
            numero_recibo_decimal = NoRecibos.obtener_siguiente_numero()
            numero_recibo = f"REC-{numero_recibo_decimal}"
            
            # Procesar conceptos del formulario
            conceptos_procesados = []
            total_general = Decimal('0.00')
            
            # Buscar todos los conceptos en el formulario
            for key, value in request.POST.items():
                if key.startswith('form-') and key.endswith('-codigo'):
                    # Extraer el índice del concepto
                    index = key.split('-')[1]
                    
                    # Obtener todos los datos del concepto
                    codigo = request.POST.get(f'form-{index}-codigo', '').strip()
                    descripcion = request.POST.get(f'form-{index}-descripcion', '').strip()
                    cantidad = request.POST.get(f'form-{index}-cantidad', '1').strip()
                    vl_unit = request.POST.get(f'form-{index}-vl_unit', '0').strip()
                    valor = request.POST.get(f'form-{index}-valor', '0').strip()
                    
                    if codigo and valor and float(valor) > 0:
                        try:
                            cantidad_decimal = Decimal(cantidad) if cantidad else Decimal('1.00')
                            vl_unit_decimal = Decimal(vl_unit) if vl_unit else Decimal('0.00')
                            valor_decimal = Decimal(valor) if valor else Decimal('0.00')
                            
                            # Crear registro en pagovariostemp con nueva estructura
                            pago_temp = PagoVariosTemp.objects.create(
                                empresa=empresa,
                                recibo=numero_recibo_decimal,
                                codigo=codigo,
                                fecha=fecha,
                                identidad=dni,
                                nombre=nombre,
                                descripcion=descripcion,
                                valor=valor_decimal,
                                comentario=comentario,
                                oficina=oficina,
                                facturadora='',
                                aplicado='0',
                                traslado='0',
                                solvencia=0,
                                fecha_solv=None,
                                cantidad=cantidad_decimal,
                                vl_unit=vl_unit_decimal,
                                deposito=0,
                                cajero=request.session.get('usuario', ''),
                                usuario=request.session.get('usuario', ''),
                                referencia='',
                                banco='',
                                Tipofa=' ',
                                Rtm=' ',
                                expe='0',  # VARCHAR(12) según estructura real
                                pagodia=0,
                                rcaja=valor_decimal,
                                Rfechapag=fecha,
                                permiso=0,
                                Fechavence=None,
                                direccion=direccion,
                                prima='',
                                categoria='',
                                sexo='',
                                rtn=dni
                            )
                            
                            conceptos_procesados.append({
                                'codigo': codigo,
                                'descripcion': descripcion,
                                'cantidad': str(cantidad_decimal),
                                'vl_unit': str(vl_unit_decimal),
                                'valor': str(valor_decimal)
                            })
                            
                            total_general += valor_decimal
                            
                        except Exception as e:
                            return JsonResponse({
                                'exito': False,
                                'mensaje': f'Error al procesar concepto {codigo}: {str(e)}'
                            })
            
            if not conceptos_procesados:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'No se encontraron conceptos válidos para procesar'
                })
            
            return JsonResponse({
                'exito': True,
                'mensaje': f'Transacción enviada a caja exitosamente. Número de recibo: {numero_recibo}',
                'numero_recibo': numero_recibo,
                'total_general': str(total_general),
                'conceptos_procesados': len(conceptos_procesados),
                'conceptos': conceptos_procesados
            })
            
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

@csrf_exempt
def generar_soporte_transaccion(request):
    """Vista AJAX para generar soporte de transacción usando datos de pagovariostemp"""
    if request.method == 'POST':
        try:
            from tributario.models import PagoVariosTemp
            
            numero_recibo = request.POST.get('numero_recibo', '').strip()
            
            if not numero_recibo:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Número de recibo es obligatorio'
                })
            
            # Convertir número de recibo a formato numérico para búsqueda
            try:
                from decimal import Decimal
                recibo_numero = Decimal(numero_recibo.replace('REC-', ''))
            except (ValueError, TypeError):
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'Formato de número de recibo inválido: {numero_recibo}'
                })
            
            # Buscar todos los registros de pagovariostemp para este recibo
            pagos = PagoVariosTemp.objects.filter(recibo=recibo_numero).order_by('codigo')
            
            if not pagos.exists():
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'No se encontraron registros para el recibo {numero_recibo}'
                })
            
            # Obtener datos del primer registro para información general
            primer_pago = pagos.first()
            
            # Construir URL con parámetros para el soporte
            url_params = f"?fecha={primer_pago.fecha}&dni={primer_pago.identidad}&nombre={primer_pago.nombre}&direccion={primer_pago.direccion}&comentario="
            
            # Agregar conceptos a la URL
            conceptos = []
            for pago in pagos:
                concepto = f"{pago.codigo}|{pago.descripcion}|{pago.valor}"
                conceptos.append(concepto)
            
            url_params += "&" + "&".join([f"conceptos[]={concepto}" for concepto in conceptos])
            
            return JsonResponse({
                'exito': True,
                'mensaje': f'Soporte generado para recibo {numero_recibo}',
                'url_soporte': f'/tributario/soporte/{numero_recibo}/{url_params}',
                'registros_encontrados': pagos.count(),
                'total_general': str(sum(pago.valor for pago in pagos))
            })
            
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

def ver_soporte(request, numero_recibo):
    """Vista para mostrar el soporte de transacción usando datos de pagovariostemp"""
    try:
        from tributario.models import PagoVariosTemp
        from decimal import Decimal
        from django.utils import timezone
        
        # Convertir número de recibo a formato numérico para búsqueda
        try:
            numero_limpio = str(numero_recibo).strip()
            empresa_recibo = None
            if '-' in numero_limpio:
                partes = [p for p in numero_limpio.split('-') if p]
                if len(partes) >= 2:
                    empresa_recibo = partes[0]
                    numero_limpio = partes[-1]
            elif numero_limpio.upper().startswith('REC-'):
                numero_limpio = numero_limpio[4:]
            recibo_numero = Decimal(numero_limpio)
        except (ValueError, TypeError):
            return render(request, 'error.html', {
                'error': f'Formato de número de recibo inválido: {numero_recibo}',
                'modulo': 'Tributario'
            })
        
        # Buscar todos los registros de pagovariostemp para este recibo
        filtros = {'recibo': recibo_numero}
        if empresa_recibo:
            filtros['empresa'] = empresa_recibo
        pagos = PagoVariosTemp.objects.filter(**filtros).order_by('codigo')
        
        if not pagos.exists():
            return render(request, 'error.html', {
                'error': f'No se encontraron registros para el recibo {numero_recibo}',
                'modulo': 'Tributario'
            })
        
        # Obtener datos del primer registro para información general
        primer_pago = pagos.first()
        
        # Procesar conceptos desde los registros de pagovariostemp
        conceptos = []
        total_general = Decimal('0.00')
        
        for pago in pagos:
            concepto = {
                'codigo': pago.codigo,
                'rubro': pago.rubro,
                'descripcion': pago.descripcion or '',
                'valor': str(pago.valor.quantize(Decimal('0.01')) if pago.valor is not None else Decimal('0.00'))
            }
            conceptos.append(concepto)
            total_general += pago.valor
        
        # Generar QR code para el recibo
        qr_data = (
            f"Municipio: {primer_pago.empresa or ''}\n"
            f"Recibo: {numero_recibo}\n"
            f"RTM: {(primer_pago.Rtm or '').strip()}\n"
            f"Expediente: {primer_pago.expe}\n"
            f"Contribuyente: {primer_pago.nombre or ''}\n"
            f"Total: L. {total_general:.2f}\n"
            f"Fecha: {primer_pago.fecha}"
        )
        import qrcode
        import io
        import base64
        from qrcode.image.svg import SvgPathImage

        qr_img = qrcode.make(qr_data, image_factory=SvgPathImage, box_size=8, border=2)
        buffer = io.BytesIO()
        qr_img.save(buffer)
        qr_svg_b64 = base64.b64encode(buffer.getvalue()).decode()
        qr_data_uri = f"data:image/svg+xml;base64,{qr_svg_b64}"
        
        return render(request, 'soporte_simple.html', {
            'numero_recibo': numero_recibo,
            'fecha': primer_pago.fecha,
             'hora_actual': timezone.now().strftime('%H:%M:%S'),
            'dni': primer_pago.identidad,
            'nombre': primer_pago.nombre,
            'negocio_nombre': (primer_pago.facturadora or '').strip(),
            'direccion': primer_pago.direccion,
            'rtm': (primer_pago.Rtm or '').strip(),
            'expe': primer_pago.expe,
            'recibo_banco': request.GET.get('recibo_banco', ''),
            'comentario': (primer_pago.comentario or '').strip(),
            'usuario': (primer_pago.usuario or '').strip() or 'SISTEMA',
            'cajero': (primer_pago.cajero or '').strip() or 'N/A',
            'conceptos': conceptos,
            'total_general': total_general.quantize(Decimal('0.01')) if total_general else Decimal('0.00'),
            'qr_code': '',
            'qr_data_uri': qr_data_uri,
            'modulo': 'Tributario',
            'descripcion': 'Soporte de Transacción'
        })
        
    except Exception as e:
        return render(request, 'error.html', {
            'error': f'Error al generar soporte: {str(e)}',
            'modulo': 'Tributario'
        })

@csrf_exempt
def buscar_oficina_ajax(request):
    """Vista AJAX para buscar oficina por empresa y código"""
    if request.method == 'GET':
        try:
            empresa = request.GET.get('empresa', '').strip()
            codigo = request.GET.get('codigo', '').strip()
            
            print(f"🔍 Buscando oficina: empresa={empresa}, codigo={codigo}")
            
            if not empresa or not codigo:
                return JsonResponse({
                    'exito': False,
                    'existe': False,
                    'descripcion': '',
                    'mensaje': 'Empresa y código son obligatorios'
                })
            
            # Buscar en la tabla oficina
            try:
                from tributario.models import Oficina
                oficina = Oficina.objects.get(empresa=empresa, codigo=codigo)
                
                return JsonResponse({
                    'exito': True,
                    'existe': True,
                    'descripcion': oficina.descripcion or '',
                    'mensaje': 'Oficina encontrada'
                })
            except Oficina.DoesNotExist:
                return JsonResponse({
                    'exito': True,
                    'existe': False,
                    'descripcion': '',
                    'mensaje': 'Oficina no encontrada'
                })
            except Exception as e:
                print(f"❌ Error en búsqueda de oficina: {e}")
                return JsonResponse({
                    'exito': False,
                    'existe': False,
                    'descripcion': '',
                    'mensaje': f'Error en la búsqueda: {str(e)}'
                })
        except Exception as e:
            print(f"❌ Error general en buscar_oficina_ajax: {e}")
            return JsonResponse({
                'exito': False,
                'existe': False,
                'descripcion': '',
                'mensaje': f'Error interno: {str(e)}'
            })
    else:
        return JsonResponse({
            'exito': False,
            'existe': False,
            'descripcion': '',
            'mensaje': 'Método no permitido'
        })


@csrf_exempt
def buscar_negocios_listado(request):
    """Vista AJAX para buscar negocios con múltiples criterios para el modal de búsqueda"""
    from django.http import JsonResponse
    try:
        from django.db.models import Q
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


def buscar_negocios_pagina(request):
    """Vista para página separada de búsqueda de negocios"""
    from django.db.models import Q
    from tributario.models import Negocio
    from django.contrib import messages
    
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
            negocios = negocios.filter(identidad__icontains=criterio_busqueda)
        elif tipo_busqueda == 'comerciante':
            negocios = negocios.filter(comerciante__icontains=criterio_busqueda)
        elif tipo_busqueda == 'nombre':
            negocios = negocios.filter(nombrenego__icontains=criterio_busqueda)
        elif tipo_busqueda == 'direccion':
            negocios = negocios.filter(direccion__icontains=criterio_busqueda)
        elif tipo_busqueda == 'rtm':
            negocios = negocios.filter(rtm__icontains=criterio_busqueda)
        elif tipo_busqueda == 'expe':
            negocios = negocios.filter(expe__icontains=criterio_busqueda)
    
    # Limitar resultados a 200
    negocios = negocios.order_by('nombrenego', 'comerciante')[:200]
    
    context = {
        'empresa': empresa_filtro,
        'municipio_codigo': empresa_filtro,
        'negocios': negocios,
        'criterio_busqueda': criterio_busqueda,
        'tipo_busqueda': tipo_busqueda,
        'total': negocios.count(),
        'modulo': 'Tributario',
        'descripcion': 'Búsqueda de Negocios'
    }
    
    return render(request, 'buscar_negocios.html', context)


@csrf_exempt
def calcular_transaccion_pago(request):
    """Vista AJAX para calcular transacción de pago desde lo más antiguo hasta lo más reciente"""
    from django.http import JsonResponse
    from django.db.models import Q
    from tributario.models import TransaccionesIcs, Rubro, ParametrosTributarios
    from decimal import Decimal
    from datetime import datetime
    import logging
    import calendar
    from datetime import date
    
    logger = logging.getLogger(__name__)
    
    try:
        empresa = request.GET.get('empresa', '').strip()
        rtm = request.GET.get('rtm', '').strip()
        expe = request.GET.get('expe', '').strip()
        tipo = request.GET.get('tipo', 'cuota').strip()
        
        logger.info(f"🔍 calcular_transaccion_pago - empresa={empresa}, rtm={rtm}, expe={expe}, tipo={tipo}")
        
        if not empresa or not rtm or not expe:
            logger.warning(f"❌ Parámetros faltantes - empresa={empresa}, rtm={rtm}, expe={expe}")
            return JsonResponse({
                'exito': False,
                'mensaje': 'Empresa, RTM y Expediente son obligatorios'
            }, status=400)
        
        # Obtener todas las transacciones pendientes
        # Solo transacciones con monto > 0 (pendientes de pago)
        # NO se filtra por operacion - se toman todas las transacciones con saldo pendiente
        # Según la tabla transaccionesics: cada combinación única de (empresa, rtm, expe, ano, mes, rubro) es una transacción
        # Ordenadas por año, mes, rubro (más antiguo primero)
        from django.db.models import Q
        transacciones_pendientes = TransaccionesIcs.objects.filter(
            empresa=empresa,
            rtm=rtm,
            expe=expe,
            monto__gt=0  # Solo transacciones con saldo pendiente > 0
        ).order_by('ano', 'mes', 'rubro')
        
        total_pendientes = transacciones_pendientes.count()
        logger.info(f"📊 Transacciones pendientes encontradas: {total_pendientes}")
        
        if not transacciones_pendientes.exists():
            # Verificar si hay transacciones sin filtro de monto
            todas = TransaccionesIcs.objects.filter(
                empresa=empresa,
                rtm=rtm,
                expe=expe
            )
            logger.warning(f"⚠️ No hay transacciones con monto > 0. Total transacciones: {todas.count()}")
            
            if todas.exists():
                logger.info(f"   Primeras 3 transacciones (sin filtro monto):")
                for t in todas[:3]:
                    logger.info(f"      Año: {t.ano}, Mes: {t.mes}, Rubro: {t.rubro}, Monto: {t.monto}, Operacion: {t.operacion}")
            
            # Mensaje informativo
            mensaje = f'No hay transacciones pendientes de pago para este negocio.\n\n'
            mensaje += f'Filtro aplicado: monto > 0 (solo saldo pendiente)\n\n'
            
            if todas.exists():
                mensaje += f'Total transacciones en la base de datos: {todas.count()}\n'
                mensaje += f'\nLas transacciones encontradas tienen monto = 0 o negativo (ya pagadas o sin saldo pendiente).\n\n'
                mensaje += f'Para generar un recibo, se necesitan transacciones con monto > 0.'
            else:
                mensaje += f'No se encontraron transacciones en la base de datos para este negocio.\n\n'
                mensaje += f'Verifique:\n'
                mensaje += f'1. Que el negocio tenga RTM y EXPE correctos\n'
                mensaje += f'2. Que existan declaraciones generadas\n'
                mensaje += f'3. Que las declaraciones hayan creado transacciones en la tabla transaccionesics'
            
            return JsonResponse({
                'exito': False,
                'mensaje': mensaje
            })
        
        # Convertir a lista para trabajar con ella
        transacciones_lista = list(transacciones_pendientes)
        
        # Agrupar transacciones por periodo (año-mes) - cada periodo es una cuota
        # Según la tabla: cada combinación única de (empresa, rtm, expe, ano, mes) = 1 CUOTA
        # Dentro de cada cuota (mes) hay varios rubros, cada rubro es una transacción única
        # En la tabla: ano es DECIMAL(4,0), mes es CHAR(2)
        periodos = {}
        for trans in transacciones_lista:
            # Obtener año (DECIMAL(4,0) -> int)
            ano = int(float(trans.ano)) if trans.ano else 0
            # Obtener mes (CHAR(2) -> string normalizado)
            mes_str = str(trans.mes).strip() if trans.mes else ''
            # Normalizar mes a 2 dígitos (rellenar con cero a la izquierda si es numérico)
            if mes_str.isdigit():
                mes_normalizado = mes_str.zfill(2)
            else:
                mes_normalizado = mes_str.zfill(2) if mes_str else '00'
            
            # Clave de periodo: (empresa, rtm, expe, ano, mes) = 1 cuota
            periodo_key = f"{ano}-{mes_normalizado}"
            
            if periodo_key not in periodos:
                periodos[periodo_key] = {
                    'ano': ano,
                    'mes': mes_normalizado,
                    'transacciones': []  # Todas las transacciones (rubros) de este mes (cuota)
                }
            periodos[periodo_key]['transacciones'].append(trans)
        
        # Ordenar periodos por fecha (más antiguo primero): primero por año, luego por mes numéricamente
        def ordenar_periodo(item):
            periodo_data = item[1]
            ano = periodo_data['ano']
            mes_str = periodo_data['mes']
            # Convertir mes a número para ordenar correctamente (01, 02, ..., 12)
            mes_num = int(mes_str) if mes_str.isdigit() else 0
            return (ano, mes_num)
        
        periodos_ordenados = sorted(periodos.items(), key=ordenar_periodo)
        
        # Determinar qué periodos (cuotas/meses) incluir
        transacciones_a_pagar = []
        periodos_a_pagar = []  # Inicializar variable
        
        if tipo == 'cuota':
            cuota_hasta = int(request.GET.get('cuota_hasta', 1))
            if cuota_hasta < 1:
                cuota_hasta = 1
            
            # Tomar los primeros N periodos (cada periodo = 1 cuota = 1 mes)
            # Cada periodo incluye TODOS los rubros de ese mes
            periodos_a_pagar = periodos_ordenados[:cuota_hasta]
            
            # Incluir TODAS las transacciones (todos los rubros) de los periodos seleccionados
            for periodo_key, periodo_data in periodos_a_pagar:
                # Agregar todas las transacciones de este periodo (mes/cuota)
                # Esto incluye todos los rubros del mes
                for trans in periodo_data['transacciones']:
                    transacciones_a_pagar.append(trans)
        else:  # parcial
            monto_abono = Decimal(str(request.GET.get('monto', '0')))
            monto_restante = monto_abono
            
            # Recorrer periodos en orden (de más antiguo a más reciente)
            for periodo_key, periodo_data in periodos_ordenados:
                if monto_restante <= 0:
                    break
                
                # Calcular el saldo total del periodo (suma de todas las transacciones del mes)
                saldo_periodo = Decimal('0')
                for trans in periodo_data['transacciones']:
                    saldo_pendiente = Decimal(str(trans.monto)) if trans.monto and trans.monto > 0 else Decimal('0')
                    if saldo_pendiente > 0:
                        saldo_periodo += saldo_pendiente
                
                if saldo_periodo > 0:
                    # Si el monto restante cubre todo el periodo, incluir todas las transacciones
                    if monto_restante >= saldo_periodo:
                        # Incluir todas las transacciones del periodo
                        for trans in periodo_data['transacciones']:
                            saldo_pendiente = Decimal(str(trans.monto)) if trans.monto and trans.monto > 0 else Decimal('0')
                            if saldo_pendiente > 0:
                                transacciones_a_pagar.append({
                                    'transaccion': trans,
                                    'monto_a_aplicar': saldo_pendiente
                                })
                        monto_restante -= saldo_periodo
                    else:
                        # Solo cubre parcialmente el periodo - aplicar proporcionalmente
                        # Aplicar desde las transacciones más antiguas del periodo
                        for trans in periodo_data['transacciones']:
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
        
        # Importar modelos necesarios
        from tributario.models import TasasDecla, Actividad, Negocio
        
        # Obtener datos del negocio para el encabezado
        negocio = Negocio.objects.filter(empresa=empresa, rtm=rtm, expe=expe).first()
        
        # Caches para reducir consultas repetidas
        tasas_cache = {}
        rubros_cache = {}
        actividades_cache = {}

        pago_fecha = date.today()

        # Desglose mora/base por año (control de abonos a periodos antiguos)
        # Regla:
        # - Mora: rubros que inician con R* (recargos) o I* (intereses)
        # - Año actual vs anteriores: por (trans.ano) respecto a pago_fecha.year
        breakdown = {
            'anio_referencia': int(pago_fecha.year),
            'base_actual': Decimal('0.00'),
            'base_anteriores': Decimal('0.00'),
            'mora_actual': Decimal('0.00'),
            'mora_anteriores': Decimal('0.00'),
        }

        # ── Helpers PA (Pago Anual) ──────────────────────────────────────────
        def _last_day_of_month(y: int, m: int) -> int:
            return calendar.monthrange(y, m)[1]

        def _vencimiento_periodo(y: int, m: int) -> date:
            # En ICS asumimos vencimiento al último día del mes
            return date(y, m, _last_day_of_month(y, m))

        def _subtract_months(d: date, months: int) -> date:
            # Restar meses preservando día dentro del mes destino
            y = d.year
            m = d.month - int(months or 0)
            while m <= 0:
                m += 12
                y -= 1
            day = min(d.day, _last_day_of_month(y, m))
            return date(y, m, day)

        pa_cache = {}  # ano -> (pct, meses_ant)
        
        # Agrupación por rubro con información de cuenta y descripción
        agrupado_por_rubro = {}
        periodos_globales = set()
        transacciones_detalle = []
        
        for item in transacciones_a_pagar:
            if tipo == 'cuota':
                trans = item
                monto = Decimal(str(trans.monto)) if trans.monto and trans.monto > 0 else Decimal('0')
            else:
                trans = item['transaccion']
                monto = Decimal(str(item['monto_a_aplicar'])) if item['monto_a_aplicar'] else Decimal('0')
            
            rubro_codigo = (trans.rubro or '').strip() or 'SIN_RUBRO'

            try:
                ano_trans = int(float(trans.ano)) if trans.ano is not None else None
            except (TypeError, ValueError):
                ano_trans = None

            mes_raw = str(trans.mes).strip() if getattr(trans, 'mes', None) else ''
            try:
                mes_trans = int(mes_raw)
            except (TypeError, ValueError):
                mes_trans = None

            rubro_norm_all = str(rubro_codigo).strip().upper()
            es_mora = rubro_norm_all.startswith('R') or rubro_norm_all.startswith('I')
            try:
                es_actual = int(ano_trans or 0) == int(pago_fecha.year)
            except Exception:
                es_actual = False
            if monto > 0:
                if es_mora:
                    breakdown['mora_actual' if es_actual else 'mora_anteriores'] += monto
                else:
                    breakdown['base_actual' if es_actual else 'base_anteriores'] += monto

            if ano_trans and mes_trans:
                periodos_globales.add((ano_trans, mes_trans))

            # Descuento PA por vencimiento (anticipación meses_anticipacion, por ley 4)
            dpa_monto = Decimal('0.00')
            dpa_pct = Decimal('0.00')
            try:
                if ano_trans and mes_trans and monto > 0:
                    if ano_trans not in pa_cache:
                        param_pa = ParametrosTributarios.obtener_parametro('PA', empresa, ano_trans, fecha_consulta=pago_fecha)
                        if not param_pa:
                            try:
                                ParametrosTributarios.objects.get_or_create(
                                    empresa='GLOB',
                                    tipo_parametro='PA',
                                    ano_vigencia=ano_trans,
                                    defaults={
                                        'descripcion': f'Descuento Pago Anual (Ley) — 10% (Año {ano_trans})',
                                        'porcentaje_descuento_anual': Decimal('10.00'),
                                        'meses_anticipacion': 4,
                                        'activo': True,
                                    }
                                )
                            except Exception:
                                pass
                            param_pa = ParametrosTributarios.obtener_parametro('PA', empresa, ano_trans, fecha_consulta=pago_fecha)

                        pct = Decimal(str(getattr(param_pa, 'porcentaje_descuento_anual', 0) or 0))
                        meses_ant = int(getattr(param_pa, 'meses_anticipacion', 0) or 0)
                        pa_cache[ano_trans] = (pct, meses_ant)

                    dpa_pct, meses_ant = pa_cache.get(ano_trans, (Decimal('0.00'), 0))
                    if dpa_pct > 0 and meses_ant >= 0:
                        venc = _vencimiento_periodo(ano_trans, mes_trans)
                        limite = _subtract_months(venc, meses_ant)
                        if pago_fecha <= limite:
                            dpa_monto = (monto * (dpa_pct / Decimal('100.00'))).quantize(Decimal('0.01'))
            except Exception:
                dpa_monto = Decimal('0.00')
                dpa_pct = Decimal('0.00')
            
            # Obtener cuenta desde TasasDecla o Rubro
            cuenta = ''
            tasa_cache_key = (rubro_codigo, ano_trans)
            if tasa_cache_key in tasas_cache:
                cuenta = tasas_cache[tasa_cache_key]
            else:
                cuenta_qs = TasasDecla.objects.filter(
                    empresa=empresa,
                    rtm=rtm,
                    expe=expe,
                    rubro=rubro_codigo
                )
                if ano_trans is not None:
                    cuenta_qs = cuenta_qs.filter(ano=ano_trans)
                tasa_obj = cuenta_qs.only('cuenta').first()
                cuenta = (tasa_obj.cuenta or '').strip() if tasa_obj and tasa_obj.cuenta else ''
                tasas_cache[tasa_cache_key] = cuenta
            
            rubro_info = rubros_cache.get(rubro_codigo)
            if rubro_info is None:
                rubro_obj = Rubro.objects.filter(empresa=empresa, codigo=rubro_codigo).only('descripcion', 'cuenta').first()
                if rubro_obj:
                    rubro_info = {
                        'descripcion': (rubro_obj.descripcion or '').strip(),
                        'cuenta': (rubro_obj.cuenta or '').strip()
                    }
                else:
                    rubro_info = {'descripcion': '', 'cuenta': ''}
                rubros_cache[rubro_codigo] = rubro_info
            
            if not cuenta:
                cuenta = rubro_info.get('cuenta') or ''
            
            if not cuenta:
                cuenta = 'SIN_CUENTA'
            
            descripcion = ''
            if cuenta in actividades_cache:
                descripcion = actividades_cache[cuenta]
            else:
                actividad_obj = Actividad.objects.filter(empresa=empresa, codigo=cuenta).only('descripcion').first()
                descripcion = (actividad_obj.descripcion or '').strip() if actividad_obj and actividad_obj.descripcion else ''
                actividades_cache[cuenta] = descripcion
            
            if not descripcion:
                descripcion = rubro_info.get('descripcion') or ''
            
            if not descripcion:
                descripcion = f'Rubro {rubro_codigo}'
            
            if rubro_codigo not in agrupado_por_rubro:
                agrupado_por_rubro[rubro_codigo] = {
                    'rubro': rubro_codigo,
                    'cuenta': cuenta,
                    'descripcion': descripcion,
                    'valor': Decimal('0'),
                    'periodos': set()
                }
            else:
                if not agrupado_por_rubro[rubro_codigo]['cuenta'] and cuenta:
                    agrupado_por_rubro[rubro_codigo]['cuenta'] = cuenta
                if agrupado_por_rubro[rubro_codigo]['descripcion'] in ('', f'Rubro {rubro_codigo}') and descripcion:
                    agrupado_por_rubro[rubro_codigo]['descripcion'] = descripcion
            
            monto_base = monto
            monto_neto = monto_base
            if dpa_monto > 0:
                monto_neto = (monto_base - dpa_monto).quantize(Decimal('0.01'))
            agrupado_por_rubro[rubro_codigo]['valor'] += monto_neto
            
            if ano_trans and mes_trans:
                agrupado_por_rubro[rubro_codigo]['periodos'].add((ano_trans, mes_trans))
            
            transacciones_detalle.append({
                'rubro': rubro_codigo if rubro_codigo != 'SIN_RUBRO' else '',
                'cuenta': cuenta,
                'descripcion': descripcion,
                'ano': ano_trans or '',
                'mes': mes_trans or '',
                'monto': float(monto_base)
            })
            if dpa_monto > 0:
                transacciones_detalle.append({
                    'rubro': rubro_codigo if rubro_codigo != 'SIN_RUBRO' else '',
                    'cuenta': cuenta,
                    'descripcion': f"Descuento pago anual ({dpa_pct}%)",
                    'ano': ano_trans or '',
                    'mes': mes_trans or '',
                    'monto': float(-dpa_monto)
                })
        
        transacciones_rubro_list = []
        total_valor_decimal = Decimal('0')
        for rubro_codigo, datos in agrupado_por_rubro.items():
            total_valor_decimal += datos['valor']
            transacciones_rubro_list.append({
                'rubro': rubro_codigo,
                'cuenta': datos['cuenta'],
                'descripcion': datos['descripcion'],
                'valor': float(datos['valor']),
                'periodos': [
                    {'ano': periodo[0], 'mes': periodo[1]}
                    for periodo in sorted(datos['periodos'])
                ]
            })
        
        transacciones_rubro_list.sort(key=lambda item: item['rubro'])
        
        periodos_info = [
            {'ano': ano, 'mes': mes}
            for ano, mes in sorted(periodos_globales)
        ]
        
        total_periodos = len(periodos_globales)
        periodos_seleccionados_count = len(periodos_a_pagar) if tipo == 'cuota' else None
        total_transacciones = len(transacciones_a_pagar)
        total_valor = float(total_valor_decimal)
        
        datos_negocio = {
            'rtm': rtm,
            'expe': expe,
            'comerciante': negocio.comerciante if negocio else '',
            'nombre_negocio': negocio.nombrenego if negocio else '',
            'direccion': negocio.direccion if negocio else '',
            'empresa': empresa
        }
        
        logger.info(f"✅ Respuesta generada - Rubros: {len(transacciones_rubro_list)}, Total: L. {total_valor:.2f}")
        
        return JsonResponse({
            'exito': True,
            'transacciones_por_rubro': transacciones_rubro_list,
            'transacciones_detalle': transacciones_detalle,
            'total_transacciones': total_transacciones,
            'total_rubros': len(transacciones_rubro_list),
            'total_periodos': total_periodos,
            'periodos_seleccionados': periodos_seleccionados_count,
            'periodos_info': periodos_info,
            'desglose_mora': {
                'anio_referencia': breakdown['anio_referencia'],
                'base_actual': float(breakdown['base_actual']),
                'base_anteriores': float(breakdown['base_anteriores']),
                'mora_actual': float(breakdown['mora_actual']),
                'mora_anteriores': float(breakdown['mora_anteriores']),
            },
            'total_valor': total_valor,
            'datos_negocio': datos_negocio
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"❌ Error en calcular_transaccion_pago: {str(e)}")
        logger.error(f"   Traceback: {error_trace}")
        traceback.print_exc()
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al calcular transacción: {str(e)}'
        }, status=500)


@csrf_exempt
def guardar_transaccion_pago(request):
    """Vista AJAX para guardar transacción de pago que puede ser cobrada en módulo de caja"""
    from django.http import JsonResponse
    from tributario.models import TransaccionesIcs, Rubro, TasasDecla, Actividad, NoRecibos, PagoVariosTemp, ParametrosTributarios
    from decimal import Decimal
    from django.utils import timezone
    from django.db import transaction
    from django.urls import reverse
    import json
    import calendar
    from datetime import date
    
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
        comentario = (data.get('comentario') or '').strip()
        if len(comentario) > 500:
            comentario = comentario[:500]
        
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
        
        # Obtener transacciones pendientes ordenadas por año, mes, rubro
        # NO se filtra por operacion - se toman todas las transacciones con saldo pendiente
        # Según la tabla transaccionesics: cada combinación única de (empresa, rtm, expe, ano, mes, rubro) es una transacción
        transacciones_pendientes = TransaccionesIcs.objects.filter(
            empresa=empresa,
            rtm=rtm,
            expe=expe,
            monto__gt=0  # Solo transacciones con saldo pendiente > 0
        ).order_by('ano', 'mes', 'rubro')
        
        transacciones_lista = list(transacciones_pendientes)
        
        # Agrupar transacciones por periodo (año-mes) - cada periodo es una cuota
        # Según la tabla: cada combinación única de (empresa, rtm, expe, ano, mes) = 1 CUOTA
        # Dentro de cada cuota (mes) hay varios rubros, cada rubro es una transacción única
        # En la tabla: ano es DECIMAL(4,0), mes es CHAR(2)
        periodos = {}
        for trans in transacciones_lista:
            ano = int(float(trans.ano)) if trans.ano else 0
            mes_str = str(trans.mes).strip() if trans.mes else ''
            if mes_str.isdigit():
                mes_normalizado = mes_str.zfill(2)
            else:
                mes_normalizado = mes_str.zfill(2) if mes_str else '00'
            
            # Clave de periodo: (empresa, rtm, expe, ano, mes) = 1 cuota
            periodo_key = f"{ano}-{mes_normalizado}"
            
            if periodo_key not in periodos:
                periodos[periodo_key] = {
                    'ano': ano,
                    'mes': mes_normalizado,
                    'transacciones': []  # Todas las transacciones (rubros) de este mes (cuota)
                }
            periodos[periodo_key]['transacciones'].append(trans)
        
        # Ordenar periodos por fecha (más antiguo primero)
        def ordenar_periodo(item):
            periodo_data = item[1]
            ano = periodo_data['ano']
            mes_str = periodo_data['mes']
            mes_num = int(mes_str) if mes_str.isdigit() else 0
            return (ano, mes_num)
        
        periodos_ordenados = sorted(periodos.items(), key=ordenar_periodo)
        
        # Determinar qué transacciones pagar
        transacciones_a_pagar = []
        periodos_a_pagar = []
        
        if tipo == 'cuota':
            cuota_hasta = int(data.get('cuota_hasta', 1))
            if cuota_hasta < 1:
                cuota_hasta = 1
            
            # Tomar los primeros N periodos (cada periodo = 1 cuota = 1 mes)
            # Cada periodo incluye TODOS los rubros de ese mes
            periodos_a_pagar = periodos_ordenados[:cuota_hasta]
            
            # Incluir TODAS las transacciones (todos los rubros) de los periodos seleccionados
            for periodo_key, periodo_data in periodos_a_pagar:
                # Agregar todas las transacciones de este periodo (mes/cuota)
                # Esto incluye todos los rubros del mes
                for trans in periodo_data['transacciones']:
                    transacciones_a_pagar.append(trans)
        else:
            monto_abono = Decimal(str(data.get('monto', '0')))
            monto_restante = monto_abono
            
            # Recorrer periodos en orden (de más antiguo a más reciente)
            for periodo_key, periodo_data in periodos_ordenados:
                if monto_restante <= 0:
                    break
                
                # Calcular el saldo total del periodo (suma de todas las transacciones del mes)
                saldo_periodo = Decimal('0')
                for trans in periodo_data['transacciones']:
                    saldo_pendiente = Decimal(str(trans.monto)) if trans.monto and trans.monto > 0 else Decimal('0')
                    if saldo_pendiente > 0:
                        saldo_periodo += saldo_pendiente
                
                if saldo_periodo > 0:
                    # Si el monto restante cubre todo el periodo, incluir todas las transacciones
                    if monto_restante >= saldo_periodo:
                        for trans in periodo_data['transacciones']:
                            saldo_pendiente = Decimal(str(trans.monto)) if trans.monto and trans.monto > 0 else Decimal('0')
                            if saldo_pendiente > 0:
                                transacciones_a_pagar.append({
                                    'transaccion': trans,
                                    'monto_a_aplicar': saldo_pendiente
                                })
                        monto_restante -= saldo_periodo
                    else:
                        # Solo cubre parcialmente el periodo - aplicar proporcionalmente
                        for trans in periodo_data['transacciones']:
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
        
        if not transacciones_a_pagar:
            return JsonResponse({
                'exito': False,
                'mensaje': 'No se encontraron transacciones pendientes para generar el pago.'
            }, status=400)
        
        fecha_emision = timezone.now()

        # ── Helpers PA (Pago Anual) ──────────────────────────────────────────
        def _last_day_of_month(y: int, m: int) -> int:
            return calendar.monthrange(y, m)[1]

        def _vencimiento_periodo(y: int, m: int) -> date:
            # En ICS asumimos vencimiento al último día del mes
            return date(y, m, _last_day_of_month(y, m))

        def _subtract_months(d: date, months: int) -> date:
            y = d.year
            m = d.month - int(months or 0)
            while m <= 0:
                m += 12
                y -= 1
            day = min(d.day, _last_day_of_month(y, m))
            return date(y, m, day)

        pago_fecha = fecha_emision.date()
        pa_cache = {}  # ano -> (pct, meses_ant)

        breakdown = {
            'anio_referencia': int(pago_fecha.year),
            'base_actual': Decimal('0.00'),
            'base_anteriores': Decimal('0.00'),
            'mora_actual': Decimal('0.00'),
            'mora_anteriores': Decimal('0.00'),
        }
        
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

            rubro_norm_all = str(rubro or '').strip().upper()
            es_mora = rubro_norm_all.startswith('R') or rubro_norm_all.startswith('I')
            try:
                es_actual = int(ano_trans or 0) == int(pago_fecha.year)
            except Exception:
                es_actual = False
            if monto_pago and monto_pago > 0:
                if es_mora:
                    breakdown['mora_actual' if es_actual else 'mora_anteriores'] += Decimal(str(monto_pago))
                else:
                    breakdown['base_actual' if es_actual else 'base_anteriores'] += Decimal(str(monto_pago))

            # Descuento PA por vencimiento (anticipación meses_anticipacion, por ley 4)
            dpa_monto = Decimal('0.00')
            dpa_pct = Decimal('0.00')
            try:
                if ano_trans and mes_trans and monto_pago > 0:
                    if ano_trans not in pa_cache:
                        param_pa = ParametrosTributarios.obtener_parametro('PA', empresa, ano_trans, fecha_consulta=pago_fecha)
                        if not param_pa:
                            try:
                                ParametrosTributarios.objects.get_or_create(
                                    empresa='GLOB',
                                    tipo_parametro='PA',
                                    ano_vigencia=ano_trans,
                                    defaults={
                                        'descripcion': f'Descuento Pago Anual (Ley) — 10% (Año {ano_trans})',
                                        'porcentaje_descuento_anual': Decimal('10.00'),
                                        'meses_anticipacion': 4,
                                        'activo': True,
                                    }
                                )
                            except Exception:
                                pass
                            param_pa = ParametrosTributarios.obtener_parametro('PA', empresa, ano_trans, fecha_consulta=pago_fecha)

                        pct = Decimal(str(getattr(param_pa, 'porcentaje_descuento_anual', 0) or 0))
                        meses_ant = int(getattr(param_pa, 'meses_anticipacion', 0) or 0)
                        pa_cache[ano_trans] = (pct, meses_ant)

                    dpa_pct, meses_ant = pa_cache.get(ano_trans, (Decimal('0.00'), 0))
                    if dpa_pct > 0 and meses_ant >= 0:
                        venc = _vencimiento_periodo(ano_trans, mes_trans)
                        limite = _subtract_months(venc, meses_ant)
                        if pago_fecha <= limite:
                            dpa_monto = (monto_pago * (dpa_pct / Decimal('100.00'))).quantize(Decimal('0.01'))
            except Exception:
                dpa_monto = Decimal('0.00')
                dpa_pct = Decimal('0.00')
            
            if rubro not in pagos_por_rubro:
                pagos_por_rubro[rubro] = {
                    'montos': [],
                    'anos': [],
                    'meses': [],
                    'transacciones': [],
                    'descuento_pa_total': Decimal('0.00'),
                    'descuento_pa_pct': None,
                }
            
            pagos_por_rubro[rubro]['montos'].append(monto_pago)
            pagos_por_rubro[rubro]['anos'].append(ano_trans)
            pagos_por_rubro[rubro]['meses'].append(mes_trans)
            pagos_por_rubro[rubro]['transacciones'].append(trans_original)
            if dpa_monto > 0:
                pagos_por_rubro[rubro]['descuento_pa_total'] += dpa_monto
                if pagos_por_rubro[rubro].get('descuento_pa_pct') is None and dpa_pct > 0:
                    pagos_por_rubro[rubro]['descuento_pa_pct'] = dpa_pct
        
        # Crear rangos de pago agrupados por rubro
        rangos_info = []
        
        tasas_cache = {}
        rubros_cache = {}
        actividades_cache = {}
        
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
                try:
                    descuento_pa_rubro = (datos.get('descuento_pa_total') or Decimal('0.00'))
                except Exception:
                    descuento_pa_rubro = Decimal('0.00')
                monto_total_neto_rubro = (monto_total_rubro - descuento_pa_rubro).quantize(Decimal('0.01'))
                
                # Formatear rango de meses para nodeclara: "ANO-MES|ANO-MES"
                # Ejemplo: "2024-01|2024-03" significa desde enero 2024 hasta marzo 2024
                mes_desde_str = str(mes_desde).zfill(2)
                mes_hasta_str = str(mes_hasta).zfill(2)
                rango_meses = f"{ano_desde}-{mes_desde_str}|{ano_hasta}-{mes_hasta_str}"
                
                # Usar el año y mes del periodo más reciente para la transacción de pago
                ano_pago = ano_hasta
                mes_pago = mes_hasta_str
                
                datos['monto_total'] = monto_total_rubro
                datos['monto_total_neto'] = monto_total_neto_rubro
                datos['rango'] = {
                    'ano_desde': ano_desde,
                    'mes_desde': mes_desde,
                    'ano_hasta': ano_hasta,
                    'mes_hasta': mes_hasta,
                    'texto': rango_meses
                }
                
                # Guardar información del rango
                rangos_info.append({
                    'rubro': rubro,
                    'ano_desde': ano_desde,
                    'mes_desde': mes_desde,
                    'ano_hasta': ano_hasta,
                    'mes_hasta': mes_hasta,
                    'monto': float(monto_total_neto_rubro),
                    'rango_str': rango_meses
                })
        
        total_base = sum((datos.get('monto_total') or Decimal('0')) for datos in pagos_por_rubro.values())
        total_desc_pa = sum((datos.get('descuento_pa_total') or Decimal('0.00')) for datos in pagos_por_rubro.values())
        total_pagado_decimal = (total_base - total_desc_pa).quantize(Decimal('0.01'))
        
        # Preparar desglose para el recibo
        detalle_recibo = []
        for rubro, datos in pagos_por_rubro.items():
            monto_total_rubro = datos.get('monto_total') or Decimal('0')
            
            # Obtener cuenta desde TasasDecla priorizando el año más reciente
            cuenta = ''
            anos_validos = [ano for ano in datos['anos'] if ano]
            for ano_candidato in sorted(set(anos_validos), reverse=True):
                cache_key = (rubro, ano_candidato)
                if cache_key in tasas_cache:
                    cuenta = tasas_cache[cache_key]
                else:
                    tasa_obj = TasasDecla.objects.filter(
                        empresa=empresa,
                        rtm=rtm,
                        expe=expe,
                        rubro=rubro,
                        ano=ano_candidato
                    ).only('cuenta').first()
                    cuenta = (tasa_obj.cuenta or '').strip() if tasa_obj and tasa_obj.cuenta else ''
                    tasas_cache[cache_key] = cuenta
                
                if cuenta:
                    break
            
            rubro_info = rubros_cache.get(rubro)
            if rubro_info is None:
                rubro_obj = Rubro.objects.filter(empresa=empresa, codigo=rubro).only('descripcion', 'cuenta').first()
                rubro_info = {
                    'descripcion': (rubro_obj.descripcion or '').strip() if rubro_obj and rubro_obj.descripcion else '',
                    'cuenta': (rubro_obj.cuenta or '').strip() if rubro_obj and rubro_obj.cuenta else ''
                }
                rubros_cache[rubro] = rubro_info
            
            if not cuenta:
                cuenta = rubro_info.get('cuenta') or ''
            
            descripcion = ''
            if cuenta:
                if cuenta in actividades_cache:
                    descripcion = actividades_cache[cuenta]
                else:
                    actividad_obj = Actividad.objects.filter(empresa=empresa, codigo=cuenta).only('descripcion').first()
                    descripcion = (actividad_obj.descripcion or '').strip() if actividad_obj and actividad_obj.descripcion else ''
                    actividades_cache[cuenta] = descripcion
            
            if not descripcion:
                descripcion = rubro_info.get('descripcion') or ''
            
            if not descripcion:
                descripcion = f'Rubro {rubro}'
            
            rango = datos.get('rango') or {}
            if rango.get('ano_desde') and rango.get('mes_desde') and rango.get('ano_hasta') and rango.get('mes_hasta'):
                periodo_texto = f"{int(rango['mes_desde']):02d}/{int(rango['ano_desde'])} - {int(rango['mes_hasta']):02d}/{int(rango['ano_hasta'])}"
            else:
                periodo_texto = 'Sin periodo asociado'
            
            detalle_recibo.append({
                'rubro': rubro,
                'cuenta': cuenta or '',
                'descripcion': descripcion,
                'periodo': periodo_texto,
                'valor': float(monto_total_rubro),
                'aplicado': float(monto_total_rubro)
            })

            try:
                desc_pa = (datos.get('descuento_pa_total') or Decimal('0.00')).quantize(Decimal('0.01'))
            except Exception:
                desc_pa = Decimal('0.00')
            if desc_pa > 0:
                pct_label = datos.get('descuento_pa_pct')
                pct_txt = f"{pct_label}%" if pct_label else "PA"
                detalle_recibo.append({
                    'rubro': rubro,
                    'cuenta': cuenta or '',
                    'descripcion': f"Descuento pago anual ({pct_txt})",
                    'periodo': periodo_texto,
                    'valor': float(-desc_pa),
                    'aplicado': float(-desc_pa)
                })
        
        detalle_recibo.sort(key=lambda item: item['rubro'])
        
        empresa_normalizada = (empresa or '').strip()
        identidad_negocio = (negocio.identidad or '').strip() if negocio and getattr(negocio, 'identidad', None) else ''
        nombre_negocio = (negocio.comerciante or '').strip() if negocio and getattr(negocio, 'comerciante', None) else ''
        direccion_negocio = (negocio.direccion or '').strip() if negocio and getattr(negocio, 'direccion', None) else ''
        rtn_negocio = (negocio.rtnnego or '').strip() if negocio and getattr(negocio, 'rtnnego', None) else ''
        expe_para_pago = negocio.expe if negocio and getattr(negocio, 'expe', None) else expe
        try:
            expe_decimal = Decimal(str(int(float(str(expe_para_pago).strip()))))
        except (TypeError, ValueError):
            expe_decimal = Decimal('0')
        
        numero_recibo = None
        numero_recibo_formateado = ''
        numero_recibo_decimal = None
        pagos_temp_creados = []
        
        with transaction.atomic():
            numero_recibo = NoRecibos.obtener_siguiente_numero_por_empresa(empresa_normalizada)
            numero_recibo_decimal = Decimal(str(numero_recibo))
            numero_recibo_formateado = f"{empresa_normalizada}-{str(int(numero_recibo)).zfill(6)}"
            
            for item in detalle_recibo:
                rubro_codigo = (item['rubro'] or '').strip() or 'SIN_RUBRO'
                cuenta_codigo = (item['cuenta'] or '').strip() or 'SIN_CUENTA'
                descripcion_item = (item['descripcion'] or f'Rubro {rubro_codigo}').strip()
                periodo_texto_item = (item.get('periodo') or '').strip()
                if periodo_texto_item:
                    descripcion_item = f"{descripcion_item} - Periodo {periodo_texto_item}"
                
                try:
                    valor_decimal = Decimal(str(item['valor'])).quantize(Decimal('0.01'))
                except Exception:
                    valor_decimal = Decimal('0.00')
                
                if valor_decimal == 0:
                    continue
                
                pago = PagoVariosTemp.objects.create(
                    empresa=empresa_normalizada or None,
                    recibo=numero_recibo_decimal,
                    rubro=rubro_codigo[:6],
                    codigo=cuenta_codigo[:16],
                    fecha=fecha_emision.date(),
                    identidad=identidad_negocio[:31] if identidad_negocio else None,
                    nombre=nombre_negocio[:150] if nombre_negocio else None,
                    descripcion=descripcion_item[:200],
                    valor=valor_decimal,
                    comentario=comentario if comentario else '',
                    oficina='1',
                    facturadora=(negocio.nombrenego or '')[:45] if negocio and getattr(negocio, 'nombrenego', None) else '',
                    aplicado='0',
                    traslado='0',
                    solvencia=Decimal('0'),
                    fecha_solv=None,
                    cantidad=Decimal('1'),
                    vl_unit=valor_decimal,
                    deposito=Decimal('0'),
                    cajero=None,
                    usuario=(usuario or 'SISTEMA')[:30],
                    referencia='',
                    banco='',
                    Tipofa='N',
                    Rtm=(rtm or '')[:20],
                    expe=expe_decimal,
                    pagodia=Decimal('0'),
                    rcaja=Decimal('0.00'),
                    Rfechapag=None,
                    permiso=Decimal('0'),
                    Fechavence=None,
                    direccion=direccion_negocio[:100] if direccion_negocio else ' ',
                    prima='',
                    categoria='',
                    sexo='',
                    rtn=rtn_negocio[:20] if rtn_negocio else None
                )
                pagos_temp_creados.append(pago.id)
        
        if not pagos_temp_creados:
            return JsonResponse({
                'exito': False,
                'mensaje': 'No se generaron conceptos para caja porque los valores calculados son cero.'
            }, status=400)
        
        # Generar código QR con los datos principales del recibo
        import qrcode
        import io
        import base64
        from qrcode.image.svg import SvgPathImage
        
        total_pagado = float(total_pagado_decimal)
        fecha_legible = fecha_emision.strftime('%d/%m/%Y %H:%M')
        
        qr_payload = (
            f"Municipio: {empresa}\n"
            f"Recibo: {numero_recibo_formateado}\n"
            f"Negocio: {negocio.nombrenego if negocio else ''}\n"
            f"RTM: {rtm}\n"
            f"Expediente: {expe}\n"
            f"Total: L. {total_pagado_decimal:.2f}\n"
            f"Fecha: {fecha_legible}"
        )
        
        qr_img = qrcode.make(qr_payload, image_factory=SvgPathImage, box_size=8, border=2)
        buffer = io.BytesIO()
        qr_img.save(buffer)
        qr_svg_b64 = base64.b64encode(buffer.getvalue()).decode()
        qr_data_uri = f"data:image/svg+xml;base64,{qr_svg_b64}"
        
        # Construir mensaje con información de rangos
        mensaje = f'Recibo generado: {numero_recibo_formateado}'
        if detalle_recibo:
            mensaje += f'\nSe registraron {len(detalle_recibo)} rubro(s) en caja.'
        if rangos_info:
            mensaje += '\n\nRangos cubiertos:'
            for rango in rangos_info:
                mensaje += f'\n- Rubro {rango["rubro"]}: {rango["mes_desde"]:02d}/{rango["ano_desde"]} hasta {rango["mes_hasta"]:02d}/{rango["ano_hasta"]}'
        
        recibo_url = reverse('tributario:ver_soporte', args=[numero_recibo_formateado])

        try:
            descuento_pago_anual_total = sum(
                (datos.get('descuento_pa_total') or Decimal('0.00')) for datos in pagos_por_rubro.values()
            )
        except Exception:
            descuento_pago_anual_total = Decimal('0.00')
        
        return JsonResponse({
            'exito': True,
            'mensaje': mensaje,
            'transaccion_id': None,
            'total_transacciones': len(transacciones_a_pagar),
            'pagos_temp_ids': pagos_temp_creados,
            'rangos': rangos_info,
            'recibo_url': recibo_url,
            'descuento_pago_anual_total': float(descuento_pago_anual_total),
            'desglose_mora': {
                'anio_referencia': breakdown['anio_referencia'],
                'base_actual': float(breakdown['base_actual']),
                'base_anteriores': float(breakdown['base_anteriores']),
                'mora_actual': float(breakdown['mora_actual']),
                'mora_anteriores': float(breakdown['mora_anteriores']),
            },
            'recibo': {
                'numero': int(numero_recibo),
                'numero_formateado': numero_recibo_formateado,
                'fecha_iso': fecha_emision.isoformat(),
                'fecha_legible': fecha_legible,
                'empresa': empresa,
                'total': total_pagado,
                'detalle': detalle_recibo,
                'qr_base64': '',
                'qr_data_uri': qr_data_uri,
                'tipo_pago': tipo,
                'periodos': rangos_info,
                'comentario': comentario,
                'url': recibo_url,
                'negocio': {
                    'nombre': negocio.nombrenego if negocio else '',
                    'comerciante': negocio.comerciante if negocio else '',
                    'direccion': negocio.direccion if negocio else '',
                    'rtm': rtm,
                    'expe': expe
                }
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al guardar transacción: {str(e)}'
        }, status=500)

def parametros_tributarios_crud(request):
    """CRUD para parámetros globales de amnistías, descuentos y recargos"""
    from django.db.models import Q
    from .models import ParametrosTributarios
    from tributario_app.forms import ParametrosTributariosForm
    from django.utils import timezone
    
    empresa = request.session.get('municipio_codigo') or request.session.get('empresa', '0301')

    # PA (Pago Anual) por ley: 10% global. Si no existe para el año vigente,
    # crear registro GLOB para que sea configurable en tabla a futuro.
    hoy = timezone.localdate()
    try:
        # Descuentos por edad (por ley): 25% TE y 35% CE (globales)
        ParametrosTributarios.objects.get_or_create(
            empresa='GLOB',
            tipo_parametro='TE',
            ano_vigencia=hoy.year,
            defaults={
                'descripcion': 'Descuento Tercera Edad (Ley) — 25%',
                'aplica_saldo_impuesto': True,
                'porcentaje_descuento_saldo': 25,
                'activo': True,
                'usuario_crea': request.session.get('usuario', 'SISTEMA'),
                'usuario_modifica': request.session.get('usuario', 'SISTEMA'),
            }
        )
        ParametrosTributarios.objects.get_or_create(
            empresa='GLOB',
            tipo_parametro='CE',
            ano_vigencia=hoy.year,
            defaults={
                'descripcion': 'Descuento Cuarta Edad (Ley) — 35%',
                'aplica_saldo_impuesto': True,
                'porcentaje_descuento_saldo': 35,
                'activo': True,
                'usuario_crea': request.session.get('usuario', 'SISTEMA'),
                'usuario_modifica': request.session.get('usuario', 'SISTEMA'),
            }
        )

        ParametrosTributarios.objects.get_or_create(
            empresa='GLOB',
            tipo_parametro='PA',
            ano_vigencia=hoy.year,
            defaults={
                'descripcion': 'Descuento Pago Anual (Ley) — 10%',
                'porcentaje_descuento_anual': 10,
                'meses_anticipacion': 1,
                'activo': True,
                'usuario_crea': request.session.get('usuario', 'SISTEMA'),
                'usuario_modifica': request.session.get('usuario', 'SISTEMA'),
            }
        )
    except Exception:
        # No bloquear la pantalla de parámetros si la BD no está disponible.
        pass
    
    # Parámetros filtrados: los de la empresa actual + los globales (GLOB)
    parametros = ParametrosTributarios.objects.filter(
        Q(empresa=empresa) | Q(empresa='GLOB')
    ).order_by('-ano_vigencia', 'tipo_parametro', 'empresa')
    
    form = ParametrosTributariosForm()
    edit_id = request.GET.get('edit')
    if edit_id:
        instance = ParametrosTributarios.objects.filter(id=edit_id).first()
        if instance:
            form = ParametrosTributariosForm(instance=instance)
            
    if request.method == 'POST':
        action = request.POST.get('action')
        param_id = request.POST.get('id')
        
        if action == 'delete' and param_id:
            ParametrosTributarios.objects.filter(id=param_id).delete()
            messages.success(request, 'Parámetro eliminado correctamente.')
            return redirect('tributario:parametros_tributarios')
            
        if param_id:
            instance = ParametrosTributarios.objects.filter(id=param_id).first()
            form = ParametrosTributariosForm(request.POST, instance=instance)
        else:
            form = ParametrosTributariosForm(request.POST)
            
        if form.is_valid():
            param = form.save(commit=False)
            if not param.empresa:
                param.empresa = empresa
            param.usuario_modifica = request.session.get('usuario', 'SISTEMA')
            if not param_id:
                param.usuario_crea = request.session.get('usuario', 'SISTEMA')
            param.save()
            messages.success(request, 'Parámetro guardado correctamente.')
            return redirect('tributario:parametros_tributarios')
        else:
            messages.error(request, 'Error al guardar el parámetro. Verifique los datos.')

    context = {
        'parametros': parametros,
        'form': form,
        'edit_id': edit_id,
        'empresa': empresa,
        'tipo_choices': ParametrosTributarios.TIPO_CHOICES
    }
    return render(request, 'parametros_tributarios.html', context)

from django.http import FileResponse, HttpResponse
from .services_permisos import verificar_requisitos_permiso, generar_permiso_pdf
from .models import Negocio
import datetime

def descargar_permiso_pdf(request):
    """
    Vista para descargar el Permiso de Operación en PDF tras validar requisitos.
    """
    rtm = request.GET.get('rtm')
    expe = request.GET.get('expe')
    empresa = request.GET.get('empresa') or request.session.get('municipio_codigo') or request.session.get('empresa', '0301')
    ano = int(request.GET.get('ano') or datetime.datetime.now().year)
    
    if not rtm or not expe:
        return HttpResponse("RTM y Expediente son requeridos", status=400)
        
    negocio = Negocio.objects.filter(empresa=empresa, rtm=rtm, expe=expe).first()
    if not negocio:
        return HttpResponse("Negocio no encontrado", status=404)
        
    # Verificar requisitos antes de emitir
    res = verificar_requisitos_permiso(negocio, ano)
    if not res['exito']:
        return HttpResponse(f"No cumple con los requisitos legales para el año {ano}. Detalles: {res['detalles']}", status=403)
        
    # Generar PDF
    pdf_buffer = generar_permiso_pdf(negocio, ano)
    
    filename = f"Permiso_Operacion_{rtm}_{ano}.pdf"
    return FileResponse(pdf_buffer, as_attachment=True, filename=filename)

