from django.shortcuts import render, redirect
from .forms import LoginForm
from usuarios.models import Usuario as usuario
from django.http import JsonResponse
from tributario.models import Actividad
from django.contrib.auth import logout
import logging
from .serializers import NegocioSerializer
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

# Importar utilidades de coordenadas
try:
    from .utils_coordenadas import latlng_to_utm, utm_to_latlng
except ImportError:
    # Si el import relativo falla, intentar import absoluto
    import sys
    import os
    # Obtener el directorio actual del archivo
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    # Agregar el directorio al path si no está
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    # Intentar import directo
    try:
        import utils_coordenadas
        latlng_to_utm = utils_coordenadas.latlng_to_utm
        utm_to_latlng = utils_coordenadas.utm_to_latlng
    except ImportError as e:
        # Si todo falla, definir funciones dummy
        logger = logging.getLogger(__name__)
        logger.warning(f"No se pudo importar utils_coordenadas: {e}. Usando funciones dummy.")
        def latlng_to_utm(lat, lng):
            return None, None
        def utm_to_latlng(easting, northing, zone=16):
            return None, None

# Importar vistas desde modules.tributario.views
from tributario.views import (
    obtener_cuenta_rezago,
    verificar_tarifa_existente,
    tarifas_crud,
)
import qrcode
import io
import base64
from django.http import HttpResponse
from django.template.loader import render_to_string
from .forms import LoginForm, ConceptoForm, ActividadForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

logger = logging.getLogger(__name__)

def login_view(request):
    error = None
    
    # Obtener municipios para el select
    from core.models import Municipio
    municipios = Municipio.objects.all().order_by('descripcion')
    
    if request.method == 'POST':
        usuario_input = request.POST.get('usuario', '').strip()
        password = request.POST.get('password', '').strip()
        municipio_id = request.POST.get('municipio', '').strip()
        
        if not usuario_input or not password or not municipio_id:
            error = "Todos los campos son obligatorios"
        else:
            try:
                # Obtener el municipio
                municipio_input = Municipio.objects.get(id=municipio_id)
                
                # Buscar usuario por usuario, empresa (código de municipio) y contraseña
                user = usuario.objects.get(
                    usuario=usuario_input,
                    empresa=municipio_input.codigo
                )
                
                # Verificar contraseña (ya está hasheada en el modelo)
                if user.password.startswith('pbkdf2_sha256'):
                    # La contraseña está hasheada, usar check_password
                    from django.contrib.auth.hashers import check_password
                    if check_password(password, user.password):
                        # Login exitoso - Guardar código de municipio en sesión
                        request.session['empresa'] = municipio_input.codigo
                        request.session['municipio_descripcion'] = municipio_input.descripcion
                        user.record_successful_login()
                        return redirect('tributario_app:tributario_menu_principal')
                    else:
                        # Contraseña incorrecta
                        user.record_failed_login()
                        error = "Usuario o contraseña incorrectos"
                else:
                    # Contraseña en texto plano (legacy)
                    if user.password == password:
                        # Login exitoso - Guardar código de municipio en sesión
                        request.session['empresa'] = municipio_input.codigo
                        request.session['municipio_descripcion'] = municipio_input.descripcion
                        user.record_successful_login()
                        return redirect('tributario_app:tributario_menu_principal')
                    else:
                        # Contraseña incorrecta
                        user.record_failed_login()
                        error = "Usuario o contraseña incorrectos"
                            
            except usuario.DoesNotExist:
                error = "Usuario no existe. Verifique el usuario y contraseña."
            except Municipio.DoesNotExist:
                error = "Municipio no válido."
            except Exception as e:
                error = f"Error en el sistema: {str(e)}"
    
    return render(request, 'core/login.html', {'municipios': municipios, 'error': error})

def menu_general(request):
    return render(request, 'menugeneral.html')


def bienes_inmuebles(request):
    return render(request, 'bienes_inmuebles.html')

def gestionar_mora_bienes(request):
    """
    Vista para gestionar (consultar y generar) la mora de Bienes Inmuebles.
    Similar a estado_cuenta para ICS, pero adaptada a BDCata1 y TasasMunicipales.
    """
    from django.contrib import messages
    from django.db.models import Sum
    from tributario.models import TransaccionesBienesInmuebles, Rubro
    from catastro.models import BDCata1, TasasMunicipales
    from calendar import monthrange
    import datetime

    empresa = request.session.get('municipio_codigo', '0301')
    empresa_get = request.GET.get('empresa', '').strip()
    if empresa_get and empresa_get != empresa:
        messages.error(request, f'⚠️ Error de seguridad: La empresa ({empresa_get}) no coincide.')
        empresa_filtro = empresa
    else:
        empresa_filtro = empresa_get if empresa_get else empresa

    cocata1 = request.GET.get('cocata1', '').strip()
    
    # Filtros para visualización en la tabla
    ano_desde = request.GET.get('ano_desde')
    mes_desde = request.GET.get('mes_desde')
    ano_hasta = request.GET.get('ano_hasta')
    mes_hasta = request.GET.get('mes_hasta')

    propiedad = None
    transacciones = []
    totales = {'mora_total': 0, 'saldo_final': 0}
    error_mensaje = None
    
    # Lista de rubros disponibles para la propiedad (sumando Impuesto + Tasas)
    rubros_disponibles = []

    if cocata1 and empresa_filtro:
        try:
            propiedad = BDCata1.objects.filter(empresa=empresa_filtro, cocata1=cocata1).first()
            if not propiedad:
                error_mensaje = f'❌ No se encontró la propiedad con Clave Catastral {cocata1}.'
            else:
                # Cargar rubros disponibles para esta propiedad
                # 1. Impuesto (Usamos un rubro genérico '0101' si no está en Tasas, pero debemos permitir al usuario seleccionarlo)
                # 2. Tasas
                tasas = TasasMunicipales.objects.filter(empresa=empresa_filtro, clave=cocata1)
                codigos_rubros = [t.rubro for t in tasas if t.rubro]
                if codigos_rubros:
                    rubros_objs = Rubro.objects.filter(empresa=empresa_filtro, codigo__in=codigos_rubros)
                    for r in rubros_objs:
                        rubros_disponibles.append({'codigo': r.codigo, 'descripcion': r.descripcion, 'tipo': r.tipo})
                
                # Siempre añadir un rubro para el Impuesto de Bienes Inmuebles si no está (por convención, asumiendo que debe poder cobrarse)
                if not any(r['codigo'] == 'IMPUBI' for r in rubros_disponibles):
                     rubros_disponibles.append({'codigo': 'IMPUBI', 'descripcion': 'Impuesto de Bienes Inmuebles', 'tipo': 'A'})

            # --- LÓGICA DE GENERACIÓN DE MORA (POST) ---
            if request.method == 'POST' and request.POST.get('accion') == 'generar_mora' and propiedad:
                from django.db import transaction
                try:
                    gen_ano_desde = int(request.POST.get('gen_ano_desde'))
                    gen_mes_desde = int(request.POST.get('gen_mes_desde'))
                    gen_ano_hasta = int(request.POST.get('gen_ano_hasta'))
                    gen_mes_hasta = int(request.POST.get('gen_mes_hasta'))
                    rubros_seleccionados = request.POST.getlist('rubros_generar')
                    
                    if not rubros_seleccionados:
                        messages.warning(request, 'Debe seleccionar al menos un rubro para generar mora.')
                    else:
                        registros_creados = 0
                        with transaction.atomic():
                            for year in range(gen_ano_desde, gen_ano_hasta + 1):
                                m_inicio = gen_mes_desde if year == gen_ano_desde else 1
                                m_fin = gen_mes_hasta if year == gen_ano_hasta else 12
                                
                                for month in range(m_inicio, m_fin + 1):
                                    for rubro_codigo in rubros_seleccionados:
                                        # Evitar duplicados
                                        qs_exist = TransaccionesBienesInmuebles.objects.filter(
                                            empresa=empresa_filtro, cocata1=cocata1, rubro=rubro_codigo, ano=year, mes=month
                                        )
                                        if qs_exist.exists():
                                            continue
                                            
                                        # Determinar valores a cobrar
                                        monto = 0
                                        tipo_cobro = 'M' # Por defecto mensual
                                        
                                        if rubro_codigo == 'IMPUBI': # Impuesto Bienes Inmuebles
                                            # El impuesto se cobra anualmente en el mes 8
                                            if month == 8:
                                                monto = propiedad.impuesto or 0
                                                tipo_cobro = 'A'
                                                
                                                # --- Descuento Tercera/Cuarta Edad (OBLIGATORIO) ---
                                                # Regla: SOLO aplica si el predio tiene exención en el avalúo catastral,
                                                # lo que indica que es la vivienda donde habita el contribuyente.
                                                tiene_exencion = False
                                                try:
                                                    # Regla negocio: aplicar SOLO si la exención del avalúo es > 0
                                                    # (indica vivienda donde habita / predio con exención aplicada).
                                                    ex_val = float(propiedad.exencion or 0)
                                                    tiene_exencion = ex_val > 0
                                                except Exception:
                                                    tiene_exencion = False

                                                if tiene_exencion:
                                                    descuento_porcentaje = 0.0
                                                    try:
                                                        from tributario_app.utils_cedula import info_cedula
                                                        info = info_cedula(propiedad.identidad) if propiedad.identidad else None
                                                        if info:
                                                            if info.get('aplica_cuarta_edad'):
                                                                descuento_porcentaje = 0.35
                                                            elif info.get('aplica_tercera_edad'):
                                                                descuento_porcentaje = 0.25
                                                    except Exception:
                                                        descuento_porcentaje = 0.0

                                                    if descuento_porcentaje > 0:
                                                        monto_descuento = float(monto) * float(descuento_porcentaje)
                                                        monto = float(monto) - monto_descuento
                                            else:
                                                continue # Solo se cobra en agosto
                                        else:
                                            # Es una Tasa Municipal
                                            tasa = tasas.filter(rubro=rubro_codigo).first()
                                            if tasa:
                                                monto = tasa.valor or 0
                                                r_obj = next((r for r in rubros_disponibles if r['codigo'] == rubro_codigo), None)
                                                
                                                is_annual = False
                                                if r_obj and r_obj['tipo'] == 'A':
                                                    is_annual = True
                                                elif rubro_codigo.upper().startswith('B'):
                                                    is_annual = True
                                                    
                                                if is_annual:
                                                    tipo_cobro = 'A'
                                                    if month != 8:
                                                        continue # Tasas/Impuestos anuales solo en agosto

                                            else:
                                                continue
                                                
                                        if monto > 0:
                                            # Calcular vencimiento (ultimo dia del mes si M, 31/08 si A)
                                            if tipo_cobro == 'A' and month == 8:
                                                vencimiento = datetime.date(year, 8, 31)
                                            else:
                                                _, last_day = monthrange(year, month)
                                                vencimiento = datetime.date(year, month, last_day)

                                            TransaccionesBienesInmuebles.objects.create(
                                                empresa=empresa_filtro,
                                                cocata1=cocata1,
                                                rubro=rubro_codigo,
                                                ano=year,
                                                mes=month,
                                                operacion='F',
                                                monto=monto,
                                                fecha=datetime.date.today(),
                                                vencimiento=vencimiento,
                                                usuario=request.user.username if request.user.is_authenticated else 'sistema',
                                                fechasys=datetime.datetime.now(),
                                                estado='A'
                                            )
                                            registros_creados += 1
                        
                        if registros_creados > 0:
                            messages.success(request, f'✅ Se generaron {registros_creados} registros de mora exitosamente.')
                        else:
                            messages.info(request, 'No se generaron registros nuevos (ya existían o no correspondían al periodo/tipo).')
                        
                except Exception as e:
                    messages.error(request, f'❌ Error al generar la mora: {str(e)}')

            # --- CONSULTA PARA MOSTRAR LA TABLA LUEGO DEL POST/GET ---
            qs = TransaccionesBienesInmuebles.objects.filter(
                empresa=empresa_filtro,
                cocata1=cocata1,
                estado='A'
            )

            if ano_desde and mes_desde:
                qs = qs.filter(ano__gte=ano_desde)
            if ano_hasta and mes_hasta:
                qs = qs.filter(ano__lte=ano_hasta)
            # Para simplificar mes: asumiendo q si viene mes_desde y ya filto año.
            
            qs = qs.order_by('ano', 'mes', 'fecha')
            transacciones_lista = list(qs)
            
            # Map rubro descriptions
            for trans in transacciones_lista:
                r_obj = next((r for r in rubros_disponibles if r['codigo'] == trans.rubro), None)
                trans.rubro_descripcion = r_obj['descripcion'] if r_obj else trans.rubro
                
            transacciones = transacciones_lista
            
            # Totales
            acumulados = qs.aggregate(total_monto=Sum('monto'))
            totales['saldo_final'] = float(acumulados.get('total_monto') or 0)
            totales['mora_total'] = totales['saldo_final'] # Simple, pending payments

        except Exception as e:
            error_mensaje = f'❌ Error al consultar transacciones: {str(e)}'
            messages.error(request, error_mensaje)

    identidad = request.GET.get('identidad', '').strip()
    current_year = datetime.datetime.now().year

    context = {
        'empresa': empresa_filtro,
        'municipio_codigo': empresa,
        'cocata1': cocata1,
        'identidad': identidad,
        'current_year': current_year,
        'propiedad': propiedad,
        'transacciones': transacciones,
        'totales': totales,
        'rubros_disponibles': rubros_disponibles,
        'error_mensaje': error_mensaje,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Mora Bienes Inmuebles'
    }

    return render(request, 'gestionar_mora_bienes.html', context)

@csrf_exempt
def enviar_a_caja_bienes(request):
    """Vista AJAX para enviar transacciones de Bienes Inmuebles a caja con reglas FIFO y Rezago"""
    if request.method == 'POST':
        try:
            import json
            from decimal import Decimal
            from django.utils import timezone
            from tributario.models import NoRecibos, PagoVariosTemp, TransaccionesBienesInmuebles, Rubro, ParametrosTributarios
            from catastro.models import BDCata1
            from tributario_app.utils_cedula import info_cedula, calcular_edad
            import datetime
            
            # Procesar datos
            data = json.loads(request.body)
            cocata1 = data.get('cocata1', '').strip()
            empresa = data.get('empresa', '').strip()
            pago_items = data.get('pago_items', []) # Lista de {id: X, monto_pagar: Y}
            identidad_pago = data.get('identidad_pago', '').strip()
            nombre_pago = data.get('nombre_pago', '').strip()
            comentario = data.get('comentario', '').strip()
            
            if not cocata1 or not pago_items:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Clave catastral y rubros a pagar son obligatorios'
                })
            
            item_ids = [item['id'] for item in pago_items]
            monto_map = {str(item['id']): Decimal(str(item['monto_pagar'])) for item in pago_items}
            
            transacciones = TransaccionesBienesInmuebles.objects.filter(
                id__in=item_ids,
                cocata1=cocata1,
                empresa=empresa,
                estado='A'
            ).order_by('ano', 'mes', 'id')
            
            if len(transacciones) != len(item_ids):
                encontrados = list(transacciones.values_list('id', flat=True))
                faltantes = list(set(int(i) for i in item_ids) - set(encontrados))
                db_items = list(TransaccionesBienesInmuebles.objects.filter(id__in=faltantes).values('id', 'empresa', 'cocata1', 'operacion', 'estado'))
                
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'Inconsistencia DB. Faltan IDs: {faltantes}. Info DB Real: {db_items}. Request: empresa={empresa}, cocata={cocata1}'
                })

            # Validación FIFO Server-side
            max_t = transacciones.last()
            pendientes_anteriores = TransaccionesBienesInmuebles.objects.filter(
                cocata1=cocata1,
                empresa=empresa,
                estado='A'
            ).exclude(id__in=item_ids)

            for p in pendientes_anteriores:
                if p.ano < max_t.ano or (p.ano == max_t.ano and p.mes < max_t.mes):
                    return JsonResponse({
                        'exito': False,
                        'mensaje': f'Regla FIFO: No puede pagar el periodo {int(max_t.ano)}-{int(max_t.mes):02} si aún debe el periodo {int(p.ano)}-{int(p.mes):02}'
                    })

            # Generar número de recibo
            numero_recibo = NoRecibos.obtener_siguiente_numero_por_empresa(empresa)
            numero_recibo_decimal = Decimal(str(numero_recibo))
            numero_recibo_formateado = f"{empresa}-{str(int(numero_recibo)).zfill(6)}"
            
            total_enviado = Decimal('0.00')
            ahora = timezone.now()
            current_year = ahora.year
            usuario = request.session.get('usuario', 'SISTEMA')
            
            # Cache de rubros para evitar múltiples queries
            rubros_query = Rubro.objects.filter(empresa=empresa)
            rubros_cache = {r.codigo: r for r in rubros_query}
            
            detalle_recibo = []

            # Descuento pago anual (PA):
            # Se aplica SOBRE EL AÑO DE CUOTAS QUE SE ESTÁ PAGANDO (t.ano),
            # y el mes de inicio depende de la fecha de pago y los meses de anticipación.
            #
            # Con meses_anticipacion=4:
            # - Pago en Sep 2026 para cuotas 2027 => aplica a las 12 (mes_inicio=1)
            # - Oct 2026 => 11 (mes_inicio=2)
            # - Nov 2026 => 10 (mes_inicio=3)
            # - Dic 2026 => 9  (mes_inicio=4)
            # - Ene 2027 (mismo año de cuotas) => desde May (mes_inicio=5) => 8 cuotas
            hoy = ahora.date()
            pa_cache = {}  # ano_objetivo -> (pct, meses_ant, mes_inicio)

            # Amnistía activa (si existe) para aplicar descuentos/condonaciones en recibo
            amnistia = ParametrosTributarios.amnistia_activa(empresa, ano=ahora.year, fecha_consulta=ahora.date())

            # Propiedad catastral para validar exención (adulto mayor solo si exencion > 0)
            propiedad = BDCata1.objects.filter(empresa=empresa, cocata1=cocata1).first()
            exencion_activa = False
            try:
                exencion_activa = float(propiedad.exencion or 0) > 0 if propiedad else False
            except Exception:
                exencion_activa = False

            # Agrupar por rubro + cuenta contable. Descuentos/amnistías salen como ítems separados
            # PERO conservan el MISMO rubro original (para rebajar por rubro).
            # key = (rubro, codigo_contable, concepto)
            grupos = {}

            # ── Desglose mora/base por año (control de abonos a periodos antiguos) ──
            # Regla:
            # - La clasificación se hace por el PERIODO del cargo (t.ano) y por tipo de rubro:
            #   - Mora: rubros que inician con R* (recargos) o I* (intereses)
            #   - Base: el resto
            breakdown = {
                'anio_referencia': int(current_year),
                'base_actual': Decimal('0.00'),
                'base_anteriores': Decimal('0.00'),
                'mora_actual': Decimal('0.00'),
                'mora_anteriores': Decimal('0.00'),
            }
            for t in transacciones:
                monto_pagar = monto_map.get(str(t.id), t.monto)
                rubro_obj = rubros_cache.get(t.rubro)
                rubro_norm_all = str(t.rubro or '').strip().upper()
                es_mora = rubro_norm_all.startswith('R') or rubro_norm_all.startswith('I')
                try:
                    es_actual = int(t.ano) == int(current_year)
                except Exception:
                    es_actual = False
                try:
                    monto_bd = Decimal(str(monto_pagar or 0)).quantize(Decimal('0.01'))
                except Exception:
                    monto_bd = Decimal('0.00')
                if monto_bd > 0:
                    if es_mora:
                        breakdown['mora_actual' if es_actual else 'mora_anteriores'] += monto_bd
                    else:
                        breakdown['base_actual' if es_actual else 'base_anteriores'] += monto_bd

                # Regla de Codificación Corriente vs Rezago (por año de la transacción)
                if int(t.ano) == current_year:
                    codigo_contable = rubro_obj.cuenta if rubro_obj and getattr(rubro_obj, 'cuenta', None) else t.rubro
                else:
                    codigo_contable = rubro_obj.cuentarez if rubro_obj and getattr(rubro_obj, 'cuentarez', None) else t.rubro

                codigo_contable = str(codigo_contable)[:16] if codigo_contable else ''

                periodo_str = f"{int(t.mes):02d}/{int(t.ano)}"

                # 1) Ítem base (positivo)
                key_base = (t.rubro, codigo_contable, 'BASE')
                if key_base not in grupos:
                    grupos[key_base] = {
                        'rubro': t.rubro,
                        'codigo': codigo_contable,
                        'descripcion': (rubro_obj.descripcion if rubro_obj else t.rubro),
                        'monto': Decimal('0.00'),
                        'periodos': [],
                    }
                grupos[key_base]['monto'] += Decimal(str(monto_pagar))
                grupos[key_base]['periodos'].append(periodo_str)

                # 2) Descuento pago anual (DPA) por año objetivo = t.ano
                try:
                    ano_objetivo = int(t.ano)
                except Exception:
                    ano_objetivo = None

                if ano_objetivo:
                    if ano_objetivo not in pa_cache:
                        # Obtener parámetro PA del año objetivo (cuotas que se pagan).
                        # Si no existe aún en tabla, crear el global por ley (10% y 4 meses)
                        # para no depender de carga manual.
                        param_pa = ParametrosTributarios.obtener_parametro('PA', empresa, ano_objetivo, fecha_consulta=hoy)
                        if not param_pa:
                            try:
                                ParametrosTributarios.objects.get_or_create(
                                    empresa='GLOB',
                                    tipo_parametro='PA',
                                    ano_vigencia=ano_objetivo,
                                    defaults={
                                        'descripcion': f'Descuento Pago Anual (Ley) — 10% (Año {ano_objetivo})',
                                        'porcentaje_descuento_anual': Decimal('10.00'),
                                        'meses_anticipacion': 4,
                                        'activo': True,
                                        'usuario_crea': request.session.get('usuario', 'SISTEMA'),
                                        'usuario_modifica': request.session.get('usuario', 'SISTEMA'),
                                    }
                                )
                            except Exception:
                                pass
                            param_pa = ParametrosTributarios.obtener_parametro('PA', empresa, ano_objetivo, fecha_consulta=hoy)
                        pct = Decimal(str(getattr(param_pa, 'porcentaje_descuento_anual', 0) or 0))
                        meses_ant = int(getattr(param_pa, 'meses_anticipacion', 0) or 0)

                        if pct > 0 and meses_ant >= 0:
                            if ano_objetivo == hoy.year:
                                # Pago dentro del mismo año de cuotas: aplica desde (mes_actual + meses_ant)
                                mes_inicio = hoy.month + meses_ant
                            elif ano_objetivo == hoy.year + 1:
                                # Pago en año anterior para cuotas del año siguiente: aplica desde (mes_actual + meses_ant - 12)
                                mes_inicio = max(1, hoy.month + meses_ant - 12)
                            else:
                                # Fuera del rango esperado: no aplicar automáticamente
                                mes_inicio = 13
                        else:
                            mes_inicio = 13

                        pa_cache[ano_objetivo] = (pct, meses_ant, mes_inicio)

                    pct_desc_anual, meses_ant, mes_inicio_desc = pa_cache[ano_objetivo]

                    if pct_desc_anual > 0 and int(t.mes) >= int(mes_inicio_desc or 13) and int(mes_inicio_desc or 13) <= 12:
                        dpa = (Decimal(str(monto_pagar)) * (pct_desc_anual / Decimal('100.00'))).quantize(Decimal('0.01'))
                        if dpa > 0:
                            key_dpa = (t.rubro, codigo_contable, 'DPA')
                            if key_dpa not in grupos:
                                grupos[key_dpa] = {
                                    'rubro': t.rubro,
                                    'codigo': codigo_contable,
                                    'descripcion': f"Descuento pago anual ({pct_desc_anual}%)",
                                    'monto': Decimal('0.00'),
                                    'periodos': [],
                                }
                            grupos[key_dpa]['monto'] -= dpa
                            grupos[key_dpa]['periodos'].append(periodo_str)

                # 3) Descuento adulto mayor (DTE/DCE)
                # Reglas:
                # - SOLO si exencion > 0 (predio habitado / con exención aplicada en avalúo)
                # - Aplica únicamente a rubros:
                #   - B0001 (BI Urbano)
                #   - B0002 (BI Rural)
                #   - T0001 (Agua Potable)
                # - Aplica desde el momento en que cumple 60/80: si debe años anteriores,
                #   solo se descuenta en los periodos cuyo vencimiento ocurre DESPUÉS de cumplir la edad.
                rubro_norm = str(t.rubro or '').strip().upper()
                if exencion_activa and rubro_norm in ('B0001', 'B0002', 'T0001'):
                    ced = identidad_pago or (propiedad.identidad if propiedad else '')
                    info = info_cedula(ced, None)

                    fecha_nac = info.get('fecha_nacimiento') if info else None
                    # Sin fecha de nacimiento no es posible determinar desde qué año aplica.
                    pct = Decimal('0.00')
                    label = ''
                    concepto = ''

                    if fecha_nac:
                        # Usar vencimiento del cargo (si existe) como referencia; si no, usar último día del mes/año
                        ref = getattr(t, 'vencimiento', None)
                        if not ref:
                            try:
                                y = int(t.ano)
                                m = int(t.mes)
                                # Si mes no es válido, asumir diciembre
                                if m < 1 or m > 12:
                                    m = 12
                                # último día del mes
                                if m == 12:
                                    ref = datetime.date(y, 12, 31)
                                else:
                                    # día 28 + 4 días => siguiente mes; restar día para fin de mes
                                    ref = datetime.date(y, m, 28) + datetime.timedelta(days=4)
                                    ref = ref.replace(day=1) - datetime.timedelta(days=1)
                            except Exception:
                                ref = hoy

                        edad_en_periodo = calcular_edad(fecha_nac, ref)
                        if edad_en_periodo >= 80:
                            pct = Decimal('35.00')
                            label = 'Descuento Cuarta Edad (35%)'
                            concepto = 'DCE'
                        elif edad_en_periodo >= 60:
                            pct = Decimal('25.00')
                            label = 'Descuento Tercera Edad (25%)'
                            concepto = 'DTE'

                    if pct > 0:
                        dam = (Decimal(str(monto_pagar)) * (pct / Decimal('100.00'))).quantize(Decimal('0.01'))
                        if dam > 0:
                            key_dam = (t.rubro, codigo_contable, concepto)
                            if key_dam not in grupos:
                                grupos[key_dam] = {
                                    'rubro': t.rubro,
                                    'codigo': codigo_contable,
                                    'descripcion': label,
                                    'monto': Decimal('0.00'),
                                    'periodos': [],
                                }
                            grupos[key_dam]['monto'] -= dam
                            grupos[key_dam]['periodos'].append(periodo_str)

                # 4) Amnistía tributaria: condonación de recargos (R*) y/o descuento de saldo
                if amnistia:
                    # Aplicar solo a cargos vencidos HASTA la fecha_corte del decreto (si existe).
                    # Para efectividad/estrictez: si hay fecha_corte pero no hay vencimiento en el cargo,
                    # NO aplicar amnistía/descuento (regla basada en vencimiento).
                    corte_ok = True
                    if amnistia.fecha_corte:
                        venc = getattr(t, 'vencimiento', None)
                        if not venc:
                            corte_ok = False
                        else:
                            try:
                                corte_ok = venc <= amnistia.fecha_corte
                            except Exception:
                                corte_ok = False

                    if corte_ok:
                        # 4.1) Recargos (rubros R*): condonación parcial/total
                        if amnistia.aplica_recargos and str(t.rubro or '').strip().upper().startswith('R'):
                            pct = Decimal(str(amnistia.porcentaje_condonacion or 0))
                            if pct > 0:
                                d = (Decimal(str(monto_pagar)) * (pct / Decimal('100.00'))).quantize(Decimal('0.01'))
                                if d > 0:
                                    key_damr = (t.rubro, codigo_contable, 'AMR')
                                    if key_damr not in grupos:
                                        grupos[key_damr] = {
                                            'rubro': t.rubro,
                                            'codigo': codigo_contable,
                                            'descripcion': f"Amnistía recargos ({pct}%)",
                                            'monto': Decimal('0.00'),
                                            'periodos': [],
                                        }
                                    grupos[key_damr]['monto'] -= d
                                    grupos[key_damr]['periodos'].append(periodo_str)

                        # 4.1b) Intereses (rubros I*): condonación parcial/total (si se usa este esquema)
                        if amnistia.aplica_intereses and str(t.rubro or '').strip().upper().startswith('I'):
                            pct = Decimal(str(amnistia.porcentaje_condonacion or 0))
                            if pct > 0:
                                d = (Decimal(str(monto_pagar)) * (pct / Decimal('100.00'))).quantize(Decimal('0.01'))
                                if d > 0:
                                    key_ami = (t.rubro, codigo_contable, 'AMI')
                                    if key_ami not in grupos:
                                        grupos[key_ami] = {
                                            'rubro': t.rubro,
                                            'codigo': codigo_contable,
                                            'descripcion': f"Amnistía intereses ({pct}%)",
                                            'monto': Decimal('0.00'),
                                            'periodos': [],
                                        }
                                    grupos[key_ami]['monto'] -= d
                                    grupos[key_ami]['periodos'].append(periodo_str)

                        # 4.2) Descuento por amnistía sobre saldo (no recargos)
                        rub = str(t.rubro or '').strip().upper()
                        es_recargo = rub.startswith('R')
                        es_interes = rub.startswith('I')
                        if amnistia.aplica_saldo_impuesto and not es_recargo and not es_interes:
                            pct = Decimal(str(amnistia.porcentaje_descuento_saldo or 0))
                            if pct > 0:
                                d = (Decimal(str(monto_pagar)) * (pct / Decimal('100.00'))).quantize(Decimal('0.01'))
                                if d > 0:
                                    key_dams = (t.rubro, codigo_contable, 'DAM')
                                    if key_dams not in grupos:
                                        grupos[key_dams] = {
                                            'rubro': t.rubro,
                                            'codigo': codigo_contable,
                                            'descripcion': f"Descuento amnistía ({pct}%)",
                                            'monto': Decimal('0.00'),
                                            'periodos': [],
                                        }
                                    grupos[key_dams]['monto'] -= d
                                    grupos[key_dams]['periodos'].append(periodo_str)

            # Crear registros en PagoVariosTemp: 1 por grupo (rubro + cuenta) incluyendo descuentos como ítems negativos
            for (_rubro, _codigo, _concepto), g in grupos.items():
                monto_item = Decimal(str(g['monto'])).quantize(Decimal('0.01'))
                if monto_item == 0:
                    continue

                periodos = ', '.join(g['periodos'][:6]) + ('…' if len(g['periodos']) > 6 else '')
                descripcion_final = f"{g['descripcion']} ({periodos})"

                PagoVariosTemp.objects.create(
                    empresa=empresa,
                    recibo=numero_recibo_decimal,
                    rubro=g['rubro'],
                    codigo=g['codigo'],
                    fecha=ahora.date(),
                    identidad=identidad_pago,
                    nombre=nombre_pago,
                    descripcion=descripcion_final,
                    valor=monto_item,
                    comentario=comentario,
                    oficina='001',
                    facturadora='BIENES INMUEBLES',
                    aplicado='0',
                    traslado='0',
                    solvencia=0,
                    fecha_solv=None,
                    cantidad=Decimal('1.00'),
                    vl_unit=monto_item,
                    deposito=0,
                    cajero=usuario,
                    usuario=usuario,
                    referencia='',
                    banco='',
                    Tipofa=' ',
                    Rtm=cocata1,
                    expe='0',
                    pagodia=0,
                    rcaja=monto_item,
                    Rfechapag=ahora.date(),
                    permiso=0,
                    Fechavence=None,
                    direccion='',
                    prima='',
                    sexo='',
                    rtn=identidad_pago
                )

                detalle_recibo.append({
                    'rubro': g['rubro'],
                    'descripcion': g['descripcion'],
                    'codigo_presupuestario': g['codigo'],
                    'concepto': _concepto,  # BASE/DPA/DTE/DCE/AMR/DAM (solo para visualización)
                    # Compatibilidad frontend (soporte/whatsapp)
                    'periodo': periodos,
                    'monto': float(monto_item),
                })

                total_enviado += monto_item
                
            # Detalle visual: agrupar descuentos (para impresión/soporte)
            detalle_visual = []
            total_dpa = Decimal('0.00')
            total_adulto_mayor = Decimal('0.00')
            for it in detalle_recibo:
                if it.get('concepto') == 'DPA':
                    try:
                        total_dpa += Decimal(str(it.get('monto', 0)))
                    except Exception:
                        pass
                elif it.get('concepto') in ('DTE', 'DCE'):
                    try:
                        total_adulto_mayor += Decimal(str(it.get('monto', 0)))
                    except Exception:
                        pass
                else:
                    detalle_visual.append(it)

            if total_dpa != 0:
                detalle_visual.append({
                    'codigo_presupuestario': '',
                    'rubro': '',
                    'descripcion': 'Descuento pago anual (resumen)',
                    'concepto': 'DPA_RESUMEN',
                    'periodo': '',
                    'monto': float(total_dpa),
                })

            if total_adulto_mayor != 0:
                detalle_visual.append({
                    'codigo_presupuestario': '',
                    'rubro': '',
                    'descripcion': 'Descuento adulto mayor (resumen)',
                    'concepto': 'DAMAYOR_RESUMEN',
                    'periodo': '',
                    'monto': float(total_adulto_mayor),
                })

            return JsonResponse({
                'exito': True,
                'mensaje': f'Transacción enviada a caja exitosamente. Recibo: {numero_recibo_formateado}',
                'numero_recibo': numero_recibo_formateado,
                'total': float(total_enviado),
                'fecha': ahora.strftime('%d/%m/%Y %H:%M'),
                'contribuyente': nombre_pago,
                'identidad': identidad_pago,
                'propiedad_clave': cocata1,
                'detalle': detalle_recibo,
                'detalle_visual': detalle_visual,
                'desglose_mora': {
                    'anio_referencia': breakdown['anio_referencia'],
                    'base_actual': float(breakdown['base_actual']),
                    'base_anteriores': float(breakdown['base_anteriores']),
                    'mora_actual': float(breakdown['mora_actual']),
                    'mora_anteriores': float(breakdown['mora_anteriores']),
                },
                'descuento_pago_anual': {
                    'hoy': hoy.isoformat(),
                    'cache': {
                        str(k): {
                            'porcentaje': float(v[0] or 0),
                            'meses_anticipacion': int(v[1] or 0),
                            'mes_inicio': int(v[2] or 0),
                        } for k, v in pa_cache.items()
                    }
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error al enviar a caja: {str(e)}'
            })
            
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'})

def industria_comercio_servicios(request):
    return render(request, 'industria_comercio_servicios.html')

def miscelaneos(request):
    from tributario.models import Oficina
    
    # Obtener el código de empresa de la sesión
    empresa = request.session.get('empresa')
    if not empresa:
        return redirect('tributario:tributario_login')
    
    # Obtener todas las oficinas ordenadas por código
    oficinas = Oficina.objects.all().order_by('codigo')
    
    return render(request, 'miscelaneos.html', {
        'oficinas': oficinas,
        'empresa': empresa
    })

def convenios_pagos(request):
    return render(request, 'convenios_pagos.html')

def utilitarios(request):
    return render(request, 'utilitarios.html')
def logout_view(request):
    logout(request)
    return redirect('tributario_app:login')

def parse_fecha(fecha_str):
    if not fecha_str:
        return None
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except Exception:
        return None

def maestro_negocios(request):
    # Obtener el código de municipio de la sesión
    empresa = request.session.get('empresa')
    if not empresa:
        return redirect('tributario:tributario_login')
    
    mensaje = None
    exito = False
    
    # Verificar si se está regresando desde otro formulario con parámetros
    rtm_regreso = request.GET.get('rtm', '').strip()
    expe_regreso = request.GET.get('expe', '').strip()
    empresa_regreso = request.GET.get('empresa', '').strip()
    
    logger.info(f"Verificando parámetros de regreso - Empresa: {empresa_regreso}, RTM: {rtm_regreso}, Expediente: {expe_regreso}")
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'salvar':
            # Obtener datos del formulario con mejor manejo de valores vacíos
            empresa = request.POST.get('empresa', '').strip()
            rtm = request.POST.get('rtm', '').strip()
            expe = request.POST.get('expe', '').strip()
            confirmar_actualizacion = request.POST.get('confirmar_actualizacion')
            
            # Log para debugging mejorado
            logger.info(f"Procesando salvar - Empresa: '{empresa}', RTM: '{rtm}', Expediente: '{expe}'")
            logger.info(f"Longitudes - Empresa: {len(empresa)}, RTM: {len(rtm)}, Expediente: {len(expe)}")
            logger.info(f"Datos POST recibidos: {dict(request.POST)}")
            logger.info(f"Content-Type: {request.headers.get('content-type', 'No especificado')}")
            logger.info(f"X-Requested-With: {request.headers.get('x-requested-with', 'No especificado')}")
            logger.info(f"Method: {request.method}")
            logger.info(f"POST keys: {list(request.POST.keys())}")
            
            # Log para debugging
            logger.info("Procesando formulario sin coordenadas")
            
            # Validación mejorada de campos obligatorios
            logger.info(f"Validando campos: empresa='{empresa}', rtm='{rtm}', expe='{expe}'")
            logger.info(f"Longitudes: empresa={len(empresa)}, rtm={len(rtm)}, expe={len(expe)}")
            
            campos_faltantes = []
            if not empresa or empresa.strip() == '':
                campos_faltantes.append("Municipio")
                logger.warning(f"Campo empresa vacío o nulo: '{empresa}'")
            if not rtm or rtm.strip() == '':
                campos_faltantes.append("RTM")
                logger.warning(f"Campo rtm vacío o nulo: '{rtm}'")
            if not expe or expe.strip() == '':
                campos_faltantes.append("Expediente")
                logger.warning(f"Campo expe vacío o nulo: '{expe}'")
            
            logger.info(f"Campos faltantes detectados: {campos_faltantes}")
            
            if campos_faltantes:
                mensaje = f"⚠️ Campos obligatorios faltantes: {', '.join(campos_faltantes)}. Por favor, complete todos los campos requeridos."
                exito = False
                logger.warning(f"Validación falló: {mensaje}")
                
                # Si es una petición AJAX, devolver JSON inmediatamente
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    logger.info(f"Devolviendo respuesta AJAX de validación fallida: exito={exito}, mensaje={mensaje}")
                    return JsonResponse({
                        'exito': exito, 
                        'mensaje': mensaje
                    })
            else:
                logger.info("✅ Validación de campos obligatorios pasó, continuando...")
                try:
                    # Validar tipos y longitudes
                    errores_longitud = []
                    if len(empresa) > 4:
                        errores_longitud.append("Empresa (máximo 4 caracteres)")
                    if len(rtm) > 16:
                        errores_longitud.append("RTM (máximo 16 caracteres)")
                    if len(expe) > 12:
                        errores_longitud.append("Expediente (máximo 12 caracteres)")
                    
                    if errores_longitud:
                        mensaje = f"❌ Longitud excedida en: {', '.join(errores_longitud)}. Verifique los límites de caracteres."
                        exito = False
                    else:
                        # Buscar si el negocio ya existe por las llaves primarias
                        logger.info(f"Buscando negocio existente: empresa={empresa}, rtm={rtm}, expe={expe}")
                        negocio_existente = Negocio.objects.filter(empresa=empresa, rtm=rtm, expe=expe).first()
                        if negocio_existente:
                            logger.info(f"Negocio existente encontrado: {negocio_existente}")
                            logger.info(f"Confirmar actualización: {confirmar_actualizacion}")
                            
                            if confirmar_actualizacion == '1':
                                logger.info("Procesando confirmación de actualización...")
                                logger.info(f"Datos POST recibidos: {dict(request.POST)}")
                                
                                # Actualizar el negocio existente
                                for campo in [
                                    'nombrenego', 'comerciante', 'identidad', 'rtnpersonal', 'rtnnego', 'catastral',
                                    'identidadrep', 'representante', 'direccion', 'actividad', 'estatus',
                                    'fecha_ini', 'fecha_can', 'telefono', 'celular', 'socios', 'correo', 'pagweb',
                                    'comentario', 'usuario']:
                                    if campo in ['fecha_ini', 'fecha_can']:
                                        valor = parse_fecha(request.POST.get(campo))
                                        logger.info(f"Campo {campo} (fecha): {valor}")
                                    else:
                                        # Usar valores por defecto según la estructura de la BD
                                        valor = request.POST.get(campo, ' ')
                                        if campo in ['identidad', 'catastral', 'socios', 'estatus']:
                                            # Campos NOT NULL - usar valores por defecto apropiados
                                            if campo in ['identidad', 'catastral']:
                                                valor = request.POST.get(campo, '0')
                                            elif campo == 'estatus':
                                                valor = request.POST.get(campo, 'A')
                                            else:
                                                valor = request.POST.get(campo, '')
                                        logger.info(f"Campo {campo}: {valor}")
                                    setattr(negocio_existente, campo, valor)
                                
                                # Procesar coordenadas UTM directamente desde el formulario
                                logger.info("Procesando coordenadas UTM desde el formulario...")
                                cx = request.POST.get('cx', '0.00')
                                cy = request.POST.get('cy', '0.00')
                                
                                # Las coordenadas ya vienen en formato UTM desde el formulario
                                try:
                                    if cx and cx != '0' and cx != '0.0' and cx != '0.00' and cy and cy != '0' and cy != '0.0' and cy != '0.00':
                                        # Convertir a float y validar
                                        cx_float = float(cx.replace(',', '.'))
                                        cy_float = float(cy.replace(',', '.'))
                                        
                                        if cx_float > 0 and cy_float > 0:
                                            negocio_existente.cx = cx_float
                                            negocio_existente.cy = cy_float
                                            logger.info(f"Coordenadas UTM guardadas - X (Easting): {cx_float:.2f}, Y (Northing): {cy_float:.2f}")
                                        else:
                                            negocio_existente.cx = 0.00
                                            negocio_existente.cy = 0.00
                                            logger.info("Coordenadas inválidas (valores <= 0), establecidas en 0.00")
                                    else:
                                        negocio_existente.cx = 0.00
                                        negocio_existente.cy = 0.00
                                        logger.info("Coordenadas vacías o cero, establecidas en 0.00")
                                except (ValueError, TypeError) as e:
                                    logger.error(f"Error al procesar coordenadas UTM: {str(e)}")
                                    negocio_existente.cx = 0.00
                                    negocio_existente.cy = 0.00
                                
                                # Verificar estado del modelo antes de guardar
                                logger.info(f"Estado del negocio antes de guardar:")
                                logger.info(f"  ID: {negocio_existente.id}")
                                logger.info(f"  Empresa: {negocio_existente.empresa}")
                                logger.info(f"  RTM: {negocio_existente.rtm}")
                                logger.info(f"  Expediente: {negocio_existente.expe}")
                                logger.info(f"  Nombre: {negocio_existente.nombrenego}")
                                
                                try:
                                    logger.info("Intentando guardar el negocio...")
                                    negocio_existente.save()
                                    logger.info(f"Negocio actualizado exitosamente")
                                    mensaje = "✅ Negocio actualizado exitosamente. Los cambios han sido guardados en la base de datos."
                                    exito = True
                                    
                                    # Si es una petición AJAX, devolver JSON inmediatamente
                                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                                        logger.info(f"Devolviendo respuesta AJAX de actualización exitosa: exito={exito}, mensaje={mensaje}")
                                        return JsonResponse({
                                            'exito': exito, 
                                            'mensaje': mensaje,
                                            'actualizado': True
                                        })
                                except Exception as e:
                                    logger.error(f"Error al actualizar negocio: {str(e)}")
                                    logger.error(f"Tipo de error: {type(e).__name__}")
                                    import traceback
                                    logger.error(f"Traceback completo: {traceback.format_exc()}")
                                    mensaje = f"❌ Error al actualizar el negocio: {str(e)}. Por favor, intente nuevamente o contacte al administrador."
                                    exito = False
                                    
                                    # Si es una petición AJAX, devolver JSON inmediatamente
                                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                                        logger.info(f"Devolviendo respuesta AJAX de error: exito={exito}, mensaje={mensaje}")
                                        return JsonResponse({
                                            'exito': exito, 
                                            'mensaje': mensaje
                                        })
                            else:
                                # El negocio existe, pero no se ha confirmado la actualización
                                # Solo mostrar mensaje de confirmación si la acción es "salvar"
                                if accion == 'salvar':
                                    logger.info("Solicitando confirmación para actualizar negocio existente")
                                    mensaje = f"❓ El negocio con Empresa: {empresa}, RTM: {rtm}, Expediente: {expe} ya existe en la base de datos. ¿Desea actualizar la información existente?"
                                    exito = False
                                    
                                    # Si es una petición AJAX, devolver JSON con información de confirmación
                                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                                        logger.info(f"Devolviendo respuesta AJAX de confirmación: exito={exito}, mensaje={mensaje}")
                                        return JsonResponse({
                                            'exito': exito, 
                                            'mensaje': mensaje,
                                            'requiere_confirmacion': True,
                                            'existe': True
                                        })
                                else:
                                    # Para otras acciones (nuevo, eliminar), no mostrar confirmación
                                    logger.info("Negocio existente encontrado, pero no es acción salvar")
                                    mensaje = "Negocio encontrado."
                                    exito = True
                        else:
                            # El negocio no existe, crear nuevo
                            logger.info("✅ Negocio no existe, creando nuevo...")
                            logger.info(f"📝 Datos para nuevo negocio: empresa={empresa}, rtm={rtm}, expe={expe}")
                            try:
                                # Procesar coordenadas UTM directamente desde el formulario para nuevo negocio
                                logger.info("Procesando coordenadas UTM desde el formulario para nuevo negocio...")
                                cx = request.POST.get('cx', '0.00')
                                cy = request.POST.get('cy', '0.00')
                                
                                # Las coordenadas ya vienen en formato UTM desde el formulario
                                cx_float = 0.00
                                cy_float = 0.00
                                
                                try:
                                    if cx and cx != '0' and cx != '0.0' and cx != '0.00' and cy and cy != '0' and cy != '0.0' and cy != '0.00':
                                        # Convertir a float y validar
                                        cx_float = float(cx.replace(',', '.'))
                                        cy_float = float(cy.replace(',', '.'))
                                        
                                        if cx_float > 0 and cy_float > 0:
                                            logger.info(f"Coordenadas UTM guardadas para nuevo negocio - X (Easting): {cx_float:.2f}, Y (Northing): {cy_float:.2f}")
                                        else:
                                            cx_float = 0.00
                                            cy_float = 0.00
                                            logger.info("Coordenadas inválidas (valores <= 0), establecidas en 0.00 para nuevo negocio")
                                    else:
                                        cx_float = 0.00
                                        cy_float = 0.00
                                        logger.info("Coordenadas vacías o cero, establecidas en 0.00 para nuevo negocio")
                                except (ValueError, TypeError) as e:
                                    logger.error(f"Error al procesar coordenadas UTM para nuevo negocio: {str(e)}")
                                    cx_float = 0.00
                                    cy_float = 0.00
                                
                                nuevo_negocio = Negocio(
                                    empresa=empresa,
                                    rtm=rtm,
                                    expe=expe,
                                    nombrenego=request.POST.get('nombrenego', ' '),
                                    comerciante=request.POST.get('comerciante', ' '),
                                    identidad=request.POST.get('identidad', '0'),  # Campo NOT NULL
                                    rtnpersonal=request.POST.get('rtnpersonal', ' '),
                                    rtnnego=request.POST.get('rtnnego', ' '),
                                    catastral=request.POST.get('catastral', '0'),  # Campo NOT NULL
                                    identidadrep=request.POST.get('identidadrep', ' '),
                                    representante=request.POST.get('representante', ' '),
                                    direccion=request.POST.get('direccion', ' '),
                                    actividad=request.POST.get('actividad', ' '),
                                    estatus=request.POST.get('estatus', 'A'),  # Campo NOT NULL
                                    fecha_ini=parse_fecha(request.POST.get('fecha_ini')),
                                    fecha_can=parse_fecha(request.POST.get('fecha_can')),
                                    telefono=request.POST.get('telefono', ' '),
                                    celular=request.POST.get('celular', ' '),
                                    socios=request.POST.get('socios', ''),  # Campo NOT NULL
                                    correo=request.POST.get('correo', ' '),
                                    pagweb=request.POST.get('pagweb', ' '),
                                    comentario=request.POST.get('comentario', ''),
                                    usuario=request.POST.get('usuario', ' '),
                                    cx=cx_float,
                                    cy=cy_float,
                                )
                                logger.info(f"💾 Intentando guardar nuevo negocio...")
                                logger.info(f"📋 Datos del negocio antes de guardar:")
                                logger.info(f"  empresa: {empresa}")
                                logger.info(f"  rtm: {rtm}")
                                logger.info(f"  expe: {expe}")
                                logger.info(f"  identidad: {request.POST.get('identidad', '0')}")
                                logger.info(f"  catastral: {request.POST.get('catastral', '0')}")
                                logger.info(f"  estatus: {request.POST.get('estatus', '')}")
                                logger.info(f"  socios: {request.POST.get('socios', '')}")
                                logger.info(f"  cx: {cx_float}")
                                logger.info(f"  cy: {cy_float}")
                                
                                try:
                                    nuevo_negocio.save()
                                    logger.info(f"✅ Nuevo negocio guardado exitosamente con ID: {nuevo_negocio.id}")
                                except Exception as save_error:
                                    logger.error(f"❌ Error al guardar negocio: {str(save_error)}")
                                    logger.error(f"❌ Tipo de error: {type(save_error).__name__}")
                                    import traceback
                                    logger.error(f"❌ Traceback: {traceback.format_exc()}")
                                    raise save_error
                                mensaje = "✅ Nuevo negocio guardado exitosamente. El registro ha sido creado en la base de datos."
                                exito = True
                                
                                # Si es una petición AJAX, devolver JSON inmediatamente
                                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                                    logger.info(f"Devolviendo respuesta AJAX de éxito: exito={exito}, mensaje={mensaje}")
                                    return JsonResponse({
                                        'exito': exito, 
                                        'mensaje': mensaje,
                                        'insertado': True
                                    })
                            except Exception as e:
                                logger.error(f"Error al guardar negocio: {str(e)}")
                                mensaje = f"❌ Error al guardar el negocio: {str(e)}. Por favor, verifique los datos e intente nuevamente."
                                exito = False
                                
                                # Si es una petición AJAX, devolver JSON inmediatamente
                                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                                    logger.info(f"Devolviendo respuesta AJAX de error: exito={exito}, mensaje={mensaje}")
                                    return JsonResponse({
                                        'exito': exito, 
                                        'mensaje': mensaje
                                    })
                except Exception as e:
                    logger.error(f"Error general en salvar: {str(e)}")
                    mensaje = f"Error inesperado: {str(e)}"
                    exito = False
                    
                    # Si es una petición AJAX, devolver JSON inmediatamente
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        logger.info(f"Devolviendo respuesta AJAX de error general: exito={exito}, mensaje={mensaje}")
                        return JsonResponse({
                            'exito': exito, 
                            'mensaje': mensaje
                        })
        
        elif accion == 'eliminar':
            # Obtener datos del formulario para eliminar
            empresa = request.POST.get('empresa', '').strip()
            rtm = request.POST.get('rtm', '').strip()
            expe = request.POST.get('expe', '').strip()
            
            logger.info(f"Procesando eliminar - Empresa: {empresa}, RTM: {rtm}, Expediente: {expe}")
            logger.info(f"Datos POST recibidos: {dict(request.POST)}")
            
            # Validar campos obligatorios
            if not empresa or not rtm or not expe:
                mensaje = "Los campos Empresa, RTM y Expediente son obligatorios para eliminar."
                exito = False
            else:
                try:
                    # Buscar el negocio a eliminar
                    logger.info(f"Buscando negocio para eliminar: empresa={empresa}, rtm={rtm}, expe={expe}")
                    negocio_a_eliminar = Negocio.objects.filter(empresa=empresa, rtm=rtm, expe=expe).first()
                    
                    if negocio_a_eliminar:
                        logger.info(f"Negocio encontrado para eliminar: {negocio_a_eliminar}")
                        
                        # Eliminar el negocio
                        negocio_a_eliminar.delete()
                        logger.info(f"Negocio eliminado exitosamente")
                        mensaje = "🗑️ Negocio eliminado exitosamente. El registro ha sido removido de la base de datos."
                        exito = True
                        
                        # Si es una petición AJAX, devolver JSON inmediatamente
                        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                            logger.info(f"Devolviendo respuesta AJAX de eliminación exitosa: exito={exito}, mensaje={mensaje}")
                            return JsonResponse({
                                'exito': exito, 
                                'mensaje': mensaje,
                                'eliminado': True
                            })
                    else:
                        logger.warning(f"Negocio no encontrado para eliminar: {empresa}-{rtm}-{expe}")
                        mensaje = f"⚠️ El negocio con Empresa: {empresa}, RTM: {rtm}, Expediente: {expe} no existe en la base de datos."
                        exito = False
                        
                        # Si es una petición AJAX, devolver JSON inmediatamente
                        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                            logger.info(f"Devolviendo respuesta AJAX de negocio no encontrado: exito={exito}, mensaje={mensaje}")
                            return JsonResponse({
                                'exito': exito, 
                                'mensaje': mensaje
                            })
                        
                except Exception as e:
                    logger.error(f"Error al eliminar negocio: {str(e)}")
                    mensaje = f"❌ Error al eliminar el negocio: {str(e)}. Por favor, intente nuevamente o contacte al administrador."
                    exito = False
                    
                    # Si es una petición AJAX, devolver JSON inmediatamente
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        logger.info(f"Devolviendo respuesta AJAX de error en eliminación: exito={exito}, mensaje={mensaje}")
                        return JsonResponse({
                            'exito': exito, 
                            'mensaje': mensaje
                        })
        
        # Si es una petición AJAX y no se ha devuelto respuesta aún, devolver JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            logger.info(f"Devolviendo respuesta AJAX final: exito={exito}, mensaje={mensaje}")
            return JsonResponse({'exito': exito, 'mensaje': mensaje or ''})

    # Solo procesar la parte de renderizado si no es una petición AJAX
    try:
        municipio_descripcion = request.session.get('municipio_descripcion')
    except AttributeError:
        # Si no hay sesión disponible, usar valores por defecto
        municipio_descripcion = 'Municipio por defecto'
        logger.warning("No hay sesión disponible, usando valores por defecto")
    
    # Filtrar actividades por el municipio (empresa)
    actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
    
    # Crear un objeto Negocio para el formulario
    negocio_formulario = Negocio()
    
    # Si hay parámetros de regreso, usarlos para mantener los valores
    if rtm_regreso and expe_regreso:
        logger.info(f"Manteniendo valores de regreso - Empresa: {empresa_regreso or empresa}, RTM: {rtm_regreso}, Expediente: {expe_regreso}")
        negocio_formulario.empresa = empresa_regreso or empresa
        negocio_formulario.rtm = rtm_regreso
        negocio_formulario.expe = expe_regreso
        
        # Intentar cargar el negocio existente para mostrar todos los datos
        try:
            negocio_existente = Negocio.objects.get(
                empresa=empresa_regreso or empresa,
                rtm=rtm_regreso,
                expe=expe_regreso
            )
            logger.info(f"Negocio encontrado al regresar: {negocio_existente}")
            negocio_formulario = negocio_existente
        except Negocio.DoesNotExist:
            logger.info("No se encontró negocio existente, usando valores básicos")
    else:
        # Sin parámetros de regreso, usar valores por defecto
        negocio_formulario.empresa = empresa
        logger.info("Sin parámetros de regreso, usando formulario limpio")
    
    return render(request, 'maestro_negocios.html', {
        'actividades': actividades,
        'mensaje': mensaje,
        'exito': exito,
        'negocio': negocio_formulario,  # Objeto Negocio con valores mantenidos
        'empresa': empresa,
        'municipio_descripcion': municipio_descripcion
    })

def maestro_negocios_simple(request):
    """Vista para la versión simple del formulario maestro_negocios (sin mapa)"""
    from tributario.models import Actividad
    
    # Obtener código de municipio de la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Obtener actividades filtradas por municipio
    actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
    
    # Obtener negocio si se proporciona en la URL
    negocio = None
    if request.GET.get('empresa') and request.GET.get('rtm') and request.GET.get('expe'):
        try:
            negocio = Negocio.objects.get(
                empresa=request.GET.get('empresa'),
                rtm=request.GET.get('rtm'),
                expe=request.GET.get('expe')
            )
        except Negocio.DoesNotExist:
            pass
    
    return render(request, 'maestro_negocios_simple.html', {
        'empresa': empresa,
        'actividades': actividades,
        'negocio': negocio
    })

def maestro_negocios_corregido(request):
    """Vista para la versión corregida del formulario maestro_negocios (con mapa corregido)"""
    from tributario.models import Actividad
    
    # Obtener código de municipio de la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Obtener actividades filtradas por municipio
    actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
    
    # Obtener negocio si se proporciona en la URL
    negocio = None
    if request.GET.get('empresa') and request.GET.get('rtm') and request.GET.get('expe'):
        try:
            negocio = Negocio.objects.get(
                empresa=request.GET.get('empresa'),
                rtm=request.GET.get('rtm'),
                expe=request.GET.get('expe')
            )
        except Negocio.DoesNotExist:
            pass
    
    return render(request, 'maestro_negocios_corregido.html', {
        'empresa': empresa,
        'actividades': actividades,
        'negocio': negocio
    })

def maestro_negocios_simple_v2(request):
    """Vista para la versión simplificada del formulario maestro_negocios (funciona como antes)"""
    from tributario.models import Actividad
    
    # Obtener código de municipio de la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Obtener actividades filtradas por municipio
    actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
    
    # Obtener negocio si se proporciona en la URL
    negocio = None
    if request.GET.get('empresa') and request.GET.get('rtm') and request.GET.get('expe'):
        try:
            negocio = Negocio.objects.get(
                empresa=request.GET.get('empresa'),
                rtm=request.GET.get('rtm'),
                expe=request.GET.get('expe')
            )
        except Negocio.DoesNotExist:
            pass
    
    return render(request, 'maestro_negocios_simple_v2.html', {
        'empresa': empresa,
        'actividades': actividades,
        'negocio': negocio
    })


def cierre_anual(request):
    return render(request, 'cierre_anual.html')

def cargo_anual(request):
    return render(request, 'cargo_anual.html')

def recargos_moratorios(request):
    return render(request, 'recargos_moratorios.html')

def informes(request):
    return render(request, 'informes.html')

def buscar_negocio(request):
    empresa = request.GET.get('empresa')
    rtm = request.GET.get('rtm')
    expe = request.GET.get('expe')
    
    logger.info(f"Valores recibidos: empresa={empresa}, rtm={rtm}, expe={expe}")
    
    # Validar que todos los campos estén presentes
    if not empresa or not rtm or not expe:
        logger.warning("Faltan campos obligatorios")
        return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)
    
    try:
        # Buscar el negocio en la base de datos
        negocio = Negocio.objects.get(empresa=empresa, rtm=rtm, expe=expe)
        logger.info(f"Negocio encontrado: {negocio}")
        logger.info(f"Coordenadas del negocio - CX: {negocio.cx}, CY: {negocio.cy}")
        
        # Serializar los datos
        serializer = NegocioSerializer(negocio)
        data = serializer.data
        
        # Convertir coordenadas UTM a lat/lng para mostrar en el mapa
        if negocio.cx and negocio.cy and float(negocio.cx) != 0 and float(negocio.cy) != 0:
            try:
                # Las coordenadas en BD están en UTM, convertir a lat/lng
                lat, lng = utm_to_latlng(float(negocio.cx), float(negocio.cy))
                if lat is not None and lng is not None:
                    # Para el mapa: cx = lng, cy = lat
                    data['cx'] = str(lng)
                    data['cy'] = str(lat)
                    logger.info(f"Coordenadas UTM convertidas a lat/lng - Lat: {lat:.7f}, Lng: {lng:.7f}")
                else:
                    # Si falla la conversión, usar las coordenadas originales
                    data['cx'] = str(negocio.cx)
                    data['cy'] = str(negocio.cy)
                    logger.warning("Error en conversión UTM a lat/lng, usando coordenadas originales")
            except Exception as e:
                logger.error(f"Error al convertir coordenadas UTM a lat/lng: {str(e)}")
                data['cx'] = str(negocio.cx) if negocio.cx else '0.0000000'
                data['cy'] = str(negocio.cy) if negocio.cy else ''
        else:
            data['cx'] = '0.0000000'
            data['cy'] = ''
        
        logger.info(f"Datos serializados: {data}")
        logger.info(f"Coordenadas en respuesta (lat/lng para mapa) - CX: {data.get('cx')}, CY: {data.get('cy')}")
        
        return JsonResponse(data, safe=False)
        
    except Negocio.DoesNotExist:
        logger.warning(f"No se encontró negocio con empresa={empresa}, rtm={rtm}, expe={expe}")
        return JsonResponse({'error': 'Negocio no encontrado'}, status=404)
    except Exception as e:
        logger.error(f"Error al buscar negocio: {str(e)}")
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

def convertir_utm_a_latlng(request):
    """
    Endpoint para convertir coordenadas UTM a lat/lng
    Útil para el frontend cuando necesita mostrar coordenadas UTM en el mapa
    """
    easting = request.GET.get('easting')
    northing = request.GET.get('northing')
    
    if not easting or not northing:
        return JsonResponse({'error': 'Se requieren easting y northing'}, status=400)
    
    try:
        easting_float = float(easting)
        northing_float = float(northing)
        
        lat, lng = utm_to_latlng(easting_float, northing_float)
        
        if lat is not None and lng is not None:
            return JsonResponse({
                'lat': lat,
                'lng': lng,
                'success': True
            })
        else:
            return JsonResponse({'error': 'Error en la conversión'}, status=500)
            
    except (ValueError, TypeError) as e:
        return JsonResponse({'error': f'Coordenadas inválidas: {str(e)}'}, status=400)
    except Exception as e:
        logger.error(f"Error al convertir UTM a lat/lng: {str(e)}")
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

def cargar_actividades(request):
    empresa = request.GET.get('empresa')
    
    if not empresa:
        return JsonResponse({'error': 'Empresa es requerida'}, status=400)
    
    try:
        # Filtrar actividades por empresa y ordenar por código
        actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
        
        # Convertir a lista de diccionarios
        actividades_data = []
        for actividad in actividades:
            actividades_data.append({
                'codigo': actividad.codigo,
                'descripcion': actividad.descripcion
            })
        
        logger.info(f"Actividades cargadas para empresa {empresa}: {len(actividades_data)} actividades")
        return JsonResponse({'actividades': actividades_data}, safe=False)
        
    except Exception as e:
        logger.error(f"Error al cargar actividades: {str(e)}")
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

@csrf_exempt
def enviar_a_caja(request):
    """Vista AJAX para enviar transacción a caja e insertar en pagovariostemp"""
    if request.method == 'POST':
        try:
            from datetime import datetime
            from decimal import Decimal
            from tributario.models import PagoVariosTemp, NoRecibos
            
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
            numero_recibo_decimal = NoRecibos.obtener_siguiente_numero()
            numero_recibo = f"REC-{numero_recibo_decimal}"
            
            # Log para debug
            logger.info(f"Enviando a caja - Empresa: {empresa}, Oficina: {oficina}, DNI: {dni}, Nombre: {nombre}")
            
            # Procesar conceptos del formulario
            conceptos_procesados = []
            total_general = Decimal('0.00')
            
            # Buscar todos los conceptos en el formulario
            i = 0
            while True:
                codigo = request.POST.get(f'form-{i}-codigo', '').strip()
                if not codigo:  # Si no hay más conceptos
                    break
                
                descripcion = request.POST.get(f'form-{i}-descripcion', '').strip()
                cantidad = request.POST.get(f'form-{i}-cantidad', '1').strip()
                vl_unit = request.POST.get(f'form-{i}-vl_unit', '0').strip()
                valor = request.POST.get(f'form-{i}-valor', '0').strip()
                
                if codigo and valor and float(valor.replace(',', '.')) > 0:
                    try:
                        cantidad_decimal = Decimal(cantidad.replace(',', '.')) if cantidad else Decimal('1.00')
                        vl_unit_decimal = Decimal(vl_unit.replace(',', '.')) if vl_unit else Decimal('0.00')
                        valor_decimal = Decimal(valor.replace(',', '.')) if valor else Decimal('0.00')
                        
                        # Crear registro en pagovariostemp con TODOS los campos del modelo
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
                        
                        # Log para debug
                        logger.info(f"Concepto guardado - Recibo: {numero_recibo}, Código: {codigo}, Oficina: {oficina}")
                        
                    except Exception as e:
                        return JsonResponse({
                            'exito': False,
                            'mensaje': f'Error al procesar concepto {codigo}: {str(e)}'
                        })
                
                i += 1
            
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
            logger.error(f"Error al enviar a caja: {str(e)}")
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
    """Genera el soporte de transacción con QR"""
    if request.method == 'POST':
        try:
            logger.info("Iniciando generación de soporte de transacción")
            
            # Obtener datos del formulario
            numero_recibo = request.POST.get('numero_recibo')
            dni = request.POST.get('dni')
            nombre = request.POST.get('nombre')
            direccion = request.POST.get('direccion')
            comentario = request.POST.get('comentario')
            conceptos = request.POST.getlist('conceptos[]')
            
            logger.info(f"Datos recibidos - Recibo: {numero_recibo}, DNI: {dni}, Nombre: {nombre}")
            logger.info(f"Conceptos recibidos: {len(conceptos)}")
            
            # Validar datos requeridos
            if not numero_recibo:
                logger.error("Número de recibo no proporcionado")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Número de recibo es requerido'
                })
            
            # Generar QR con información de la transacción
            logger.info("Generando QR code")
            qr_data = f"Transacción: {numero_recibo}\nNombre: {nombre}\nDNI: {dni}"
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Crear imagen QR en SVG (evita dependencia PIL/_imaging)
            from qrcode.image.svg import SvgPathImage
            img = qrcode.make(qr_data, image_factory=SvgPathImage, box_size=8, border=2)

            # Convertir a base64 para mostrar en HTML
            buffer = io.BytesIO()
            img.save(buffer)
            qr_svg_b64 = base64.b64encode(buffer.getvalue()).decode()
            qr_data_uri = f"data:image/svg+xml;base64,{qr_svg_b64}"
            logger.info("QR code generado exitosamente")
            
            # Preparar datos para el template
            conceptos_data = []
            total_general = 0
            for i, concepto_str in enumerate(conceptos):
                if concepto_str:
                    logger.info(f"Procesando concepto {i}: {concepto_str}")
                    # Parsear el concepto (formato: codigo|descripcion|valor)
                    partes = concepto_str.split('|')
                    if len(partes) >= 3:
                        try:
                            # Función auxiliar para convertir string a float manejando comas y puntos
                            def parse_float(value):
                                if not value:
                                    return 0.0
                                # Convertir comas a puntos para compatibilidad
                                if isinstance(value, str):
                                    value = value.replace(',', '.')
                                return float(value)
                            
                            valor = parse_float(partes[2])
                            total_general += valor
                            conceptos_data.append({
                                'codigo': partes[0],
                                'descripcion': partes[1],
                                'valor': partes[2]
                            })
                            logger.info(f"Concepto procesado: {partes[0]} - {partes[1]} - {partes[2]}")
                        except (ValueError, TypeError) as e:
                            logger.error(f"Error al procesar valor del concepto: {e}")
                            continue
                    else:
                        logger.warning(f"Concepto mal formateado: {concepto_str}")
            
            logger.info(f"Total conceptos procesados: {len(conceptos_data)}, Total: {total_general}")
            
            context = {
                'numero_recibo': numero_recibo,
                'dni': dni or '',
                'nombre': nombre or '',
                'direccion': direccion or '',
                'comentario': comentario or '',
                'conceptos': conceptos_data,
                'total_general': f"{total_general:.2f}",
                'qr_code': '',
                'qr_data_uri': qr_data_uri,
                'fecha': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            }
            
            logger.info("Renderizando template de soporte")
            # Renderizar template de soporte
            html_content = render_to_string('soporte_transaccion.html', context)
            logger.info(f"Template renderizado, longitud HTML: {len(html_content)}")
            
            return HttpResponse(html_content, content_type='text/html')
            
        except Exception as e:
            logger.error(f"Error al generar soporte: {str(e)}", exc_info=True)
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error al generar soporte: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

def buscar_identificacion(request):
    identidad = request.GET.get('identidad')
    if not identidad:
        return JsonResponse({'error': 'No se proporcionó identidad'}, status=400)
    try:
        identificacion = Identificacion.objects.get(identidad=identidad)
        return JsonResponse({
            'encontrado': True,
            'nombres': identificacion.nombres or '',
            'apellidos': identificacion.apellidos or '',
        })
    except Identificacion.DoesNotExist:
        return JsonResponse({'encontrado': False})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def buscar_actividad(request):
    """Vista AJAX para buscar actividad por empresa y código"""
    from tributario.models import Actividad
    
    try:
        empresa = request.GET.get('empresa', '').strip()
        codigo = request.GET.get('codigo', '').strip()
        
        if not empresa or not codigo:
            return JsonResponse({
                'exito': False,
                'existe': False,
                'descripcion': '',
                'mensaje': 'Empresa y código son obligatorios'
            })
        
        # Buscar la actividad
        act = Actividad.objects.filter(empresa=empresa, codigo=codigo).first()
        if act:
            return JsonResponse({
                'exito': True,
                'existe': True,
                'descripcion': act.descripcion or '',
                'mensaje': 'Actividad encontrada'
            })
        else:
            return JsonResponse({
                'exito': True,
                'existe': False,
                'descripcion': '',
                'mensaje': 'Actividad no encontrada'
            })
            
    except Exception as e:
        logger.error(f"Error en buscar_actividad: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'exito': False,
            'existe': False,
            'descripcion': '',
            'mensaje': f'Error al buscar actividad: {str(e)}'
        }, status=500)

@require_GET
def buscar_oficina(request):
    from tributario.models import Oficina
    
    empresa = request.GET.get('empresa', '').strip()
    codigo = request.GET.get('codigo', '').strip()
    descripcion = ''
    existe = False
    
    logger.info(f"Buscando oficina - Empresa: '{empresa}', Código: '{codigo}'")
    
    if empresa and codigo:
        try:
            ofi = Oficina.objects.filter(empresa=empresa, codigo=codigo).first()
            if ofi:
                descripcion = ofi.descripcion or ''
                existe = True
                logger.info(f"Oficina encontrada: {empresa}-{codigo}, Descripción: '{descripcion}'")
            else:
                logger.info(f"Oficina no encontrada: {empresa}-{codigo}")
        except Exception as e:
            logger.error(f"Error al buscar oficina: {str(e)}")
    else:
        logger.warning(f"Datos incompletos para búsqueda - Empresa: '{empresa}', Código: '{codigo}'")
    
    response_data = {'descripcion': descripcion, 'existe': existe}
    logger.info(f"Respuesta: {response_data}")
    return JsonResponse(response_data)

def actividad_crud(request):
    from tributario.models import Actividad
    mensaje = None
    exito = False
    actividad = None
    empresa_filtro = ''
    confirm_actualizar = False
    show_confirm_script = False
    show_confirm_delete_script = False
    if request.method == 'POST':
        accion = request.POST.get('accion', '')
        logger.info(f"Acción recibida: {accion}")
        
        if accion == 'guardar':
            empresa = request.POST.get('empresa', '').strip()
            codigo = request.POST.get('codigo', '').strip()
            cuenta = request.POST.get('cuenta', '').strip()  # Capturar cuenta también
            descripcion = request.POST.get('descripcion', '').strip()
            cuentarez = request.POST.get('cuentarez', '').strip()
            cuentarec = request.POST.get('cuentarec', '').strip()
            cuentaint = request.POST.get('cuentaint', '').strip()
            
            logger.info(f"Guardando actividad - Empresa: {empresa}, Código: {codigo}, Cuenta: {cuenta}, Descripción: {descripcion}")
            logger.info(f"POST data: {request.POST}")
            
            # Usar valores por defecto si están vacíos
            if not empresa:
                empresa = request.session.get('empresa', '0301')
            
            if not codigo and cuenta:
                codigo = cuenta
            
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
                form = ActividadForm(request.POST)
                actividades = Actividad.objects.filter(empresa=empresa).order_by('-id') if empresa else []
                return render(request, 'actividad.html', {
                    'form': form,
                    'actividades': actividades,
                    'mensaje': mensaje,
                    'exito': exito,
                    'actividad': None,
                    'empresa_filtro': empresa,
                    'confirm_actualizar': False,
                    'show_confirm_script': False,
                    'show_confirm_delete_script': False,
                })
            
            # GUARDAR - Validación pasada
            try:
                if codigo:
                    actividad, created = Actividad.objects.get_or_create(
                        empresa=empresa,
                        codigo=codigo,
                        defaults={
                            'descripcion': descripcion,
                            'cuentarez': cuentarez,
                            'cuentarec': cuentarec,
                            'cuentaint': cuentaint
                        }
                    )
                    
                    if created:
                        mensaje = f'Actividad creada correctamente. Código: {codigo}, Empresa: {empresa}'
                        exito = True
                        logger.info(f"Nueva actividad creada: {empresa}-{codigo}")
                    else:
                        # Actualizar todos los campos
                        actividad.descripcion = descripcion
                        actividad.cuentarez = cuentarez
                        actividad.cuentarec = cuentarec
                        actividad.cuentaint = cuentaint
                        actividad.save()
                        mensaje = f'Actividad actualizada correctamente. Código: {codigo}, Empresa: {empresa}'
                        exito = True
                        logger.info(f"Actividad actualizada: {empresa}-{codigo}")
                else:
                    mensaje = 'Error: El código/cuenta es necesario para guardar'
                    exito = False
                    
            except Exception as e:
                mensaje = f'Error al guardar actividad: {str(e)}'
                exito = False
                logger.error(f"Error al guardar actividad: {str(e)}")
            
            # Preparar formulario limpio manteniendo empresa
            form = ActividadForm(initial={'empresa': empresa})
            actividades = Actividad.objects.filter(empresa=empresa).order_by('-id')
            empresa_filtro = empresa
            
            # Renderizar la página con los datos actualizados
            return render(request, 'actividad.html', {
                'form': form,
                'actividades': actividades,
                'mensaje': mensaje,
                'exito': exito,
                'actividad': None,
                'empresa': empresa_filtro,
                'empresa_filtro': empresa_filtro,
                'confirm_actualizar': False,
                'show_confirm_script': False,
                'show_confirm_delete_script': False,
            })
        elif accion == 'eliminar':
            empresa = request.POST.get('empresa', '').strip()
            codigo = request.POST.get('codigo', '').strip()
            
            logger.info(f"Eliminando actividad - Empresa: {empresa}, Código: {codigo}")
            logger.info(f"POST data eliminar: {request.POST}")
            
            # Buscar y eliminar la actividad
            try:
                actividad_a_eliminar = Actividad.objects.get(empresa=empresa, codigo=codigo)
                actividad_a_eliminar.delete()
                mensaje = f'Actividad eliminada correctamente. Código: {codigo}, Empresa: {empresa}'
                exito = True
                logger.info(f"Actividad eliminada: {empresa}-{codigo}")
            except Actividad.DoesNotExist:
                mensaje = f'No se encontró la actividad con código {codigo} y empresa {empresa}'
                exito = False
                logger.warning(f"Actividad no encontrada para eliminar: {empresa}-{codigo}")
            except Exception as e:
                mensaje = f'Error al eliminar actividad: {str(e)}'
                exito = False
                logger.error(f"Error al eliminar actividad: {str(e)}")
            
            # Preparar formulario limpio manteniendo empresa
            form = ActividadForm(initial={'empresa': empresa})
            actividades = Actividad.objects.filter(empresa=empresa).order_by('-id')
            empresa_filtro = empresa
            
            # Renderizar la página con los datos actualizados
            return render(request, 'actividad.html', {
                'form': form,
                'actividades': actividades,
                'mensaje': mensaje,
                'exito': exito,
                'actividad': None,
                'empresa': empresa_filtro,
                'empresa_filtro': empresa_filtro,
                'confirm_actualizar': False,
                'show_confirm_script': False,
                'show_confirm_delete_script': False,
            })
        elif accion == 'nuevo':
            empresa = request.POST.get('empresa', '').strip()
            logger.info(f"Nuevo - Empresa: {empresa}")
            
            # Preparar formulario limpio manteniendo empresa
            form = ActividadForm(initial={'empresa': empresa})
            actividades = Actividad.objects.filter(empresa=empresa).order_by('-id')
            empresa_filtro = empresa
            
            # Renderizar la página con formulario limpio
            return render(request, 'actividad.html', {
                'form': form,
                'actividades': actividades,
                'mensaje': None,
                'exito': False,
                'actividad': None,
                'empresa': empresa_filtro,
                'empresa_filtro': empresa_filtro,
                'confirm_actualizar': False,
                'show_confirm_script': False,
                'show_confirm_delete_script': False,
            })
        # La acción 'salir' ya no se maneja aquí porque ahora usamos enlaces directos
        else:
            empresa_filtro = request.POST.get('empresa', '')
        form = ActividadForm(request.POST)
    else:
        empresa_filtro = request.GET.get('empresa', '')
        # Heredar municipio de la sesión si no hay filtro
        if not empresa_filtro:
            empresa_filtro = request.session.get('empresa', '')
        # Inicializar formulario con municipio de la sesión
        initial_data = {}
        if empresa_filtro:
            initial_data['empresa'] = empresa_filtro
        form = ActividadForm(instance=actividad, initial=initial_data)
    actividades = Actividad.objects.filter(empresa=empresa_filtro).order_by('-id') if empresa_filtro else []
    return render(request, 'actividad.html', {
        'form': form,
        'actividades': actividades,
        'mensaje': mensaje,
        'exito': exito,
        'actividad': actividad,
        'empresa_filtro': empresa_filtro,
        'confirm_actualizar': confirm_actualizar,
        'show_confirm_script': show_confirm_script,
        'show_confirm_delete_script': show_confirm_delete_script,
    })

def oficina_crud(request):
    from tributario.models import Oficina
    from .forms import OficinaForm
    mensaje = None
    exito = False
    oficina = None
    empresa_filtro = ''
    confirm_actualizar = False
    show_confirm_script = False
    show_confirm_delete_script = False
    if request.method == 'POST':
        accion = request.POST.get('accion', '')
        logger.info(f"Acción recibida: {accion}")
        
        if accion == 'guardar':
            empresa = request.POST.get('empresa', '').strip()
            codigo = request.POST.get('codigo', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            
            logger.info(f"Guardando oficina - Empresa: {empresa}, Código: {codigo}, Descripción: {descripcion}")
            logger.info(f"POST data: {request.POST}")
            
            # Validar campos obligatorios
            if not empresa or not codigo or not descripcion:
                mensaje = 'Todos los campos son obligatorios.'
                exito = False
                form = OficinaForm(request.POST)
                oficinas = Oficina.objects.filter(empresa=empresa).order_by('codigo') if empresa else []
                return render(request, 'oficina.html', {
                    'form': form,
                    'oficinas': oficinas,
                    'mensaje': mensaje,
                    'exito': exito,
                    'oficina': None,
                    'empresa': empresa,
                    'empresa_filtro': empresa,
                    'confirm_actualizar': False,
                    'show_confirm_script': False,
                    'show_confirm_delete_script': False,
                })
            
            # Usar get_or_create para manejar la restricción UNIQUE
            try:
                oficina, created = Oficina.objects.get_or_create(
                    empresa=empresa,
                    codigo=codigo,
                    defaults={'descripcion': descripcion}
                )
                
                if created:
                    # Se creó una nueva oficina
                    mensaje = f'Oficina creada correctamente. Código: {codigo}, Empresa: {empresa}'
                    exito = True
                    logger.info(f"Nueva oficina creada: {empresa}-{codigo}")
                else:
                    # La oficina ya existía, actualizar la descripción
                    oficina.descripcion = descripcion
                    oficina.save()
                    mensaje = f'Oficina actualizada correctamente. Código: {codigo}, Empresa: {empresa}'
                    exito = True
                    logger.info(f"Oficina actualizada: {empresa}-{codigo}")
                    
            except Exception as e:
                # Manejar cualquier otro error
                mensaje = f'Error al guardar oficina: {str(e)}'
                exito = False
                logger.error(f"Error al guardar oficina: {str(e)}")
            
            # Preparar formulario limpio manteniendo empresa
            form = OficinaForm(initial={'empresa': empresa})
            oficinas = Oficina.objects.filter(empresa=empresa).order_by('codigo')
            empresa_filtro = empresa
            
            # Renderizar la página con los datos actualizados
            return render(request, 'oficina.html', {
                'form': form,
                'oficinas': oficinas,
                'mensaje': mensaje,
                'exito': exito,
                'oficina': None,
                'empresa': empresa_filtro,
                'empresa_filtro': empresa_filtro,
                'confirm_actualizar': False,
                'show_confirm_script': False,
                'show_confirm_delete_script': False,
            })
        elif accion == 'eliminar':
            empresa = request.POST.get('empresa', '').strip()
            codigo = request.POST.get('codigo', '').strip()
            
            logger.info(f"Eliminando oficina - Empresa: {empresa}, Código: {codigo}")
            logger.info(f"POST data eliminar: {request.POST}")
            
            # Buscar y eliminar la oficina
            try:
                oficina_a_eliminar = Oficina.objects.get(empresa=empresa, codigo=codigo)
                oficina_a_eliminar.delete()
                mensaje = f'Oficina eliminada correctamente. Código: {codigo}, Empresa: {empresa}'
                exito = True
                logger.info(f"Oficina eliminada: {empresa}-{codigo}")
            except Oficina.DoesNotExist:
                mensaje = f'No se encontró la oficina con código {codigo} y empresa {empresa}'
                exito = False
                logger.warning(f"Oficina no encontrada para eliminar: {empresa}-{codigo}")
            except Exception as e:
                mensaje = f'Error al eliminar oficina: {str(e)}'
                exito = False
                logger.error(f"Error al eliminar oficina: {str(e)}")
            
            # Preparar formulario limpio manteniendo empresa
            form = OficinaForm(initial={'empresa': empresa})
            oficinas = Oficina.objects.filter(empresa=empresa).order_by('codigo')
            empresa_filtro = empresa
            
            # Renderizar la página con los datos actualizados
            return render(request, 'oficina.html', {
                'form': form,
                'oficinas': oficinas,
                'mensaje': mensaje,
                'exito': exito,
                'oficina': None,
                'empresa': empresa_filtro,
                'empresa_filtro': empresa_filtro,
                'confirm_actualizar': False,
                'show_confirm_script': False,
                'show_confirm_delete_script': False,
            })
        elif accion == 'nuevo':
            empresa = request.POST.get('empresa', '').strip()
            logger.info(f"Nuevo - Empresa: {empresa}")
            
            # Preparar formulario limpio manteniendo empresa
            form = OficinaForm(initial={'empresa': empresa})
            oficinas = Oficina.objects.filter(empresa=empresa).order_by('codigo')
            empresa_filtro = empresa
            
            # Renderizar la página con formulario limpio
            return render(request, 'oficina.html', {
                'form': form,
                'oficinas': oficinas,
                'mensaje': None,
                'exito': False,
                'oficina': None,
                'empresa': empresa_filtro,
                'empresa_filtro': empresa_filtro,
                'confirm_actualizar': False,
                'show_confirm_script': False,
                'show_confirm_delete_script': False,
            })
        # La acción 'salir' ya no se maneja aquí porque ahora usamos enlaces directos
        else:
            empresa_filtro = request.POST.get('empresa', '')
        form = OficinaForm(request.POST)
    else:
        empresa_filtro = request.GET.get('empresa', '')
        # Heredar municipio de la sesión si no hay filtro
        if not empresa_filtro:
            empresa_filtro = request.session.get('empresa', '')
        # Inicializar formulario con municipio de la sesión
        initial_data = {}
        if empresa_filtro:
            initial_data['empresa'] = empresa_filtro
        form = OficinaForm(instance=oficina, initial=initial_data)
    oficinas = Oficina.objects.filter(empresa=empresa_filtro).order_by('codigo') if empresa_filtro else []
    return render(request, 'oficina.html', {
        'form': form,
        'oficinas': oficinas,
        'mensaje': mensaje,
        'exito': exito,
        'oficina': oficina,
        'empresa': empresa_filtro,
        'empresa_filtro': empresa_filtro,
        'confirm_actualizar': confirm_actualizar,
        'show_confirm_script': show_confirm_script,
        'show_confirm_delete_script': show_confirm_delete_script,
    })

def _buscar_rubro_helper(empresa, codigo):
    """Función helper para buscar rubros y retornar datos estandarizados"""
    from tributario.models import Rubro, RubroMoratorioConfig
    rubro = Rubro.objects.get(empresa=empresa, codigo=codigo)
    cfg = RubroMoratorioConfig.objects.filter(empresa=empresa, rubro_codigo=rubro.codigo, activo=True).first()
    return {
        'codigo': rubro.codigo,
        'descripcion': rubro.descripcion or '',
        'tipo': rubro.tipo or '',
        'cuenta': rubro.cuenta or '',
        'cuentarez': rubro.cuentarez or '',
        'moratorio': {
            'es_moratorio': bool(cfg),
            'rubro_padre_codigo': (cfg.rubro_padre_codigo if cfg else ''),
            'tasa_recargo_mensual': (str(cfg.tasa_recargo_mensual) if cfg else ''),
            'tasa_interes_mensual': (str(cfg.tasa_interes_mensual) if cfg else ''),
            'aplica_modulo': (cfg.aplica_modulo if cfg else 'AMBOS'),
            'activo': (bool(cfg.activo) if cfg else False),
        }
    }

@csrf_exempt
def buscar_rubro(request):
    """Vista AJAX optimizada para buscar rubros por empresa y código"""
    if request.method not in ['POST', 'GET']:
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        # Obtener datos según el método
        if request.method == 'POST':
            codigo = request.POST.get('codigo', '').strip()
            empresa = request.POST.get('empresa', '').strip()
        else:  # GET
            codigo = request.GET.get('codigo', '').strip()
            empresa = request.GET.get('empresa', '').strip()
        
        print(f"🔍 Buscando rubro: empresa={empresa}, codigo={codigo}")
        
        # Validar campos requeridos
        if not codigo or not empresa:
            print("❌ Código o empresa vacíos")
            return JsonResponse({
                'exito': False,
                'mensaje': 'Código y empresa son requeridos'
            })
        
        # Buscar el rubro usando la función helper
        rubro_data = _buscar_rubro_helper(empresa, codigo)
        print(f"✅ Rubro encontrado: {rubro_data}")
        
        return JsonResponse({
            'exito': True,
            'rubro': rubro_data,
            'mensaje': 'Rubro encontrado'
        })
        
    except Exception as e:
        print(f"❌ Error en búsqueda AJAX: {e}")
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al buscar rubro: {str(e)}'
        })

def rubros_crud(request):
    """Vista principal para el CRUD de rubros"""
    from .forms import RubroForm
    from tributario.models import Rubro, Actividad, RubroMoratorioConfig
    
    # Obtener el código de empresa de la sesión
    empresa = request.session.get('empresa', '0301')
    
    mensaje = None
    exito = False
    form = RubroForm(initial={'empresa': empresa})
    
    if request.method == 'POST':
        # Debug: mostrar todos los parámetros recibidos
        print(f"[DEBUG] Parámetros POST recibidos: {dict(request.POST)}")
        
        # Verificar si es una acción específica (eliminar o editar)
        action = request.POST.get('action', '')
        is_update = request.POST.get('is_update', '')
        
        print(f"[DEBUG] Action detectada: '{action}', is_update: '{is_update}'")
        print(f"[DEBUG] Condición eliminación: {action == 'eliminar'}")
        print(f"[DEBUG] Condición edición: {action == 'editar' and is_update == 'true'}")
        
        if action == 'eliminar':
            # Manejar eliminación de rubro
            empresa_eliminar = request.POST.get('empresa_eliminar', '').strip()
            codigo_eliminar = request.POST.get('codigo_eliminar', '').strip()
            
            # Debug para ver qué parámetros se están recibiendo
            print(f"[DEBUG] Eliminando rubro - empresa_eliminar: '{empresa_eliminar}', codigo_eliminar: '{codigo_eliminar}'")
            print(f"[DEBUG] Todos los parámetros POST: {dict(request.POST)}")
            
            if not empresa_eliminar:
                mensaje = f"❌ Empresa no encontrada para eliminar el rubro."
                exito = False
            elif not codigo_eliminar:
                mensaje = f"❌ Código no encontrado para eliminar el rubro."
                exito = False
            else:
                # Ambos campos están presentes, proceder con la eliminación
                try:
                    rubro_a_eliminar = Rubro.objects.get(
                        empresa=empresa_eliminar,
                        codigo=codigo_eliminar
                    )
                    rubro_a_eliminar.delete()
                    mensaje = f"✅ Rubro {codigo_eliminar} eliminado exitosamente."
                    exito = True
                except Rubro.DoesNotExist:
                    mensaje = f"❌ Rubro {codigo_eliminar} no encontrado."
                    exito = False
                except Exception as e:
                    mensaje = f"❌ Error al eliminar el rubro: {str(e)}"
                    exito = False
        elif action == 'editar' and is_update == 'true':
            # Manejar actualización de rubro
            try:
                codigo_original = request.POST.get('rubro_codigo_original')
                
                # Debug para ver qué parámetros se están recibiendo
                print(f"[DEBUG] Actualizando rubro - codigo_original: '{codigo_original}'")
                print(f"[DEBUG] Todos los parámetros POST: {dict(request.POST)}")
                
                if not codigo_original:
                    mensaje = "❌ Código original no encontrado para actualizar."
                    exito = False
                else:
                    # Código original encontrado, proceder con la actualización
                    rubro_a_editar = Rubro.objects.get(
                        empresa=request.POST.get('empresa'),
                        codigo=codigo_original
                    )
                    rubro_a_editar.descripcion = request.POST.get('descripcion', '')
                    rubro_a_editar.cuenta = request.POST.get('cuenta', '')
                    es_moratorio = (request.POST.get('es_moratorio') == 'on') or (request.POST.get('es_moratorio') == 'true')
                    rubro_a_editar.cuentarez = '' if es_moratorio else (request.POST.get('cuentarez', '') or '')
                    rubro_a_editar.tipo = request.POST.get('tipo', '')
                    rubro_a_editar.save()

                    # Upsert configuración moratoria
                    if es_moratorio:
                        RubroMoratorioConfig.objects.update_or_create(
                            empresa=rubro_a_editar.empresa,
                            rubro_codigo=rubro_a_editar.codigo,
                            defaults={
                                'rubro_padre_codigo': (request.POST.get('rubro_padre_codigo') or '').strip().upper(),
                                'tasa_recargo_mensual': (request.POST.get('tasa_recargo_mensual') or '0').strip() or '0',
                                'tasa_interes_mensual': (request.POST.get('tasa_interes_mensual') or '0').strip() or '0',
                                'aplica_modulo': (request.POST.get('aplica_modulo') or 'AMBOS').strip(),
                                'activo': True,
                                'usuario_modifica': request.session.get('usuario', '') or request.session.get('nombre', ''),
                            },
                        )
                    else:
                        RubroMoratorioConfig.objects.filter(
                            empresa=rubro_a_editar.empresa,
                            rubro_codigo=rubro_a_editar.codigo,
                        ).delete()

                    mensaje = f"✅ Rubro {rubro_a_editar.codigo} actualizado exitosamente."
                    exito = True
                    print(f"[DEBUG] Rubro actualizado exitosamente: {rubro_a_editar.codigo}")
            except Rubro.DoesNotExist:
                mensaje = f"❌ Rubro no encontrado para actualizar."
                exito = False
            except Exception as e:
                mensaje = f"❌ Error al actualizar el rubro: {str(e)}"
                exito = False
        else:
            # Manejar creación de rubro
            form = RubroForm(request.POST)
            if form.is_valid():
                try:
                    es_moratorio = (request.POST.get('es_moratorio') == 'on') or (request.POST.get('es_moratorio') == 'true')
                    # Verificar si ya existe el rubro antes de crear
                    empresa_form = form.cleaned_data.get('empresa')
                    codigo_form = form.cleaned_data.get('codigo')
                    
                    if Rubro.objects.filter(empresa=empresa_form, codigo=codigo_form).exists():
                        # Si existe, actualizar
                        rubro = Rubro.objects.get(empresa=empresa_form, codigo=codigo_form)
                        rubro.descripcion = form.cleaned_data.get('descripcion', '')
                        rubro.cuenta = form.cleaned_data.get('cuenta', '')
                        rubro.cuentarez = '' if es_moratorio else (form.cleaned_data.get('cuentarez', '') or '')
                        rubro.tipo = form.cleaned_data.get('tipo', '')
                        rubro.save()
                        mensaje = f"✅ Rubro {rubro.codigo} actualizado exitosamente."
                        exito = True
                    else:
                        # Si no existe, crear nuevo
                        rubro = form.save(commit=False)
                        rubro.empresa = empresa
                        if es_moratorio:
                            rubro.cuentarez = ''
                        rubro.save()
                        mensaje = f"✅ Rubro {rubro.codigo} guardado exitosamente."
                        exito = True

                    # Upsert / eliminar configuración moratoria acorde a checkbox
                    if es_moratorio:
                        RubroMoratorioConfig.objects.update_or_create(
                            empresa=rubro.empresa,
                            rubro_codigo=rubro.codigo,
                            defaults={
                                'rubro_padre_codigo': (request.POST.get('rubro_padre_codigo') or '').strip().upper(),
                                'tasa_recargo_mensual': (request.POST.get('tasa_recargo_mensual') or '0').strip() or '0',
                                'tasa_interes_mensual': (request.POST.get('tasa_interes_mensual') or '0').strip() or '0',
                                'aplica_modulo': (request.POST.get('aplica_modulo') or 'AMBOS').strip(),
                                'activo': True,
                                'usuario_crea': request.session.get('usuario', '') or request.session.get('nombre', ''),
                                'usuario_modifica': request.session.get('usuario', '') or request.session.get('nombre', ''),
                            },
                        )
                    else:
                        RubroMoratorioConfig.objects.filter(
                            empresa=rubro.empresa,
                            rubro_codigo=rubro.codigo,
                        ).delete()
                    
                    # Resetear formulario después de guardar
                    form = RubroForm(initial={'empresa': empresa})
                except Exception as e:
                    mensaje = f"❌ Error al guardar el rubro: {str(e)}"
                    exito = False
            else:
                # Mostrar errores específicos del formulario
                errores = []
                for field, errors in form.errors.items():
                    for error in errors:
                        if field == '__all__':
                            errores.append(error)
                        else:
                            campo_nombre = form.fields[field].label if field in form.fields else field
                            errores.append(f"{campo_nombre}: {error}")
                
                if errores:
                    mensaje = "❌ " + " | ".join(errores)
                else:
                    mensaje = "❌ Por favor, corrija los errores en el formulario."
                exito = False
    
    # Obtener todos los rubros de la empresa
    rubros = Rubro.objects.filter(empresa=empresa).order_by('codigo')

    # Configuración moratoria por rubro (para pintar en tabla / JS)
    cfgs = RubroMoratorioConfig.objects.filter(empresa=empresa, activo=True)
    moratorio_map = {c.rubro_codigo: c for c in cfgs}
    
    # Obtener todas las actividades de la empresa para los combobox
    actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
    
    return render(request, 'formulario_rubros.html', {
        'form': form,
        'rubros': rubros,
        'moratorio_map': moratorio_map,
        'actividades': actividades,
        'mensaje': mensaje,
        'exito': exito,
        'empresa': empresa
    })



def plan_arbitrio_crud(request):
    """Vista principal para el CRUD de plan de arbitrio"""
    from .forms import PlanArbitrioForm
    from tributario.models import PlanArbitrio, Rubro, Tarifas
    
    # Obtener el código de municipio de la sesión
    empresa = request.session.get('empresa')
    if not empresa:
        return redirect('tributario:tributario_login')
    
    # Obtener parámetros de la URL para pre-cargar datos
    codigo_rubro = request.GET.get('codigo_rubro', '')
    codigo_tarifa = request.GET.get('codigo_tarifa', '')
    ano_tarifa = request.GET.get('ano', '')
    
    mensaje = None
    exito = False
    mostrar_tipocat = False  # Flag para mostrar tipocat si tipomodulo=D
    
    if request.method == 'POST':
        print(f"[DEBUG] POST recibido - Datos: {request.POST}")
        print(f"[DEBUG] Datos específicos:")
        print(f"  - empresa: '{request.POST.get('empresa', '')}'")
        print(f"  - rubro: '{request.POST.get('rubro', '')}'")
        print(f"  - cod_tarifa: '{request.POST.get('cod_tarifa', '')}'")
        print(f"  - ano: '{request.POST.get('ano', '')}'")
        print(f"  - codigo: '{request.POST.get('codigo', '')}'")
        print(f"  - descripcion: '{request.POST.get('descripcion', '')}'")
        print(f"  - minimo: '{request.POST.get('minimo', '')}'")
        print(f"  - maximo: '{request.POST.get('maximo', '')}'")
        print(f"  - valor: '{request.POST.get('valor', '')}'")
        
        # Verificar si es una acción específica (eliminar o editar)
        action = request.POST.get('action', '')
        is_update = request.POST.get('is_update', '')
        print(f"[DEBUG] Acción detectada: '{action}'")
        print(f"[DEBUG] Es actualización: '{is_update}'")
        print(f"[DEBUG] Todos los parámetros POST recibidos:")
        for key, value in request.POST.items():
            print(f"  - {key}: '{value}'")
        
        if action == 'eliminar':
            # Manejar eliminación de plan
            empresa_eliminar = request.POST.get('empresa_eliminar', '').strip()
            rubro_eliminar = request.POST.get('rubro_eliminar', '').strip()
            cod_tarifa_eliminar = request.POST.get('cod_tarifa_eliminar', '').strip()
            ano_eliminar = request.POST.get('ano_eliminar', '').strip()
            codigo_eliminar = request.POST.get('codigo_eliminar', '').strip()
            tipocat_eliminar = request.POST.get('tipocat_eliminar', '').strip()
            
            print(f"[DEBUG] 🔴 ELIMINANDO PLAN:")
            print(f"  - empresa: '{empresa_eliminar}'")
            print(f"  - rubro: '{rubro_eliminar}'")
            print(f"  - cod_tarifa: '{cod_tarifa_eliminar}'")
            print(f"  - tipocat: '{tipocat_eliminar}'")
            print(f"  - ano: '{ano_eliminar}'")
            print(f"  - codigo: '{codigo_eliminar}'")
            
            if not all([empresa_eliminar, rubro_eliminar, cod_tarifa_eliminar, ano_eliminar, codigo_eliminar]):
                mensaje = "❌ Datos insuficientes para eliminar el plan."
                exito = False
                print(f"[DEBUG] ❌ Datos insuficientes para eliminar")
            else:
                try:
                    ano_int = int(ano_eliminar) if ano_eliminar else None
                    # CRÍTICO: tipocat es CHAR(1), usar string directamente ('1', '2', '3' o '')
                    tipocat_str = ''
                    if tipocat_eliminar:
                        import re
                        match = re.match(r'^([123])', tipocat_eliminar)
                        if match:
                            tipocat_str = match.group(1)  # '1', '2' o '3'
                    print(f"[DEBUG] Buscando plan con año: {ano_int}, tipocat: '{tipocat_str}'")
                    
                    # Construir filtros con tipocat si está presente
                    filtros_eliminar = {
                        'empresa': empresa_eliminar,
                        'rubro': rubro_eliminar,
                        'cod_tarifa': cod_tarifa_eliminar,
                        'ano': ano_int,
                        'codigo': codigo_eliminar
                    }
                    if tipocat_str:  # Solo incluir si tiene valor
                        filtros_eliminar['tipocat'] = tipocat_str
                    
                    plan_a_eliminar = PlanArbitrio.objects.get(**filtros_eliminar)
                    print(f"[DEBUG] ✅ Plan encontrado: ID={plan_a_eliminar.id}")
                    
                    plan_a_eliminar.delete()
                    mensaje = f"✅ Plan de arbitrio {codigo_eliminar} eliminado exitosamente."
                    exito = True
                    print(f"[DEBUG] ✅ Plan eliminado exitosamente")
                except PlanArbitrio.DoesNotExist:
                    mensaje = f"❌ No se encontró el plan con los criterios especificados."
                    exito = False
                    print(f"[DEBUG] ❌ Plan no encontrado para eliminar")
                except Exception as e:
                    mensaje = f"❌ Error al eliminar el plan: {str(e)}"
                    exito = False
                    print(f"[DEBUG] ❌ Error al eliminar: {e}")
            
            # Preparar formulario limpio
            form = PlanArbitrioForm(initial={'empresa': empresa})
            
        elif action == 'editar':
            # Manejar edición de plan - cargar datos existentes
            empresa_editar = request.POST.get('empresa_editar', '').strip()
            rubro_editar = request.POST.get('rubro_editar', '').strip()
            cod_tarifa_editar = request.POST.get('cod_tarifa_editar', '').strip()
            ano_editar = request.POST.get('ano_editar', '').strip()
            codigo_editar = request.POST.get('codigo_editar', '').strip()
            tipocat_editar = request.POST.get('tipocat_editar', '').strip()
            
            print(f"[DEBUG] 🔵 EDITANDO PLAN:")
            print(f"  - empresa: '{empresa_editar}'")
            print(f"  - rubro: '{rubro_editar}'")
            print(f"  - cod_tarifa: '{cod_tarifa_editar}'")
            print(f"  - tipocat: '{tipocat_editar}'")
            print(f"  - ano: '{ano_editar}'")
            print(f"  - codigo: '{codigo_editar}'")
            
            if not all([empresa_editar, rubro_editar, cod_tarifa_editar, ano_editar, codigo_editar]):
                mensaje = "❌ Datos insuficientes para editar el plan."
                exito = False
                form = PlanArbitrioForm(initial={'empresa': empresa})
                print(f"[DEBUG] ❌ Datos insuficientes para editar")
            else:
                try:
                    ano_int = int(ano_editar) if ano_editar else None
                    # CRÍTICO: tipocat es CHAR(1), usar string directamente ('1', '2', '3' o '')
                    tipocat_str_editar = ''
                    if tipocat_editar:
                        import re
                        match = re.match(r'^([123])', tipocat_editar)
                        if match:
                            tipocat_str_editar = match.group(1)  # '1', '2' o '3'
                    print(f"[DEBUG] Buscando plan con año: {ano_int}, tipocat: '{tipocat_str_editar}'")
                    
                    # Construir filtros con tipocat si está presente
                    filtros_editar = {
                        'empresa': empresa_editar,
                        'rubro': rubro_editar,
                        'cod_tarifa': cod_tarifa_editar,
                        'ano': ano_int,
                        'codigo': codigo_editar
                    }
                    if tipocat_str_editar:  # Solo incluir si tiene valor
                        filtros_editar['tipocat'] = tipocat_str_editar
                    
                    plan_a_editar = PlanArbitrio.objects.get(**filtros_editar)
                    print(f"[DEBUG] ✅ Plan encontrado: ID={plan_a_editar.id}")
                    
                    # Cargar los datos del plan en el formulario
                    # CRÍTICO: tipocat es CHAR(1), convertir a string
                    tipocat_editar_str = str(plan_a_editar.tipocat) if plan_a_editar.tipocat is not None and plan_a_editar.tipocat else ''
                    form = PlanArbitrioForm(initial={
                        'empresa': plan_a_editar.empresa,
                        'rubro': plan_a_editar.rubro,
                        'cod_tarifa': plan_a_editar.cod_tarifa,
                        'ano': plan_a_editar.ano,
                        'codigo': plan_a_editar.codigo,
                        'descripcion': plan_a_editar.descripcion,
                        'minimo': plan_a_editar.minimo,
                        'maximo': plan_a_editar.maximo,
                        'valor': plan_a_editar.valor,
                        'tipocat': tipocat_editar_str  # String: '1', '2', '3' o ''
                    })
                    mensaje = f"✅ Plan de arbitrio {codigo_editar} cargado para edición."
                    exito = True
                    print(f"[DEBUG] ✅ Plan cargado para edición")
                except PlanArbitrio.DoesNotExist:
                    mensaje = f"❌ No se encontró el plan con los criterios especificados."
                    exito = False
                    form = PlanArbitrioForm(initial={'empresa': empresa})
                    print(f"[DEBUG] ❌ Plan no encontrado para editar")
                except Exception as e:
                    mensaje = f"❌ Error al cargar el plan para edición: {str(e)}"
                    exito = False
                    form = PlanArbitrioForm(initial={'empresa': empresa})
                    print(f"[DEBUG] ❌ Error al cargar para editar: {e}")
        
        else:
            # Acción normal de guardar/crear o actualizar
            form = PlanArbitrioForm(request.POST)
            
            # DEBUG: Imprimir todos los datos POST recibidos ANTES de validar
            print(f"[DEBUG] ========== DATOS POST RECIBIDOS ==========")
            for key, value in request.POST.items():
                print(f"[DEBUG]   {key}: '{value}'")
            print(f"[DEBUG] ===========================================")
            
            print(f"[DEBUG] Formulario válido: {form.is_valid()}")
            if not form.is_valid():
                print(f"[DEBUG] Errores del formulario: {form.errors}")
            
            if form.is_valid():
                # Obtener los datos directamente del POST para asegurar que sean correctos
                empresa = request.POST.get('empresa', '').strip()
                rubro = request.POST.get('rubro', '').strip()
                cod_tarifa = request.POST.get('cod_tarifa', '').strip()
                ano = request.POST.get('ano', '').strip()
                codigo = request.POST.get('codigo', '').strip()
                
                print(f"[DEBUG] 🔍 VERIFICANDO EXISTENCIA DE REGISTRO:")
                print(f"  - empresa: '{empresa}'")
                print(f"  - rubro: '{rubro}'")
                print(f"  - cod_tarifa: '{cod_tarifa}'")
                print(f"  - ano: '{ano}'")
                print(f"  - codigo: '{codigo}'")
                print(f"  - is_update: '{is_update}'")
                
                # Obtener tipocat - PRIORIDAD a form.cleaned_data (más confiable)
                tipocat_post = request.POST.get('tipocat', '').strip()
                tipocat_form = ''
                if form.is_valid():
                    tipocat_form_raw = form.cleaned_data.get('tipocat', '')
                    tipocat_form = str(tipocat_form_raw) if tipocat_form_raw else ''
                    print(f"[DEBUG] 🔍 tipocat_form_raw (de cleaned_data): '{tipocat_form_raw}'")
                    print(f"[DEBUG] 🔍 tipocat_form (convertido): '{tipocat_form}'")
                
                print(f"[DEBUG] 🔍 tipocat_post (de POST directo): '{tipocat_post}'")
                
                # Usar tipocat del formulario si está disponible y no vacía, sino del POST
                tipocat = tipocat_form if tipocat_form else tipocat_post
                
                # Si tipocat está vacía, verificar si hay un select en el formulario (para tarifas domésticas)
                if not tipocat:
                    # Intentar obtener del campo del formulario directamente
                    tipocat_from_form_field = form.data.get('tipocat', '') if hasattr(form, 'data') else ''
                    if tipocat_from_form_field:
                        tipocat = str(tipocat_from_form_field).strip()
                        print(f"[DEBUG] 🔍 tipocat obtenida del form.data: '{tipocat}'")
                
                # CRÍTICO: tipocat es CHAR(1), extraer solo '1', '2' o '3' como string
                import re
                tipocat_str = ''
                if tipocat:
                    match = re.match(r'^([123])', tipocat)
                    if match:
                        tipocat_str = match.group(1)  # '1', '2' o '3'
                
                print(f"[DEBUG] 🔍 tipocat final usada: '{tipocat}' -> tipocat_str='{tipocat_str}'")
                print(f"[DEBUG] ⚠️ IMPORTANTE: Si tipocat_str está vacío y debería tener un valor, revisar que el campo se esté enviando desde el frontend")
                
                print(f"[DEBUG] ========== VERIFICACIÓN DE EXISTENCIA ==========")
                print(f"[DEBUG] 🔍 Todos los valores POST recibidos:")
                for key, value in request.POST.items():
                    if key == 'tipocat':
                        print(f"     ⚠️ {key}: '{value}' ← TIPOCAT (MUY IMPORTANTE)")
                    else:
                        print(f"     - {key}: '{value}'")
                print(f"[DEBUG] 🔍 tipocat recibida POST: '{tipocat_post}'")
                print(f"[DEBUG] 🔍 tipocat del form.cleaned_data: '{tipocat_form}'")
                print(f"[DEBUG] 🔍 tipocat final usada: '{tipocat}' -> tipocat_str='{tipocat_str}'")
                print(f"[DEBUG] ⚠️ IMPORTANTE: Se buscará registro con tipocat EXACTA='{tipocat_str}'")
                print(f"[DEBUG] ⚠️ Si existe un registro con tipocat='1' y se busca tipocat='2', NO debe encontrarlo")
                print(f"[DEBUG] ⚠️ Si tipocat_str='{tipocat_str}', solo debe encontrar registros con tipocat='{tipocat_str}' en la BD")
                
                # OBTENER tipomodulo DE LA TARIFA para aplicar la misma lógica que la búsqueda automática
                from decimal import Decimal
                from tributario.models import Tarifas
                
                try:
                    ano_int = int(ano) if ano else None
                    
                    # Obtener tipomodulo de la tarifa (igual que en búsqueda automática)
                    tipomodulo = ''
                    try:
                        if empresa and cod_tarifa and rubro and ano:
                            tarifa = Tarifas.objects.filter(
                                empresa=empresa,
                                cod_tarifa=cod_tarifa,
                                rubro=rubro,
                                ano=ano_int
                            ).first()
                        elif empresa and cod_tarifa:
                            tarifa = Tarifas.objects.filter(
                                empresa=empresa,
                                cod_tarifa=cod_tarifa
                            ).order_by('-ano').first()
                        else:
                            tarifa = None
                        
                        if tarifa:
                            tipomodulo = tarifa.tipomodulo or ''
                            print(f"[DEBUG] 🔍 tipomodulo obtenido de tarifa: '{tipomodulo}'")
                        else:
                            print(f"[DEBUG] ⚠️ Tarifa no encontrada, usando tipomodulo vacío")
                    except Exception as e:
                        print(f"[DEBUG] ⚠️ Error al obtener tipomodulo: {str(e)}")
                    
                    # APLICAR LA MISMA LÓGICA QUE LA BÚSQUEDA AUTOMÁTICA
                    # Si tipomodulo == 'D': incluir tipocat en filtros (OBLIGATORIO)
                    # Si tipomodulo != 'D': NO incluir tipocat en filtros (búsqueda sin tipocat)
                    
                    print(f"[DEBUG] ========== APLICANDO MISMA LÓGICA QUE BÚSQUEDA AUTOMÁTICA ==========")
                    print(f"[DEBUG] 🔍 tipomodulo: '{tipomodulo}'")
                    
                    if tipomodulo == 'D':
                        # VALIDACIÓN DOMÉSTICA: empresa, rubro, cod_tarifa, tipocat, ano, codigo
                        print(f"[DEBUG] 🔍 TARIFA DOMÉSTICA - TIPOCAT OBLIGATORIA")
                        
                        # Obtener tipocat del POST o form - PRIORIDAD AL POST (para filtros de búsqueda)
                        tipocat_post_busqueda = request.POST.get('tipocat', '').strip()
                        print(f"[DEBUG] 🔍 tipocat_post_busqueda (POST directo para búsqueda): '{tipocat_post_busqueda}'")
                        
                        # Si no está en POST, intentar obtener del form.cleaned_data
                        if not tipocat_post_busqueda and form.is_valid():
                            tipocat_form_value = form.cleaned_data.get('tipocat', '')
                            tipocat_post_busqueda = str(tipocat_form_value) if tipocat_form_value else ''
                            print(f"[DEBUG] 🔍 tipocat obtenida de form.cleaned_data: '{tipocat_post_busqueda}'")
                        
                        # Si aún no hay valor, usar tipocat_str que ya se calculó antes
                        if not tipocat_post_busqueda:
                            tipocat_post_busqueda = tipocat_str if tipocat_str else ''
                            print(f"[DEBUG] 🔍 tipocat usando tipocat_str como fallback: '{tipocat_post_busqueda}'")
                        
                        # Extraer solo el número (ej: "1" de "1. Viviendas" o "1 - Viviendas")
                        import re
                        match = re.match(r'^(\d+)', tipocat_post_busqueda) if tipocat_post_busqueda else None
                        if match:
                            tipocat_post_busqueda = match.group(1)
                            print(f"[DEBUG] 🔍 tipocat extraída (solo número): '{tipocat_post_busqueda}'")
                        elif '-' in tipocat_post_busqueda:
                            tipocat_post_busqueda = tipocat_post_busqueda.split('-')[0].strip()
                            print(f"[DEBUG] 🔍 tipocat extraída con split(-): '{tipocat_post_busqueda}'")
                        elif '.' in tipocat_post_busqueda:
                            tipocat_post_busqueda = tipocat_post_busqueda.split('.')[0].strip()
                            print(f"[DEBUG] 🔍 tipocat extraída con split(.): '{tipocat_post_busqueda}'")
                        
                        # CRÍTICO: El campo tipocat es CHAR(1) en la BD, usar string ('1', '2', '3' o '')
                        # Validar que sea solo '1', '2' o '3'
                        if tipocat_post_busqueda and re.match(r'^[123]$', tipocat_post_busqueda):
                            tipocat_str_busqueda = tipocat_post_busqueda  # Ya es '1', '2' o '3'
                        elif tipocat_post_busqueda:
                            # Si tiene formato diferente, extraer solo el número
                            match = re.match(r'^([123])', tipocat_post_busqueda)
                            if match:
                                tipocat_str_busqueda = match.group(1)  # '1', '2' o '3'
                            else:
                                tipocat_str_busqueda = ''
                        else:
                            tipocat_str_busqueda = ''  # Vacío si no hay valor
                        
                        print(f"[DEBUG] 🔍 tipocat_str_busqueda (CHAR(1)): '{tipocat_str_busqueda}' (tipo: {type(tipocat_str_busqueda)})")
                        
                        filtros_indice_unico = {
                            'empresa': empresa.strip() if empresa else '',
                            'rubro': rubro.strip() if rubro else '',
                            'cod_tarifa': cod_tarifa.strip() if cod_tarifa else None,
                            'tipocat': tipocat_str_busqueda,  # OBLIGATORIO para Doméstica (string: '1', '2' o '3')
                            'ano': ano_int,
                            'codigo': codigo.strip() if codigo else ''
                        }
                        print(f"[DEBUG] 🔍 FILTROS DOMÉSTICOS (con tipocat): empresa, rubro, cod_tarifa, tipocat='{tipocat_str_busqueda}', ano, codigo")
                    else:
                        # VALIDACIÓN NO-DOMÉSTICA: empresa, rubro, cod_tarifa, ano, codigo (sin tipocat)
                        print(f"[DEBUG] 🔍 TARIFA NO-DOMÉSTICA - SIN TIPOCAT")
                        
                        # Para tarifas no domésticas, usar tipocat='' (string vacío) por defecto
                        tipocat_str = ''  # String vacío para no-domésticas
                        
                        filtros_indice_unico = {
                            'empresa': empresa.strip() if empresa else '',
                            'rubro': rubro.strip() if rubro else '',
                            'cod_tarifa': cod_tarifa.strip() if cod_tarifa else None,
                            'tipocat': tipocat_str,  # String vacío para no-domésticas
                            'ano': ano_int,
                            'codigo': codigo.strip() if codigo else ''
                        }
                        print(f"[DEBUG] 🔍 FILTROS NO-DOMÉSTICOS (tipocat=''): empresa, rubro, cod_tarifa, ano, codigo")
                    
                    print(f"[DEBUG] 🔍 filtros_indice_unico construido:")
                    print(f"[DEBUG]     - empresa: '{filtros_indice_unico['empresa']}'")
                    print(f"[DEBUG]     - rubro: '{filtros_indice_unico['rubro']}'")
                    print(f"[DEBUG]     - cod_tarifa: '{filtros_indice_unico['cod_tarifa']}'")
                    print(f"[DEBUG]     - tipocat: {filtros_indice_unico['tipocat']} (tipo: {type(filtros_indice_unico['tipocat'])})")
                    print(f"[DEBUG]     - ano: {filtros_indice_unico['ano']}")
                    print(f"[DEBUG]     - codigo: '{filtros_indice_unico['codigo']}'")
                    
                    # BÚSQUEDA DIRECTA usando el índice único planarbitio_idx1
                    # El índice único es: (empresa, rubro, cod_tarifa, tipocat, ano, codigo)
                    # Usar filter().first() para obtener el registro si existe
                    print(f"[DEBUG] ========== BÚSQUEDA POR ÍNDICE ÚNICO planarbitio_idx1 ==========")
                    print(f"[DEBUG] 🔍 FILTROS DE BÚSQUEDA (ÍNDICE ÚNICO):")
                    print(f"[DEBUG]     - empresa: '{filtros_indice_unico['empresa']}'")
                    print(f"[DEBUG]     - rubro: '{filtros_indice_unico['rubro']}'")
                    print(f"[DEBUG]     - cod_tarifa: '{filtros_indice_unico['cod_tarifa']}'")
                    print(f"[DEBUG]     - tipocat: {filtros_indice_unico['tipocat']} (tipo: {type(filtros_indice_unico['tipocat'])}) ⚠️ OBLIGATORIO")
                    print(f"[DEBUG]     - ano: {filtros_indice_unico['ano']}")
                    print(f"[DEBUG]     - codigo: '{filtros_indice_unico['codigo']}'")
                    print(f"[DEBUG] ⚠️ Si existe un registro con estos 6 campos exactos → ACTUALIZAR")
                    print(f"[DEBUG] ⚠️ Si NO existe → CREAR NUEVO")
                    
                    # Buscar registro usando TODOS los campos del índice único
                    query_set = PlanArbitrio.objects.filter(**filtros_indice_unico)
                    print(f"[DEBUG] 🔍 QuerySet generado: {query_set.query}")
                    print(f"[DEBUG] 🔍 Cantidad de registros encontrados: {query_set.count()}")
                    
                    # Verificar todos los registros encontrados para debugging
                    todos_encontrados = list(query_set)
                    if todos_encontrados:
                        print(f"[DEBUG] 🔍 REGISTROS ENCONTRADOS POR EL QUERY:")
                        for idx, reg in enumerate(todos_encontrados):
                            print(f"[DEBUG]     Registro #{idx+1}: ID={reg.id}")
                            print(f"         - empresa: '{reg.empresa}' (buscado: '{filtros_indice_unico['empresa']}')")
                            print(f"         - rubro: '{reg.rubro}' (buscado: '{filtros_indice_unico['rubro']}')")
                            print(f"         - cod_tarifa: '{reg.cod_tarifa}' (buscado: '{filtros_indice_unico['cod_tarifa']}')")
                            print(f"         - tipocat: {reg.tipocat} tipo={type(reg.tipocat)} (buscado: {filtros_indice_unico['tipocat']} tipo={type(filtros_indice_unico['tipocat'])})")
                            print(f"         - ano: {reg.ano} (buscado: {filtros_indice_unico['ano']})")
                            print(f"         - codigo: '{reg.codigo}' (buscado: '{filtros_indice_unico['codigo']}')")
                    
                    existing_plan = query_set.first()
                    
                    if existing_plan:
                        print(f"[DEBUG] ✅✅✅ REGISTRO ENCONTRADO usando índice único planarbitio_idx1")
                        print(f"[DEBUG] ✅ ID={existing_plan.id}")
                        print(f"[DEBUG] ✅ CAMPOS DEL REGISTRO ENCONTRADO:")
                        print(f"     - empresa: '{existing_plan.empresa}'")
                        print(f"     - rubro: '{existing_plan.rubro}'")
                        print(f"     - cod_tarifa: '{existing_plan.cod_tarifa}'")
                        print(f"     - tipocat: '{existing_plan.tipocat}' (CHAR(1))")
                        print(f"     - ano: {int(existing_plan.ano) if existing_plan.ano else None}")
                        print(f"     - codigo: '{existing_plan.codigo}'")
                        print(f"[DEBUG] ✅✅✅ DECISIÓN: Se ACTUALIZARÁ el registro existente")
                    else:
                        print(f"[DEBUG] ⚠️⚠️⚠️ NO SE ENCONTRÓ ningún registro con esta combinación de índice único")
                        print(f"[DEBUG] ⚠️⚠️⚠️ CAMPOS BUSCADOS:")
                        print(f"     - empresa: '{filtros_indice_unico['empresa']}'")
                        print(f"     - rubro: '{filtros_indice_unico['rubro']}'")
                        print(f"     - cod_tarifa: '{filtros_indice_unico['cod_tarifa']}'")
                        print(f"     - tipocat: {filtros_indice_unico['tipocat']}")
                        print(f"     - ano: {filtros_indice_unico['ano']}")
                        print(f"     - codigo: '{filtros_indice_unico['codigo']}'")
                        print(f"[DEBUG] ⚠️⚠️⚠️ DECISIÓN: Se CREARÁ un nuevo registro")
                    
                    # DECISIÓN: ACTUALIZAR O CREAR
                    if existing_plan:
                        print(f"[DEBUG] ========== REGISTRO EXISTENTE VÁLIDO ENCONTRADO ==========")
                        print(f"[DEBUG] ✅ ID={existing_plan.id}")
                        print(f"[DEBUG] ✅ COINCIDENCIA EXACTA EN TODOS LOS CAMPOS ÚNICOS:")
                        print(f"[DEBUG]     - empresa: '{existing_plan.empresa}' == '{empresa}' ✅")
                        print(f"[DEBUG]     - rubro: '{existing_plan.rubro}' == '{rubro}' ✅")
                        print(f"[DEBUG]     - cod_tarifa: '{existing_plan.cod_tarifa}' == '{cod_tarifa}' ✅")
                        print(f"[DEBUG]     - tipocat: '{existing_plan.tipocat}' == '{tipocat_str}' ✅")
                        print(f"[DEBUG]     - ano: {int(existing_plan.ano)} == {ano_int} ✅")
                        print(f"[DEBUG]     - codigo: '{existing_plan.codigo}' == '{codigo}' ✅")
                        print(f"[DEBUG] 🔄 MODO: ACTUALIZACIÓN")
                        print(f"[DEBUG] ⚠️ Solo se actualizará este registro porque coincide EXACTAMENTE con todos los campos únicos")
                        
                        # ACTUALIZAR registro existente usando los campos únicos
                        print(f"[DEBUG] 🔄 ACTUALIZANDO REGISTRO EXISTENTE")
                        
                        # Obtener los nuevos valores del formulario (solo si el formulario es válido)
                        if form.is_valid():
                            nueva_descripcion = form.cleaned_data.get('descripcion', '')
                            nuevo_minimo = form.cleaned_data.get('minimo', 0.00)
                            nuevo_maximo = form.cleaned_data.get('maximo', 0.00)
                        else:
                            # Si el formulario no es válido, obtener los valores directamente del POST
                            nueva_descripcion = request.POST.get('descripcion', '').strip()
                            nuevo_minimo = Decimal(request.POST.get('minimo', '0.00').replace(',', '.')) if request.POST.get('minimo') else Decimal('0.00')
                            nuevo_maximo = Decimal(request.POST.get('maximo', '0.00').replace(',', '.')) if request.POST.get('maximo') else Decimal('0.00')
                        
                        # Calcular el valor automáticamente
                        if nuevo_minimo is not None and nuevo_maximo is not None:
                            nuevo_valor = (nuevo_minimo + nuevo_maximo) / 2
                        elif nuevo_minimo is not None:
                            nuevo_valor = nuevo_minimo
                        elif nuevo_maximo is not None:
                            nuevo_valor = nuevo_maximo
                        else:
                            nuevo_valor = 0.00
                        
                        print(f"[DEBUG] Nuevos valores a guardar:")
                        print(f"  - descripcion: '{nueva_descripcion}'")
                        print(f"  - minimo: {nuevo_minimo}")
                        print(f"  - maximo: {nuevo_maximo}")
                        print(f"  - valor: {nuevo_valor}")
                        print(f"  - tipocat: {tipocat_int} (no cambiará)")
                        
                        # IMPORTANTE: Usar EXACTAMENTE los mismos filtros del índice único para actualizar
                        # Usar filtros_indice_unico que ya tiene TODOS los campos correctos del índice planarbitio_idx1
                        print(f"[DEBUG] 🔄 FILTROS DE ACTUALIZACIÓN (usando filtros_indice_unico - ÍNDICE planarbitio_idx1):")
                        print(f"[DEBUG]     - empresa: '{filtros_indice_unico['empresa']}'")
                        print(f"[DEBUG]     - rubro: '{filtros_indice_unico['rubro']}'")
                        print(f"[DEBUG]     - cod_tarifa: '{filtros_indice_unico['cod_tarifa']}'")
                        print(f"[DEBUG]     - tipocat: {filtros_indice_unico['tipocat']} ⚠️ OBLIGATORIO - parte del índice único")
                        print(f"[DEBUG]     - ano: {filtros_indice_unico['ano']}")
                        print(f"[DEBUG]     - codigo: '{filtros_indice_unico['codigo']}'")
                        print(f"[DEBUG] ⚠️ Esto actualizará SOLO el registro con esta combinación exacta del índice único planarbitio_idx1")
                        
                        # Actualizar usando los mismos filtros del índice único (NO actualizar tipocat porque es parte del índice)
                        rows_updated = PlanArbitrio.objects.filter(**filtros_indice_unico).update(
                            descripcion=nueva_descripcion,
                            minimo=nuevo_minimo,
                            maximo=nuevo_maximo,
                            valor=nuevo_valor
                            # NO actualizar tipocat porque es parte del índice único planarbitio_idx1 y no debe cambiar
                        )
                        
                        if rows_updated > 0:
                            print(f"[DEBUG] ✅ Plan actualizado exitosamente: {rows_updated} registro(s)")
                            mensaje = f"✅ Plan de arbitrio {codigo} actualizado exitosamente."
                            exito = True
                        else:
                            print(f"[DEBUG] ❌ No se pudo actualizar el registro")
                            mensaje = f"❌ Error: No se pudo actualizar el plan de arbitrio {codigo}."
                            exito = False
                        
                        form = PlanArbitrioForm(initial={'empresa': empresa})
                    
                    else:
                        # No se encontró registro válido - CREAR uno nuevo
                        print(f"[DEBUG] ========== NO SE ENCONTRÓ REGISTRO VÁLIDO ==========")
                        if tipomodulo == 'D':
                            print(f"[DEBUG] ❌ No se encontró registro con los parámetros (incluyendo tipocat={filtros_indice_unico['tipocat']})")
                        else:
                            print(f"[DEBUG] ❌ No se encontró registro con los parámetros (tipocat=0 para tarifa no-doméstica)")
                        print(f"[DEBUG] 🆕 MODO: CREACIÓN DE NUEVO REGISTRO")
                        print(f"[DEBUG] 🆕 existing_plan es None, ejecutando bloque else para CREAR")
                        
                        # Obtener valores del formulario (solo si es válido, sino del POST)
                        if form.is_valid():
                            descripcion_nueva = form.cleaned_data.get('descripcion', '')
                            minimo_nuevo = form.cleaned_data.get('minimo', Decimal('0.00'))
                            maximo_nuevo = form.cleaned_data.get('maximo', Decimal('0.00'))
                            # OBTENER TIPOCAT DEL FORMULARIO VALIDADO (PRIORIDAD)
                            tipocat_form_guardar = form.cleaned_data.get('tipocat', '')
                            tipocat_form_guardar = str(tipocat_form_guardar).strip() if tipocat_form_guardar else ''
                        else:
                            descripcion_nueva = request.POST.get('descripcion', '').strip()
                            minimo_nuevo = Decimal(request.POST.get('minimo', '0.00').replace(',', '.')) if request.POST.get('minimo') else Decimal('0.00')
                            maximo_nuevo = Decimal(request.POST.get('maximo', '0.00').replace(',', '.')) if request.POST.get('maximo') else Decimal('0.00')
                            tipocat_form_guardar = ''
                        
                        # OBTENER TIPOCAT FINAL PARA GUARDAR - PRIORIDAD: form.cleaned_data, luego POST
                        tipocat_post_guardar = request.POST.get('tipocat', '').strip()
                        # Usar tipocat del formulario si está disponible, sino del POST
                        tipocat_para_guardar = tipocat_form_guardar if tipocat_form_guardar else tipocat_post_guardar
                        print(f"[DEBUG] 🆕 ========== OBTENIENDO TIPOCAT PARA GUARDAR ==========")
                        print(f"[DEBUG] 🆕 tipocat_form_guardar (del formulario validado): '{tipocat_form_guardar}'")
                        print(f"[DEBUG] 🆕 tipocat_post_guardar (RAW del POST): '{tipocat_post_guardar}'")
                        print(f"[DEBUG] 🆕 tipocat_para_guardar (FINAL - prioridad form): '{tipocat_para_guardar}'")
                        print(f"[DEBUG] 🆕 tipomodulo: '{tipomodulo}'")
                        print(f"[DEBUG] 🆕 Tipo de dato recibido: {type(tipocat_para_guardar)}")
                        print(f"[DEBUG] 🆕 Longitud: {len(tipocat_para_guardar) if tipocat_para_guardar else 0}")
                        print(f"[DEBUG] 🆕 Representación: repr(tipocat_para_guardar) = {repr(tipocat_para_guardar)}")
                        print(f"[DEBUG] 🆕 Todos los campos POST relacionados con tipocat:")
                        tipocat_keys_found = []
                        for key in request.POST.keys():
                            if 'tipocat' in key.lower():
                                valor = request.POST.get(key)
                                tipocat_keys_found.append(key)
                                print(f"[DEBUG]         - {key}: '{valor}' (tipo: {type(valor)}, longitud: {len(str(valor)) if valor else 0})")
                        if not tipocat_keys_found:
                            print(f"[DEBUG]         ⚠️⚠️⚠️ NO SE ENCONTRÓ NINGÚN CAMPO CON 'tipocat' EN EL NOMBRE!")
                        print(f"[DEBUG] 🆕 ======================================================")
                        
                        # VALIDACIÓN: El frontend DEBE enviar el código de tipocategoria (1 carácter)
                        # El campo en la BD es CHAR(1), así que debe ser string de 1 carácter
                        if tipocat_para_guardar:
                            print(f"[DEBUG] 🆕 tipocat encontrada: '{tipocat_para_guardar}'")
                            
                            # CRÍTICO: Validar que sea un código válido de tipocategoria (1 carácter)
                            import re
                            # Validar formato: código de 1 carácter alfanumérico
                            tipocat_para_guardar = tipocat_para_guardar.strip()
                            if len(tipocat_para_guardar) == 1 and re.match(r'^[A-Za-z0-9]$', tipocat_para_guardar):
                                # Ya es el formato correcto, usar directamente como string
                                print(f"[DEBUG] 🆕 ✅✅✅ tipocat VALIDA: '{tipocat_para_guardar}' (string CHAR(1))")
                                print(f"[DEBUG] 🆕 ✅ Tipo final: {type(tipocat_para_guardar)}")
                            else:
                                # Si viene con formato diferente (ej: "1. Viviendas"), intentar extraer solo el código
                                print(f"[DEBUG] 🆕 ⚠️ tipocat no está en formato esperado (código de 1 carácter)")
                                # Intentar extraer el código (primer carácter antes de un punto o espacio)
                                match = re.match(r'^([A-Za-z0-9])', tipocat_para_guardar)
                                if match:
                                    tipocat_para_guardar = match.group(1)  # Código de 1 carácter
                                    print(f"[DEBUG] 🆕 ✅ tipocat extraída y validada: '{tipocat_para_guardar}' (string)")
                                else:
                                    print(f"[DEBUG] 🆕 ❌ ERROR: tipocat no válida: '{tipocat_para_guardar}'")
                                    print(f"[DEBUG] 🆕 ❌ Debe ser un código de 1 carácter, pero se recibió: '{tipocat_para_guardar}' (longitud: {len(tipocat_para_guardar)})")
                                    # Intentar usar el valor de filtros_indice_unico como fallback
                                    tipocat_fallback = filtros_indice_unico.get('tipocat', '')
                                    if tipomodulo == 'D' and not tipocat_fallback:
                                        print(f"[DEBUG] 🆕 ❌ ERROR CRÍTICO: tipocat no válida y fallback está vacío para tarifa doméstica!")
                                    tipocat_para_guardar = tipocat_fallback
                                    print(f"[DEBUG] 🆕 ⚠️ usando filtros_indice_unico como fallback: '{tipocat_para_guardar}'")
                        else:
                            # Si no hay en form ni POST, buscar en otros campos o usar fallback
                            print(f"[DEBUG] 🆕 ⚠️ tipocat NO ENCONTRADA EN FORM NI POST")
                            print(f"[DEBUG] 🆕 ⚠️ Buscando en TODOS los campos POST (para debug completo)...")
                            tipocat_encontrada = False
                            for key, value in request.POST.items():
                                print(f"[DEBUG] 🆕         '{key}' = '{value}' (tipo: {type(value)})")
                                if 'tipocat' in key.lower():
                                    print(f"[DEBUG] 🆕 ⚠️⚠️⚠️ ENCONTRADO campo relacionado con tipocat: '{key}' = '{value}'")
                                    # Intentar extraer el valor
                                    import re
                                    match = re.match(r'^([123])', str(value))
                                    if match:
                                        tipocat_para_guardar = match.group(1)  # '1', '2' o '3' (string)
                                        tipocat_encontrada = True
                                        print(f"[DEBUG] 🆕 ✅✅✅ tipocat encontrada en campo '{key}': '{tipocat_para_guardar}' (string)")
                                        break
                            
                            if not tipocat_encontrada:
                                tipocat_para_guardar = filtros_indice_unico.get('tipocat', '')
                                print(f"[DEBUG] 🆕 ⚠️ usando filtros_indice_unico como fallback: '{tipocat_para_guardar}'")
                        
                        # Si es tarifa doméstica y tipocat está vacío, mostrar advertencia
                        if tipomodulo == 'D' and not tipocat_para_guardar:
                            print(f"[DEBUG] ⚠️ ADVERTENCIA: Tarifa doméstica pero tipocat está vacío. Verificar que se esté enviando desde el frontend.")
                        
                        # Verificación final: asegurar que tipocat_para_guardar sea string válido
                        if tipocat_para_guardar is None:
                            tipocat_para_guardar = ''  # String vacío por defecto
                            print(f"[DEBUG]     - tipocat_para_guardar era None, usando '' (string vacío)")
                        
                        print(f"[DEBUG] 🆕 CREANDO NUEVO REGISTRO:")
                        if tipomodulo == 'D':
                            print(f"[DEBUG] 🆕 TARIFA DOMÉSTICA - tipocat='{tipocat_para_guardar}' (tipo: {type(tipocat_para_guardar)})")
                        else:
                            print(f"[DEBUG] 🆕 TARIFA NO-DOMÉSTICA - tipocat='{tipocat_para_guardar}' (string vacío)")
                        print(f"[DEBUG] 🆕 Usando EXACTAMENTE los mismos parámetros que la búsqueda automática")
                        
                        # Calcular el valor automáticamente antes de crear
                        if minimo_nuevo is not None and maximo_nuevo is not None:
                            valor_calculado = (minimo_nuevo + maximo_nuevo) / 2
                        elif minimo_nuevo is not None:
                            valor_calculado = minimo_nuevo
                        elif maximo_nuevo is not None:
                            valor_calculado = maximo_nuevo
                        else:
                            valor_calculado = Decimal('0.00')
                        
                        # Asegurar que tipocat_para_guardar sea string válido (código de tipocategoria de 1 carácter o '')
                        if not isinstance(tipocat_para_guardar, str):
                            tipocat_para_guardar = str(tipocat_para_guardar) if tipocat_para_guardar else ''
                        
                        # Validar que sea un código válido de tipocategoria (1 carácter alfanumérico) o string vacío
                        if tipocat_para_guardar:
                            tipocat_para_guardar = tipocat_para_guardar.strip()
                            # Truncar a 1 carácter si es más largo
                            if len(tipocat_para_guardar) > 1:
                                tipocat_para_guardar = tipocat_para_guardar[0]
                            # Verificar que el código existe en la tabla tipocategoria
                            from tributario.models import TipoCategoria
                            try:
                                categoria_existe = TipoCategoria.objects.filter(codigo=tipocat_para_guardar).exists()
                                if not categoria_existe:
                                    print(f"[DEBUG] ⚠️⚠️⚠️ CÓDIGO NO EXISTE EN TIPOCATEGORIA: tipocat='{tipocat_para_guardar}'")
                                    print(f"[DEBUG] ⚠️⚠️⚠️ VALOR INVÁLIDO: tipocat='{tipocat_para_guardar}' no existe en tipocategoria, usando '' como fallback")
                                    tipocat_para_guardar = ''
                            except Exception as e:
                                print(f"[DEBUG] ⚠️ Error al validar tipocat en BD: {e}")
                                # Si hay error, permitir el valor pero truncar a 1 carácter
                                if len(tipocat_para_guardar) > 1:
                                    tipocat_para_guardar = tipocat_para_guardar[0]
                        
                        print(f"[DEBUG] 🆕 VALORES FINALES PARA CREAR OBJETO:")
                        print(f"[DEBUG]     - empresa: '{filtros_indice_unico['empresa']}'")
                        print(f"[DEBUG]     - rubro: '{filtros_indice_unico['rubro']}'")
                        print(f"[DEBUG]     - cod_tarifa: '{filtros_indice_unico['cod_tarifa']}'")
                        print(f"[DEBUG]     - tipocat: '{tipocat_para_guardar}' (tipo: {type(tipocat_para_guardar)}, CHAR(1)) ⚠️⚠️⚠️ CRÍTICO")
                        print(f"[DEBUG]     - ano: {filtros_indice_unico['ano']}")
                        print(f"[DEBUG]     - codigo: '{filtros_indice_unico['codigo']}'")
                        print(f"[DEBUG]     - descripcion: '{descripcion_nueva}'")
                        print(f"[DEBUG]     - minimo: {minimo_nuevo}")
                        print(f"[DEBUG]     - maximo: {maximo_nuevo}")
                        print(f"[DEBUG]     - valor: {valor_calculado}")
                        
                        print(f"[DEBUG] 🆕 VALOR FINAL DE TIPOCAT ANTES DE CREAR: '{tipocat_para_guardar}' (string CHAR(1) - código de tipocategoria)")
                        
                        # Crear el nuevo plan usando objects.create() directamente con TODOS los campos
                        nuevo_plan = PlanArbitrio.objects.create(
                            empresa=filtros_indice_unico['empresa'],
                            rubro=filtros_indice_unico['rubro'],
                            cod_tarifa=filtros_indice_unico['cod_tarifa'],
                            tipocat=tipocat_para_guardar,  # OBLIGATORIO: asignar tipocat explícitamente como string (código de tipocategoria de 1 carácter o '')
                            ano=filtros_indice_unico['ano'],
                            codigo=filtros_indice_unico['codigo'],
                            descripcion=descripcion_nueva,
                            minimo=minimo_nuevo,
                            maximo=maximo_nuevo,
                            valor=valor_calculado
                        )
                        
                        print(f"[DEBUG] ✅ Objeto creado con objects.create() - ID: {nuevo_plan.id}")
                        
                        # VERIFICACIÓN INMEDIATA después de crear (objects.create() ya guarda automáticamente)
                        print(f"[DEBUG] ✅ OBJETO CREADO CON objects.create() - ID: {nuevo_plan.id}")
                        print(f"[DEBUG] 🆕 VERIFICACIÓN DESPUÉS DE CREAR:")
                        print(f"[DEBUG]     - nuevo_plan.tipocat: {nuevo_plan.tipocat} (tipo: {type(nuevo_plan.tipocat)})")
                        print(f"[DEBUG]     - nuevo_plan.empresa: '{nuevo_plan.empresa}'")
                        print(f"[DEBUG]     - nuevo_plan.rubro: '{nuevo_plan.rubro}'")
                        print(f"[DEBUG]     - nuevo_plan.cod_tarifa: '{nuevo_plan.cod_tarifa}'")
                        print(f"[DEBUG]     - nuevo_plan.ano: {nuevo_plan.ano}")
                        print(f"[DEBUG]     - nuevo_plan.codigo: '{nuevo_plan.codigo}'")
                        print(f"[DEBUG] ⚠️ VERIFICACIÓN CRÍTICA: tipocat guardada = '{nuevo_plan.tipocat}', tipocat esperada = '{tipocat_para_guardar}'")
                        print(f"[DEBUG] ⚠️ Comparación (tipocat guardada == tipocat esperada): {nuevo_plan.tipocat == tipocat_para_guardar}")
                        print(f"[DEBUG] ⚠️ Tipos: guardada={type(nuevo_plan.tipocat)}, esperada={type(tipocat_para_guardar)}")
                        
                        # VERIFICACIÓN POST-CREATE: Si tipocat no coincide, actualizar
                        # Comparar como string para evitar problemas de tipo
                        tipocat_guardada_str = str(nuevo_plan.tipocat) if nuevo_plan.tipocat is not None else ''
                        tipocat_esperada_str = str(tipocat_para_guardar) if tipocat_para_guardar else ''
                        
                        if tipocat_guardada_str != tipocat_esperada_str:
                            print(f"[DEBUG] ⚠️⚠️⚠️ DISCREPANCIA DETECTADA: tipocat guardada ('{tipocat_guardada_str}') != tipocat esperada ('{tipocat_esperada_str}')")
                            print(f"[DEBUG] 🔧 Actualizando tipocat manualmente...")
                            nuevo_plan.tipocat = tipocat_para_guardar
                            nuevo_plan.save(update_fields=['tipocat'])
                            nuevo_plan.refresh_from_db()
                            print(f"[DEBUG] ✅ tipocat actualizada. Nuevo valor: '{nuevo_plan.tipocat}'")
                        else:
                            print(f"[DEBUG] ✅✅✅ tipocat guardada CORRECTAMENTE: '{tipocat_guardada_str}'")
                        
                        # Verificar que se guardó correctamente consultando la BD inmediatamente
                        try:
                            plan_guardado = PlanArbitrio.objects.get(id=nuevo_plan.id)
                            print(f"[DEBUG] ✅ VERIFICACIÓN EN BD:")
                            print(f"[DEBUG]     - tipocat en objeto: {nuevo_plan.tipocat}")
                            print(f"[DEBUG]     - tipocat en BD: {plan_guardado.tipocat}")
                            print(f"[DEBUG]     - empresa: '{plan_guardado.empresa}'")
                            print(f"[DEBUG]     - rubro: '{plan_guardado.rubro}'")
                            print(f"[DEBUG]     - cod_tarifa: '{plan_guardado.cod_tarifa}'")
                            print(f"[DEBUG]     - ano: {plan_guardado.ano}")
                            print(f"[DEBUG]     - codigo: '{plan_guardado.codigo}'")
                            
                            # CRÍTICO: tipocat es CHAR(1), comparar como strings
                            tipocat_guardada_str_bd = str(plan_guardado.tipocat) if plan_guardado.tipocat is not None and plan_guardado.tipocat else ''
                            tipocat_esperada_str_bd = str(tipocat_para_guardar) if tipocat_para_guardar else ''
                            
                            print(f"[DEBUG] 🔍 COMPARACIÓN FINAL:")
                            print(f"[DEBUG]     - tipocat guardada en BD: '{tipocat_guardada_str_bd}'")
                            print(f"[DEBUG]     - tipocat esperada: '{tipocat_esperada_str_bd}'")
                            
                            if tipocat_guardada_str_bd != tipocat_esperada_str_bd:
                                print(f"[DEBUG] ❌❌❌ ERROR CRÍTICO: tipocat guardada ('{tipocat_guardada_str_bd}') != tipocat esperada ('{tipocat_esperada_str_bd}')")
                                print(f"[DEBUG] ❌❌❌ CORRIGIENDO usando update()...")
                                
                                # Actualizar usando update() con el ID específico
                                rows_updated = PlanArbitrio.objects.filter(id=nuevo_plan.id).update(tipocat=tipocat_para_guardar)
                                print(f"[DEBUG]     - Filas actualizadas: {rows_updated}")
                                
                                # Verificar nuevamente
                                plan_guardado.refresh_from_db()
                                tipocat_guardada_str_bd_2 = str(plan_guardado.tipocat) if plan_guardado.tipocat else ''
                                
                                if tipocat_guardada_str_bd_2 == tipocat_esperada_str_bd:
                                    print(f"[DEBUG] ✅✅✅ CORRECCIÓN EXITOSA: tipocat actualizada correctamente a '{tipocat_guardada_str_bd_2}'")
                                else:
                                    print(f"[DEBUG] ❌❌❌ CORRECCIÓN FALLIDA: tipocat sigue siendo '{tipocat_guardada_str_bd_2}', intentando SQL directo...")
                                    # Intentar con SQL directo como último recurso
                                    from django.db import connection
                                    with connection.cursor() as cursor:
                                        cursor.execute(
                                            "UPDATE planarbitio SET tipocat = %s WHERE id = %s",
                                            [tipocat_para_guardar, nuevo_plan.id]
                                        )
                                    plan_guardado.refresh_from_db()
                                    tipocat_guardada_str_bd_2 = str(plan_guardado.tipocat) if plan_guardado.tipocat else ''
                                    print(f"[DEBUG]     - Después de SQL directo: '{tipocat_guardada_str_bd_2}'")
                                
                                categoria_display = tipocat_guardada_str_bd_2 if tipocat_guardada_str_bd_2 else 'Sin categoría'
                                mensaje = f"✅ Plan de arbitrio {codigo} creado exitosamente con categoría {categoria_display}."
                            else:
                                print(f"[DEBUG] ✅✅✅ VERIFICACIÓN EXITOSA: tipocat guardada ('{tipocat_guardada_str_bd}') == tipocat esperada ('{tipocat_esperada_str_bd}')")
                                categoria_display = tipocat_guardada_str_bd if tipocat_guardada_str_bd else 'Sin categoría'
                                mensaje = f"✅ Plan de arbitrio {codigo} creado exitosamente con categoría {categoria_display}."
                            
                            exito = True
                        except Exception as save_error:
                            print(f"[DEBUG] ❌ Error al guardar nuevo plan: {str(save_error)}")
                            import traceback
                            traceback.print_exc()
                            mensaje = f"❌ Error al crear el plan de arbitrio: {str(save_error)}"
                            exito = False
                        
                        form = PlanArbitrioForm(initial={'empresa': empresa})
                
                except Exception as e:
                    # Capturar cualquier otro error inesperado
                    print(f"[DEBUG] ❌ ERROR INESPERADO: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    mensaje = f"❌ Error al procesar el plan de arbitrio: {str(e)}"
                    exito = False
                    form = PlanArbitrioForm(initial={'empresa': empresa})
            else:
                mensaje = "Por favor, corrija los errores en el formulario."
                exito = False
    else:
        initial_data = {'empresa': empresa}
        
        # Pre-cargar datos desde tarifas si se proporcionan
        if codigo_tarifa and ano_tarifa:
            try:
                tarifa = Tarifas.objects.get(
                    empresa=empresa,
                    cod_tarifa=codigo_tarifa,
                    ano=ano_tarifa
                )
                initial_data['cod_tarifa'] = tarifa.cod_tarifa
                initial_data['ano'] = tarifa.ano
                initial_data['rubro'] = tarifa.rubro
                
                # Si tipomodulo es "D", incluir tipocat en el contexto para JavaScript
                if tarifa.tipomodulo == 'D':
                    initial_data['mostrar_tipocat'] = True
                
                print(f"[DEBUG] ✅ Datos pre-cargados desde tarifa:")
                print(f"  - empresa: {initial_data['empresa']}")
                print(f"  - rubro: {initial_data['rubro']}")
                print(f"  - cod_tarifa: {initial_data['cod_tarifa']}")
                print(f"  - ano: {initial_data['ano']}")
                print(f"  - tipomodulo: {tarifa.tipomodulo}")
                
                # Obtener la descripción del rubro
                if tarifa.rubro:
                    try:
                        rubro_obj = Rubro.objects.get(empresa=empresa, codigo=tarifa.rubro)
                        initial_data['descripcion_rubro'] = rubro_obj.descripcion
                        print(f"  - descripcion_rubro: {rubro_obj.descripcion}")
                    except Rubro.DoesNotExist:
                        pass
            except Tarifas.DoesNotExist:
                print(f"[DEBUG] ❌ Tarifa no encontrada: empresa={empresa}, cod_tarifa={codigo_tarifa}, ano={ano_tarifa}")
                pass
        
        # Pre-cargar datos desde rubros si solo se proporciona el rubro
        elif codigo_rubro:
            initial_data['rubro'] = codigo_rubro
            print(f"[DEBUG] ✅ Datos pre-cargados desde rubro:")
            print(f"  - empresa: {initial_data['empresa']}")
            print(f"  - rubro: {initial_data['rubro']}")
            
            try:
                rubro_obj = Rubro.objects.get(empresa=empresa, codigo=codigo_rubro)
                initial_data['descripcion_rubro'] = rubro_obj.descripcion
                print(f"  - descripcion_rubro: {rubro_obj.descripcion}")
            except Rubro.DoesNotExist:
                print(f"[DEBUG] ❌ Rubro no encontrado: empresa={empresa}, codigo={codigo_rubro}")
                pass
        
        form = PlanArbitrioForm(initial=initial_data)
    
    # Verificar si mostrar_tipocat debe estar activo (si viene desde URL con tarifa doméstica)
    if not mostrar_tipocat and codigo_tarifa and ano_tarifa:
        try:
            tarifa_check = Tarifas.objects.filter(
                empresa=empresa,
                cod_tarifa=codigo_tarifa,
                ano=ano_tarifa
            ).first()
            if tarifa_check and tarifa_check.tipomodulo == 'D':
                mostrar_tipocat = True
                print(f"[DEBUG] ✅ Tarifa doméstica detectada desde URL - mostrar_tipocat activado")
        except Exception as e:
            print(f"[DEBUG] ⚠️ Error al verificar tipomodulo: {str(e)}")
    
    # Obtener todos los planes de arbitrio del municipio
    # Ordenar por: empresa, Año, Rubro, Cod_Tarifa, Categoría (tipocat), Código
    planes = PlanArbitrio.objects.filter(empresa=empresa).order_by('empresa', 'ano', 'rubro', 'cod_tarifa', 'tipocat', 'codigo')
    
    # Si no se ha establecido mostrar_tipocat (por ejemplo, cuando viene desde URL), verificar ahora
    if not mostrar_tipocat and codigo_tarifa and ano_tarifa:
        try:
            tarifa = Tarifas.objects.filter(
                empresa=empresa,
                cod_tarifa=codigo_tarifa,
                ano=ano_tarifa
            ).first()
            if tarifa and tarifa.tipomodulo == 'D':
                mostrar_tipocat = True
        except:
            pass
    
    # Asegurar que mostrar_tipocat esté en el contexto
    context = {
        'form': form,
        'planes_arbitrio': planes,
        'mensaje': mensaje if 'mensaje' in locals() else '',
        'exito': exito if 'exito' in locals() else False,
        'empresa_filtro': empresa,
        'rubro_filtro': codigo_rubro,
        'cod_tarifa_filtro': codigo_tarifa,
        'ano_filtro': ano_tarifa,
        'empresa': empresa,  # Agregar variable empresa para el template
        'mostrar_tipocat': mostrar_tipocat  # Flag para mostrar tipocat si tipomodulo=D
    }
    return render(request, 'formulario_plan_arbitrio.html', context)

def buscar_plan_arbitrio(request):
    """Vista AJAX para buscar planes de arbitrio"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"🔍 Búsqueda de plan arbitrio - Método: {request.method}")
    
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            empresa = data.get('empresa', '').strip()
            rubro = data.get('rubro', '').strip()
            cod_tarifa = data.get('cod_tarifa', '').strip()
            ano = data.get('ano', '').strip()
            codigo = data.get('codigo', '').strip()
            tipocat = data.get('tipocat', '').strip()
            tipomodulo = data.get('tipomodulo', '').strip()
            
            logger.info(f"📋 Datos recibidos: empresa={empresa}, rubro={rubro}, cod_tarifa={cod_tarifa}, ano={ano}, codigo={codigo}, tipocat={tipocat}, tipomodulo={tipomodulo}")
            
            if not empresa or not rubro or not cod_tarifa or not ano or not codigo:
                logger.warning("⚠️ Faltan campos requeridos")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Todos los campos son requeridos para la búsqueda'
                })
            
            # Buscar el plan de arbitrio en la base de datos
            try:
                from tributario.models import PlanArbitrio
                from decimal import Decimal
                logger.info("🔍 Buscando en base de datos...")
                
                # Para tarifa Doméstica: SIEMPRE incluir tipocat en la búsqueda (OBLIGATORIO)
                # VALIDACIÓN DOMÉSTICA: empresa, rubro, cod_tarifa, tipocat, ano, codigo
                if tipomodulo == 'D':
                    # Construir filtros con tipocat (SIEMPRE requerida para Doméstica)
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
                        'codigo': codigo
                    }
                    logger.info(f"📋 VALIDACIÓN DOMÉSTICA - TIPOCAT OBLIGATORIA")
                    logger.info(f"📋 Parámetros de búsqueda: empresa={empresa}, rubro={rubro}, cod_tarifa={cod_tarifa}, tipocat='{tipocat_valor_str}', ano={ano}, codigo={codigo}")
                else:
                    # Para otras tarifas: búsqueda sin tipocat (usar string vacío)
                    # VALIDACIÓN NO-DOMÉSTICA: empresa, rubro, cod_tarifa, ano, codigo
                    filtros = {
                        'empresa': empresa,
                        'rubro': rubro,
                        'cod_tarifa': cod_tarifa,
                        'tipocat': '',  # String vacío para no-domésticas
                        'ano': Decimal(str(ano)) if ano else None,
                        'codigo': codigo
                    }
                    logger.info(f"📋 VALIDACIÓN NO-DOMÉSTICA")
                    logger.info(f"📋 Parámetros de búsqueda: empresa={empresa}, rubro={rubro}, cod_tarifa={cod_tarifa}, ano={ano}, codigo={codigo}")
                
                plan = PlanArbitrio.objects.filter(**filtros).first()
                
                if not plan:
                    logger.info("ℹ️ Plan no encontrado en base de datos con los filtros especificados")
                    logger.info(f"📋 Filtros utilizados: {filtros}")
                    if tipomodulo == 'D':
                        logger.info(f"⚠️ Para tarifa Doméstica, se requiere coincidencia EXACTA en todos los parámetros incluyendo tipocat='{tipocat_valor_str}'")
                    return JsonResponse({
                        'exito': True,
                        'existe': False,
                        'mensaje': 'Plan de arbitrio no encontrado'
                    })
                
                logger.info(f"✅ Plan encontrado: ID={plan.id}, tipocat={plan.tipocat}")
                
                concepto_data = {
                    'empresa': plan.empresa or '',
                    'rubro': plan.rubro or '',
                    'cod_tarifa': plan.cod_tarifa or '',
                    'tipocat': str(plan.tipocat) if hasattr(plan, 'tipocat') and plan.tipocat is not None and plan.tipocat else '',
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
            except Exception as e:
                logger.error(f"❌ Error al buscar plan: {str(e)}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'Error al buscar plan: {str(e)}'
                })
                
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error JSON: {str(e)}")
            return JsonResponse({
                'exito': False,
                'mensaje': 'Error en el formato de datos'
            })
        except Exception as e:
            logger.error(f"❌ Error al buscar plan arbitrio: {str(e)}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error interno: {str(e)}'
            })
    
    logger.warning("⚠️ Método no permitido")
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

@csrf_exempt
def obtener_tipomodulo_tarifa(request):
    """Vista AJAX para obtener el tipomodulo de una tarifa"""
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        from tributario.models import Tarifas
        empresa = request.POST.get('empresa', '').strip()
        cod_tarifa = request.POST.get('cod_tarifa', '').strip()
        rubro = request.POST.get('rubro', '').strip()
        ano = request.POST.get('ano', '').strip()
        
        if not empresa or not cod_tarifa:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Empresa y código de tarifa son requeridos'
            })
        
        # Buscar la tarifa
        try:
            if rubro and ano:
                tarifa = Tarifas.objects.filter(
                    empresa=empresa,
                    cod_tarifa=cod_tarifa,
                    rubro=rubro,
                    ano=ano
                ).first()
            else:
                tarifa = Tarifas.objects.filter(
                    empresa=empresa,
                    cod_tarifa=cod_tarifa
                ).order_by('-ano').first()
            
            if tarifa:
                return JsonResponse({
                    'exito': True,
                    'tipomodulo': tarifa.tipomodulo or '',
                    'tipo': tarifa.tipo or '',
                    'descripcion': tarifa.descripcion or ''
                })
            else:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Tarifa no encontrada'
                })
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error al buscar tarifa: {str(e)}'
            })
            
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error interno: {str(e)}'
        })

@csrf_exempt
def buscar_plan_arbitrio_por_codigo(request):
    """Vista AJAX para buscar plan de arbitrio según código"""
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        from tributario.models import PlanArbitrio, Tarifas
        from decimal import Decimal
        import logging
        logger = logging.getLogger(__name__)
        
        # Obtener datos del FormData
        empresa = request.POST.get('empresa', '').strip()
        rubro = request.POST.get('rubro', '').strip()
        cod_tarifa = request.POST.get('cod_tarifa', '').strip()
        ano = request.POST.get('ano', '').strip()
        codigo = request.POST.get('codigo', '').strip()
        tipocat = request.POST.get('tipocat', '').strip()
        tipomodulo = request.POST.get('tipomodulo', '').strip()
        
        logger.info(f"🔍 Búsqueda por código: empresa={empresa}, rubro={rubro}, cod_tarifa={cod_tarifa}, ano={ano}, codigo={codigo}, tipocat={tipocat}, tipomodulo={tipomodulo}")
        
        # Validar campos requeridos
        if not empresa or not rubro or not cod_tarifa or not ano or not codigo:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Todos los campos son requeridos'
            })
        
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
                'ano': Decimal(ano) if ano else None,
                'codigo': codigo
            }
        else:
            # Para otras tarifas: sin tipocat
            filtros = {
                'empresa': empresa,
                'rubro': rubro,
                'cod_tarifa': cod_tarifa,
                'ano': Decimal(ano) if ano else None,
                'codigo': codigo
            }
        
        # Buscar el plan
        plan = PlanArbitrio.objects.filter(**filtros).first()
        
        if plan:
            return JsonResponse({
                'exito': True,
                'plan': {
                    'id': plan.id,
                    'empresa': plan.empresa or '',
                    'rubro': plan.rubro or '',
                    'cod_tarifa': plan.cod_tarifa or '',
                    'tipocat': str(plan.tipocat) if plan.tipocat is not None and plan.tipocat else '',
                    'ano': str(plan.ano) if plan.ano else '',
                    'codigo': plan.codigo or '',
                    'descripcion': plan.descripcion or '',
                    'minimo': str(plan.minimo) if plan.minimo else '0.00',
                    'maximo': str(plan.maximo) if plan.maximo else '0.00',
                    'valor': str(plan.valor) if plan.valor else '0.00'
                },
                'mensaje': f'Plan encontrado: {plan.descripcion}',
                'encontrado_en_otro_ano': False
            })
        else:
            return JsonResponse({
                'exito': False,
                'mensaje': f'No se encontró un plan con código "{codigo}" para el rubro "{rubro}" en el año "{ano}". Puede crear un nuevo plan.'
            })
            
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"❌ Error en búsqueda por código: {str(e)}")
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error en el servidor: {str(e)}'
        })

def buscar_rubro_plan_arbitrio(request):
    """Vista AJAX optimizada para buscar rubros desde el plan de arbitrio"""
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        # Obtener datos del FormData
        codigo_rubro = request.POST.get('codigo_rubro', '').strip()
        empresa = request.POST.get('empresa', '').strip()
        
        # Validar campos requeridos
        if not codigo_rubro or not empresa:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Código de rubro y empresa son requeridos'
            })
        
        # Buscar el rubro usando la función helper
        rubro_data = _buscar_rubro_helper(empresa, codigo_rubro)
        
        return JsonResponse({
            'exito': True,
            'rubro': rubro_data
        })
        
    except Rubro.DoesNotExist:
        return JsonResponse({
            'exito': False,
            'mensaje': 'Rubro no encontrado'
        })
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al buscar rubro: {str(e)}'
        })

def tarifas_crud(request):
    """Vista principal para el CRUD de tarifas"""
    from .forms import TarifasForm
    from tributario.models import Tarifas
    
    # Obtener el código de municipio de la sesión
    empresa = request.session.get('empresa')
    if not empresa:
        return redirect('tributario:tributario_login')
    
    # Obtener parámetros de la URL para pre-cargar datos
    codigo_rubro = request.GET.get('codigo_rubro', '')
    
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        # Verificar si es una acción de eliminar ANTES de validar el formulario
        accion = request.POST.get('accion', '')
        if accion == 'eliminar':
                    # Obtener solo los campos necesarios para eliminar
                    empresa_eliminar = request.POST.get('empresa', '').strip() or empresa
                    rubro_eliminar = request.POST.get('rubro', '').strip()
                    ano_eliminar = request.POST.get('ano', '').strip()
                    cod_tarifa_eliminar = request.POST.get('cod_tarifa', '').strip()
                    
                    # Debug: Mostrar solo los parámetros específicos para eliminación
                    print("🔍 DEBUG - Parámetros específicos para eliminación:")
                    print(f"   - empresa: '{empresa_eliminar}'")
                    print(f"   - rubro: '{rubro_eliminar}' (campo independiente)")
                    print(f"   - ano: '{ano_eliminar}'")
                    print(f"   - cod_tarifa: '{cod_tarifa_eliminar}' (campo independiente)")
                    
                    # Verificar independencia de rubro y cod_tarifa
                    if rubro_eliminar == cod_tarifa_eliminar:
                        print(f"   ⚠️ NOTA: Rubro y Cod_Tarifa tienen el mismo valor '{rubro_eliminar}' (coincidencia válida)")
                    else:
                        print(f"   ✅ Rubro '{rubro_eliminar}' y Cod_Tarifa '{cod_tarifa_eliminar}' son independientes")
                    
                    # Validar que todos los campos necesarios estén presentes
                    if not all([empresa_eliminar, rubro_eliminar, ano_eliminar, cod_tarifa_eliminar]):
                        campos_faltantes = []
                        if not empresa_eliminar:
                            campos_faltantes.append('empresa')
                        if not rubro_eliminar:
                            campos_faltantes.append('rubro')
                        if not ano_eliminar:
                            campos_faltantes.append('ano')
                        if not cod_tarifa_eliminar:
                            campos_faltantes.append('cod_tarifa')
                        
                        mensaje = f"❌ Faltan campos obligatorios para eliminar: {', '.join(campos_faltantes)}"
                        exito = False
                    else:
                        try:
                            # Buscar la tarifa usando exactamente los campos necesarios
                            print(f"🔍 DEBUG - Buscando tarifa con filtros:")
                            print(f"   - empresa: '{empresa_eliminar}'")
                            print(f"   - rubro: '{rubro_eliminar}'")
                            print(f"   - ano: '{ano_eliminar}'")
                            print(f"   - cod_tarifa: '{cod_tarifa_eliminar}'")
                            
                            # Contar registros antes de buscar
                            total_registros = Tarifas.objects.filter(
                                empresa=empresa_eliminar,
                                rubro=rubro_eliminar,
                                ano=ano_eliminar,
                                cod_tarifa=cod_tarifa_eliminar
                            ).count()
                            
                            print(f"🔍 DEBUG - Total registros encontrados: {total_registros}")
                            
                            tarifa_a_eliminar = Tarifas.objects.filter(
                                empresa=empresa_eliminar,
                                rubro=rubro_eliminar,
                                ano=ano_eliminar,
                                cod_tarifa=cod_tarifa_eliminar
                            ).first()
                            
                            if tarifa_a_eliminar:
                                descripcion_eliminar = tarifa_a_eliminar.descripcion or cod_tarifa_eliminar
                                print(f"🔍 DEBUG - Tarifa encontrada: {tarifa_a_eliminar}")
                                tarifa_a_eliminar.delete()
                                print(f"🔍 DEBUG - Tarifa eliminada exitosamente")
                                mensaje = f"✅ Tarifa {cod_tarifa_eliminar} ({descripcion_eliminar}) eliminada exitosamente."
                                exito = True
                            else:
                                print(f"🔍 DEBUG - No se encontró la tarifa con esos filtros")
                                mensaje = f"❌ No se encontró la tarifa {cod_tarifa_eliminar} (Empresa: {empresa_eliminar}, Rubro: {rubro_eliminar}, Año: {ano_eliminar}) para eliminar."
                                exito = False
                                
                        except Exception as e:
                            mensaje = f"❌ Error al eliminar la tarifa: {str(e)}"
                            exito = False
        else:
            # Procesar formulario normal (crear/actualizar)
            form = TarifasForm(request.POST)
            if form.is_valid():
                try:
                    # Obtener datos del formulario
                    cod_tarifa = form.cleaned_data.get('cod_tarifa')
                    ano = form.cleaned_data.get('ano')
                    rubro = form.cleaned_data.get('rubro')
                    
                    if cod_tarifa and ano and rubro:
                        # Verificar si se proporcionó un ID de tarifa (actualización)
                        tarifa_id = request.POST.get('tarifa_id', '').strip()
                        try:
                            # Usar get_or_create para manejar automáticamente la creación o actualización
                            tarifa, created = Tarifas.objects.get_or_create(
                                empresa=empresa,
                                ano=ano,
                                rubro=rubro,
                                cod_tarifa=cod_tarifa,
                                defaults={
                                    'descripcion': form.cleaned_data.get('descripcion', ''),
                                    'valor': form.cleaned_data.get('valor', 0.00),
                                    'frecuencia': form.cleaned_data.get('frecuencia', ''),
                                    'tipo': form.cleaned_data.get('tipo', ''),
                                }
                            )
                            
                            if created:
                                # Se creó un nuevo registro
                                mensaje = f"Tarifa {cod_tarifa} (Año {ano}) creada exitosamente."
                                exito = True
                            else:
                                # Ya existía, actualizar campos
                                tarifa.descripcion = form.cleaned_data.get('descripcion', '')
                                tarifa.valor = form.cleaned_data.get('valor', 0.00)
                                tarifa.frecuencia = form.cleaned_data.get('frecuencia', '')
                                tarifa.tipo = form.cleaned_data.get('tipo', '')
                                tarifa.save()
                                mensaje = f"Tarifa {cod_tarifa} (Año {ano}) actualizada exitosamente."
                                exito = True
                        except Exception as e:
                            mensaje = f"Error al procesar la tarifa: {str(e)}"
                            exito = False
                    else:
                        mensaje = "Los campos Empresa, Rubro, Año y Código de Tarifa son obligatorios."
                        exito = False
                
                    # Limpiar formulario después de cualquier operación, pero mantener el rubro si existe
                    initial_data = {'empresa': empresa}
                    if codigo_rubro:
                        initial_data['rubro'] = codigo_rubro
                    form = TarifasForm(initial=initial_data)
                except Exception as e:
                    mensaje = f"Error al guardar la tarifa: {str(e)}"
                    exito = False
            else:
                mensaje = "Por favor, corrija los errores en el formulario."
                exito = False
    
    # Inicializar formulario (necesario tanto para POST como GET)
    initial_data = {'empresa': empresa}
    if codigo_rubro:
        initial_data['rubro'] = codigo_rubro
    
    # Si hay año seleccionado, mantenerlo en el formulario
    ano_seleccionado = request.GET.get('ano', '') or request.POST.get('ano', '')
    if ano_seleccionado:
        initial_data['ano'] = ano_seleccionado
        
    form = TarifasForm(initial=initial_data)
    
    # Poblar las opciones de año con TODOS los años disponibles en la tabla anos
    from tributario.models import Anos
    anos_disponibles = Anos.objects.all().values_list('ano', flat=True).distinct().order_by('-ano')
    
    # Crear choices para el campo año (siempre todos los años disponibles)
    choices_anos = [('', 'Todos los años')] + [(str(ano), str(ano)) for ano in anos_disponibles]
    form.fields['ano'].widget.choices = choices_anos
    
    # Obtener tarifas del municipio, siempre filtrando por rubro si está disponible
    tarifas_query = Tarifas.objects.filter(empresa=empresa)
    
    # Si hay rubro heredado, siempre filtrar por él
    if codigo_rubro:
        tarifas_query = tarifas_query.filter(rubro=codigo_rubro)
    
    # Si hay año seleccionado en el formulario, filtrar por año
    ano_seleccionado = request.GET.get('ano', '') or request.POST.get('ano', '')
    if ano_seleccionado:
        tarifas_query = tarifas_query.filter(ano=ano_seleccionado)
    
    tarifas = tarifas_query.order_by('-ano', 'cod_tarifa')
    
    return render(request, 'formulario_tarifas.html', {
        'form': form,
        'tarifas': tarifas,
        'mensaje': mensaje,
        'exito': exito,
        'empresa_filtro': empresa,
        'empresa': empresa,  # Agregar variable empresa para el template
        'codigo_rubro': codigo_rubro  # Preservar el código de rubro heredado
    })

def buscar_tarifa_automatica(request):
    """Vista AJAX para búsqueda automática de tarifas con lógica de fallback"""
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        # Obtener datos del FormData
        empresa = request.POST.get('empresa', '').strip()
        rubro = request.POST.get('rubro', '').strip()
        ano = request.POST.get('ano', '').strip()
        cod_tarifa = request.POST.get('cod_tarifa', '').strip()
        
        # Validar campos requeridos
        if not empresa or not cod_tarifa:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Empresa y código de tarifa son requeridos'
            })
        
        from tributario.models import Tarifas
        
        # Búsqueda principal: buscar por empresa, año y código de tarifa
        tarifa_principal = None
        
        # Intento 1: Búsqueda por empresa, código de tarifa y año
        if empresa and cod_tarifa and ano:
            try:
                # Buscar sin considerar rubro primero (más flexible)
                tarifa_principal = Tarifas.objects.filter(
                    empresa=empresa,
                    cod_tarifa=cod_tarifa,
                    ano=ano
                ).first()
                
                # Si no encuentra y hay rubro, intentar con rubro específico
                if not tarifa_principal and rubro:
                    tarifa_principal = Tarifas.objects.filter(
                        empresa=empresa,
                        cod_tarifa=cod_tarifa,
                        ano=ano,
                        rubro=rubro
                    ).first()
                    
            except Exception as e:
                pass
        elif empresa and cod_tarifa:
            # Si no hay año, buscar solo por empresa y código de tarifa
            try:
                tarifa_principal = Tarifas.objects.filter(
                    empresa=empresa,
                    cod_tarifa=cod_tarifa
                ).order_by('-ano').first()
            except Exception as e:
                pass
        
        # Si se encontró la tarifa principal
        if tarifa_principal:
            return JsonResponse({
                'exito': True,
                'encontrado_en_otro_ano': False,
                'mensaje': f'Tarifa encontrada para el año {tarifa_principal.ano}',
                'tarifa': {
                    'id': tarifa_principal.id,
                    'cod_tarifa': tarifa_principal.cod_tarifa,
                    'descripcion': tarifa_principal.descripcion or '',
                    'valor': str(tarifa_principal.valor) if tarifa_principal.valor else '',
                    'frecuencia': tarifa_principal.frecuencia or '',
                    'tipo': tarifa_principal.tipo or '',
                    'ano': str(tarifa_principal.ano),
                    'rubro': tarifa_principal.rubro or ''
                }
            })
        
        # Si no se encontró la tarifa principal, buscar el mismo código en otros años
        try:
            query_filter = {
                'empresa': empresa,
                'cod_tarifa': cod_tarifa
            }
            # Excluir el año actual si se proporcionó
            if ano:
                tarifa_alternativa = Tarifas.objects.filter(**query_filter).exclude(ano=ano).order_by('-ano').first()
            else:
                tarifa_alternativa = Tarifas.objects.filter(**query_filter).order_by('-ano').first()
            
            if tarifa_alternativa:
                return JsonResponse({
                    'exito': True,
                    'encontrado_en_otro_ano': True,
                    'mensaje': f'Código de tarifa encontrado en el año {tarifa_alternativa.ano}. Se han cargado los datos del concepto.',
                                    'tarifa': {
                    'id': tarifa_alternativa.id,
                    'cod_tarifa': tarifa_alternativa.cod_tarifa,
                    'descripcion': tarifa_alternativa.descripcion or '',
                    'valor': str(tarifa_alternativa.valor) if tarifa_alternativa.valor else '',
                    'frecuencia': tarifa_alternativa.frecuencia or '',
                    'tipo': tarifa_alternativa.tipo or '',
                    'ano_original': str(tarifa_alternativa.ano),
                    'rubro': tarifa_alternativa.rubro or ''
                }
                })
        except Exception as e:
            pass
        
        # Si no se encontró en ningún caso
        return JsonResponse({
            'exito': False,
            'mensaje': 'No se encontró una tarifa con ese código'
        })
        
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al buscar tarifa: {str(e)}'
        })

def buscar_tarifa(request):
    """Vista AJAX para buscar tarifas"""
    if request.method == 'POST':
        try:
            # Obtener datos del FormData (método preferido)
            empresa = request.POST.get('empresa', '').strip()
            cod_tarifa = request.POST.get('cod_tarifa', '').strip()
            
            print(f"🔍 Buscando tarifa: empresa={empresa}, cod_tarifa={cod_tarifa}")
            
            if not empresa or not cod_tarifa:
                print("❌ Empresa o código de tarifa vacíos")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Empresa y código de tarifa son requeridos'
                })
            
            # Buscar la tarifa en la base de datos
            try:
                from tributario.models import Tarifas
                # Usar filter().first() para manejar múltiples resultados
                # Ordenar por año descendente para obtener la más reciente
                tarifa = Tarifas.objects.filter(
                    empresa=empresa, 
                    cod_tarifa=cod_tarifa
                ).order_by('-ano').first()
                
                if tarifa:
                    tarifa_data = {
                        'rubro': tarifa.rubro or '',
                        'cod_tarifa': tarifa.cod_tarifa or '',
                        'ano': str(tarifa.ano) if tarifa.ano else '',
                        'descripcion': tarifa.descripcion or '',
                        'valor': str(tarifa.valor),
                        'frecuencia': tarifa.frecuencia or '',
                        'tipo': tarifa.tipo or ''
                    }
                    
                    print(f"✅ Tarifa encontrada: {tarifa_data}")
                    
                    return JsonResponse({
                        'exito': True,
                        'tarifa': tarifa_data,
                        'mensaje': 'Tarifa encontrada'
                    })
                else:
                    return JsonResponse({
                        'exito': False,
                        'mensaje': 'Tarifa no encontrada'
                    })
            except Exception as e:
                print(f"❌ Error al buscar tarifa: {e}")
            return JsonResponse({
                'exito': False,
                    'mensaje': f'Error al buscar tarifa: {str(e)}'
            })
                
        except Exception as e:
            print(f"❌ Error en búsqueda AJAX de tarifa: {e}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error al buscar tarifa: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

def buscar_tarifa_plan_arbitrio(request):
    """Vista AJAX para buscar tarifas desde el plan de arbitrio"""
    if request.method == 'POST':
        try:
            codigo_tarifa = request.POST.get('codigo_tarifa', '').strip()
            empresa = request.POST.get('empresa', '').strip()
            
            if not codigo_tarifa or not empresa:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Código de tarifa y empresa son requeridos'
                })
            
            # Buscar la tarifa en la base de datos
            try:
                from tributario.models import Tarifas, Rubro
                tarifa = Tarifas.objects.get(
                    empresa=empresa, 
                    cod_tarifa=codigo_tarifa
                )
                
                # Obtener la descripción del rubro si existe
                descripcion_rubro = ''
                if tarifa.rubro:
                    try:
                        rubro_obj = Rubro.objects.get(empresa=empresa, codigo=tarifa.rubro)
                        descripcion_rubro = rubro_obj.descripcion or ''
                    except Rubro.DoesNotExist:
                        pass
                
                return JsonResponse({
                    'exito': True,
                    'tarifa': {
                        'cod_tarifa': tarifa.cod_tarifa,
                        'rubro': tarifa.rubro or '',
                        'descripcion_rubro': descripcion_rubro,
                        'ano': str(tarifa.ano) if tarifa.ano else '',
                        'descripcion': tarifa.descripcion or '',
                        'valor': str(tarifa.valor) if tarifa.valor else '',
                        'frecuencia': tarifa.frecuencia or '',
                        'tipo': tarifa.tipo or ''
                    }
                })
            except Tarifas.DoesNotExist:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Tarifa no encontrada'
                })
                
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error al buscar tarifa: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

def declaracion_volumen(request):
    """Vista para el formulario de declaración de volumen de ventas"""
    from tributario.models import DeclaracionVolumen, Negocio, AnoEmpreNu
    from tributario.models import TarifasICS, Anos
    from .forms import DeclaracionVolumenForm
    from decimal import Decimal
    from django.utils import timezone
    from django.db import transaction
    
    mensaje = None
    exito = False
    negocio = None
    declaraciones = None
    tarifas_ics = None
    
    # Obtener años disponibles de la tabla anos
    anos_disponibles = Anos.objects.all().order_by('-ano')
    
    # Obtener parámetros de la URL
    rtm = request.GET.get('rtm', '')
    expe = request.GET.get('expe', '')
    
    # Debug: verificar que las variables se estén obteniendo correctamente
    print(f"DEBUG: RTM from URL: {rtm}")
    print(f"DEBUG: EXPE from URL: {expe}")
    
    # Obtener el código de municipio de la sesión
    empresa = request.session.get('empresa')
    
    # Si se proporcionan RTM y expediente, buscar el negocio
    if rtm and expe:
        try:
            negocio = Negocio.objects.get(empresa=empresa, rtm=rtm, expe=expe)
            # Obtener declaraciones existentes para este negocio
            declaraciones = DeclaracionVolumen.objects.filter(
                empresa=empresa,
                rtm=rtm, 
                expe=expe
            ).order_by('-ano', '-mes')
            
            # Obtener tasas de declaración vinculadas al negocio desde tasasdecla
            from tributario.models import TasasDecla, Rubro
            tasas_decla_raw = TasasDecla.objects.filter(
                empresa=empresa,
                idneg=negocio.id,
                rtm=rtm,
                expe=expe
            ).order_by('rubro', 'cod_tarifa')
            
            # Enriquecer con información del rubro
            tarifas_ics = []
            for tasa in tasas_decla_raw:
                try:
                    rubro_info = Rubro.objects.get(empresa=empresa, codigo=tasa.rubro)
                    rubro_nombre = rubro_info.descripcion
                except Rubro.DoesNotExist:
                    rubro_nombre = "Rubro no encontrado"
                
                # Convertir frecuencia a descripción
                frecuencia_desc = "Mensual" if tasa.frecuencia == 'M' else "Anual" if tasa.frecuencia == 'A' else ""
                
                tarifas_ics.append({
                    'id': tasa.id,
                    'rubro': tasa.rubro,
                    'rubro_nombre': rubro_nombre,
                    'cod_tarifa': tasa.cod_tarifa,
                    'frecuencia': tasa.frecuencia,
                    'frecuencia_desc': frecuencia_desc,
                    'valor': tasa.valor,
                    'nodecla': tasa.nodecla,
                    'ano': tasa.ano
                })
            
        except Negocio.DoesNotExist:
            mensaje = "No se encontró el negocio con el RTM y expediente proporcionados"
    
    if request.method == 'POST':
        accion = request.POST.get('accion', '')
        
        if accion == 'guardar':
            form = DeclaracionVolumenForm(request.POST)
            
            # Agregar logging para debugging
            print(f"📝 Intentando guardar declaración:")
            print(f"   Empresa: {empresa}")
            print(f"   RTM: {rtm}")
            print(f"   EXPE: {expe}")
            print(f"   Usuario: {request.session.get('usuario', 'NO DEFINIDO')}")
            
            if form.is_valid():
                try:
                    from decimal import Decimal
                    
                    # Obtener datos del formulario con conversión segura
                    ano = form.cleaned_data.get('ano')
                    mes = form.cleaned_data.get('mes')
                    tipo = form.cleaned_data.get('tipo')
                    
                    # Convertir a Decimal y manejar valores None
                    ventai = Decimal(str(form.cleaned_data.get('ventai') or 0))
                    ventac = Decimal(str(form.cleaned_data.get('ventac') or 0))
                    ventas = Decimal(str(form.cleaned_data.get('ventas') or 0))
                    valorexcento = Decimal(str(form.cleaned_data.get('valorexcento') or 0))
                    controlado = Decimal(str(form.cleaned_data.get('controlado') or 0))
                    unidad = int(form.cleaned_data.get('unidad') or 0)
                    factor = Decimal(str(form.cleaned_data.get('factor') or 0))
                    multadecla = Decimal(str(form.cleaned_data.get('multadecla') or 0))
                    impuesto = Decimal(str(form.cleaned_data.get('impuesto') or 0))
                    ajuste = Decimal(str(form.cleaned_data.get('ajuste') or 0))
                    
                    # Obtener usuario de la sesión
                    usuario = request.session.get('usuario', '')
                    
                    # Verificar si ya existe un registro con empresa, RTM, EXPE y año
                    declaracion_existente = None
                    if negocio:
                        try:
                            declaracion_existente = DeclaracionVolumen.objects.get(
                                empresa=empresa,
                                rtm=rtm,
                                expe=expe,
                                ano=ano
                            )
                        except DeclaracionVolumen.DoesNotExist:
                            declaracion_existente = None
                    
                    if declaracion_existente:
                        # ACTUALIZAR registro existente
                        declaracion_existente.mes = mes
                        declaracion_existente.tipo = tipo
                        declaracion_existente.ventai = ventai
                        declaracion_existente.ventac = ventac
                        declaracion_existente.ventas = ventas
                        declaracion_existente.valorexcento = valorexcento
                        declaracion_existente.controlado = controlado
                        declaracion_existente.unidad = unidad
                        declaracion_existente.factor = factor
                        declaracion_existente.multadecla = multadecla
                        declaracion_existente.impuesto = impuesto
                        declaracion_existente.ajuste = ajuste
                        declaracion_existente.fechssys = timezone.now()
                        declaracion_existente.usuario = usuario
                        declaracion_existente.save()
                        
                        mensaje = "Declaración actualizada exitosamente"
                    else:
                        # CREAR NUEVA - Generar nodecla
                        print("="*80)
                        print(f"🔍 GENERANDO NÚMERO DE PERMISO - INICIO")
                        print(f"   Empresa: {empresa}")
                        print(f"   Año: {ano}")
                        
                        # Convertir año a Decimal para compatibilidad con BD
                        ano_decimal = Decimal(str(ano))
                        
                        # Buscar o crear registro en anoemprenu según empresa y año
                        print(f"   Buscando en anoemprenu: empresa='{empresa}', ano={ano_decimal}")
                        
                        ano_emp = None
                        try:
                            # BUSCAR registro existente
                            ano_emp = AnoEmpreNu.objects.get(empresa=empresa, ano=ano_decimal)
                            print(f"   ✅ Registro ENCONTRADO - nopermiso actual: {ano_emp.nopermiso}")
                            
                            # INCREMENTAR nopermiso
                            nopermiso_actual = ano_emp.nopermiso or Decimal('0')
                            ano_emp.nopermiso = nopermiso_actual + Decimal('1')
                            ano_emp.save()
                            print(f"   ✅ nopermiso INCREMENTADO a: {ano_emp.nopermiso}")
                            
                        except AnoEmpreNu.DoesNotExist:
                            # CREAR nuevo registro con nopermiso=1
                            print(f"   ℹ️ Registro NO existe - Creando NUEVO con nopermiso=1")
                            ano_emp = AnoEmpreNu.objects.create(
                                empresa=str(empresa),
                                ano=ano_decimal,
                                nopermiso=Decimal('1'),
                                noplanes=Decimal('0')
                            )
                            print(f"   ✅ Registro CREADO - ID: {ano_emp.id}, nopermiso: {ano_emp.nopermiso}")
                        
                        except Exception as create_error:
                            print(f"   ❌ ERROR al buscar/crear: {create_error}")
                            import traceback
                            traceback.print_exc()
                        
                        # Generar nodecla
                        if ano_emp and ano_emp.nopermiso:
                            nodecla = f"{int(ano_emp.nopermiso):010d}-{int(ano)}"
                            print(f"   ✅ NODECLA GENERADO: {nodecla}")
                        else:
                            # Fallback solo si ano_emp es None
                            import time
                            nodecla = f"{int(time.time()):010d}-{int(ano)}"
                            print(f"   ⚠️ ERROR: ano_emp es None - Usando fallback: {nodecla}")
                        
                        print(f"="*80)
                        
                        # INSERTAR nuevo registro
                        declaracion = DeclaracionVolumen(
                            nodecla=nodecla,
                            empresa=empresa,
                            idneg=negocio.id if negocio else 0,
                            rtm=rtm,
                            expe=expe,
                            ano=ano,
                            mes=mes,
                            tipo=tipo,
                            ventai=ventai,
                            ventac=ventac,
                            ventas=ventas,
                            valorexcento=valorexcento,
                            controlado=controlado,
                            unidad=unidad,
                            factor=factor,
                            multadecla=multadecla,
                            impuesto=impuesto,
                            ajuste=ajuste,
                            fechssys=timezone.now(),
                            usuario=usuario
                        )
                        declaracion.save()
                        
                        # Vincular tasas desde tarifasics a tasasdecla
                        print(f"📋 Vinculando tasas a la declaración {nodecla}...")
                        try:
                            from tributario.models import TasasDecla, Tarifas
                            
                            # Obtener todas las tarifas del negocio desde tarifasics
                            tarifas_negocio = TarifasICS.objects.filter(
                                idneg=negocio.id if negocio else 0,
                                rtm=rtm,
                                expe=expe
                            )
                            
                            tasas_creadas = 0
                            for tarifa_ics in tarifas_negocio:
                                # Buscar información de frecuencia en tabla tarifas
                                frecuencia_valor = ''
                                try:
                                    tarifa_info = Tarifas.objects.get(
                                        empresa=empresa,
                                        rubro=tarifa_ics.rubro,
                                        cod_tarifa=tarifa_ics.cod_tarifa,
                                        ano=ano
                                    )
                                    frecuencia_valor = tarifa_info.frecuencia or ''
                                except Tarifas.DoesNotExist:
                                    frecuencia_valor = ''
                                
                                # Verificar si ya existe para evitar duplicados
                                tasa_existe = TasasDecla.objects.filter(
                                    empresa=empresa,
                                    rtm=rtm,
                                    expe=expe,
                                    nodecla=nodecla,
                                    ano=ano,
                                    rubro=tarifa_ics.rubro
                                ).exists()
                                
                                if not tasa_existe:
                                    # Crear registro en tasasdecla
                                    TasasDecla.objects.create(
                                        empresa=empresa,
                                        idneg=negocio.id if negocio else 0,
                                        rtm=rtm,
                                        expe=expe,
                                        nodecla=nodecla,
                                        ano=ano,
                                        rubro=tarifa_ics.rubro,
                                        cod_tarifa=tarifa_ics.cod_tarifa,
                                        frecuencia=frecuencia_valor,
                                        valor=tarifa_ics.valor,
                                        cuenta=tarifa_ics.cuenta or '',
                                        cuentarez=tarifa_ics.cuentarez or ''
                                    )
                                    tasas_creadas += 1
                            
                            print(f"✅ {tasas_creadas} tasas vinculadas a la declaración {nodecla}")
                        except Exception as e:
                            print(f"⚠️ Error al vincular tasas: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        mensaje = f"Declaración guardada exitosamente. Número de permiso: {nodecla}"
                    
                    exito = True
                    
                    # Recargar las declaraciones y tasas
                    if negocio:
                        declaraciones = DeclaracionVolumen.objects.filter(
                            empresa=empresa,
                            rtm=rtm, 
                            expe=expe
                        ).order_by('-ano', '-mes')
                        
                        # Recargar tasas de declaración
                        from tributario.models import TasasDecla, Rubro
                        tasas_decla_raw = TasasDecla.objects.filter(
                            empresa=empresa,
                            idneg=negocio.id,
                            rtm=rtm,
                            expe=expe
                        ).order_by('rubro', 'cod_tarifa')
                        
                        # Enriquecer con información del rubro
                        tarifas_ics = []
                        for tasa in tasas_decla_raw:
                            try:
                                rubro_info = Rubro.objects.get(empresa=empresa, codigo=tasa.rubro)
                                rubro_nombre = rubro_info.descripcion
                            except Rubro.DoesNotExist:
                                rubro_nombre = "Rubro no encontrado"
                            
                            frecuencia_desc = "Mensual" if tasa.frecuencia == 'M' else "Anual" if tasa.frecuencia == 'A' else ""
                            
                            tarifas_ics.append({
                                'id': tasa.id,
                                'rubro': tasa.rubro,
                                'rubro_nombre': rubro_nombre,
                                'cod_tarifa': tasa.cod_tarifa,
                                'frecuencia': tasa.frecuencia,
                                'frecuencia_desc': frecuencia_desc,
                                'valor': tasa.valor,
                                'nodecla': tasa.nodecla,
                                'ano': tasa.ano
                            })
                        
                except Exception as e:
                    import traceback
                    error_detalle = traceback.format_exc()
                    print(f"❌ ERROR AL GUARDAR DECLARACIÓN:")
                    print(error_detalle)
                    mensaje = f"Error al guardar la declaración: {str(e)}"
                    exito = False
            else:
                # Formulario no válido - mostrar errores
                errores = []
                for field, errors in form.errors.items():
                    for error in errors:
                        errores.append(f"{field}: {error}")
                mensaje = f"Error de validación: {'; '.join(errores)}"
                exito = False
                print(f"❌ FORMULARIO NO VÁLIDO:")
                print(f"   Errores: {form.errors}")
        
        elif accion == 'eliminar':
            declaracion_id = request.POST.get('id')
            if declaracion_id:
                try:
                    declaracion = DeclaracionVolumen.objects.get(id=declaracion_id)
                    declaracion.delete()
                    mensaje = "Declaración eliminada exitosamente"
                    exito = True
                    
                    # Recargar las declaraciones
                    if negocio:
                        declaraciones = DeclaracionVolumen.objects.filter(
                            empresa=empresa,
                            rtm=rtm, 
                            expe=expe
                        ).order_by('-ano', '-mes')
                        
                except DeclaracionVolumen.DoesNotExist:
                    mensaje = "La declaración no existe"
                except Exception as e:
                    mensaje = f"Error al eliminar la declaración: {str(e)}"
    else:
        form = DeclaracionVolumenForm()
    
    # Debug: verificar que las variables se estén pasando al contexto
    print(f"DEBUG: Context RTM: {rtm}")
    print(f"DEBUG: Context EXPE: {expe}")
    print(f"DEBUG: Context Negocio: {negocio}")
    
    context = {
        'form': form,
        'negocio': negocio,
        'rtm': rtm,
        'expe': expe,
        'declaraciones': declaraciones,
        'tarifas_ics': tarifas_ics,
        'anos_disponibles': anos_disponibles,
        'mensaje': mensaje,
        'exito': exito,
        'modulo': 'Tributario',
        'descripcion': 'Declaración de Volumen de Ventas'
    }
    
    return render(request, 'declaracion_volumen.html', context)

def obtener_tarifas_escalonadas(request):
    """Vista AJAX para obtener tarifas escalonadas y calcular el impuesto"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            tipocat = data.get('tipocat', '1')
            valor = Decimal(str(data.get('valor', 0)))
            
            if valor <= 0:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'El valor debe ser mayor a 0'
                })
            
            # Usar el modelo TarifasImptoics para calcular la tarifa escalonada
            from tributario.models import TarifasImptoics
            calculo = TarifasImptoics.calcular_tarifa_escalonada(tipocat, valor)
            
            return JsonResponse(calculo)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Error en el formato de datos'
            })
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error al calcular tarifa escalonada: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })


def test_calculadora_ics(request):
    """
    Vista para la calculadora de prueba ICS
    """
    return render(request, 'test_calculadora_ics.html', {
        'titulo': 'Test - Calculadora ICS',
        'descripcion': 'Sistema de cálculo automático para declaración de volumen'
    })


def configurar_tasas_negocio(request):
    """
    Vista para configurar tasas específicas de negocios
    """
    # Obtener el código de municipio de la sesión
    empresa = request.session.get('empresa')
    if not empresa:
        print(f"DEBUG: No empresa in session. Session: {request.session}")
        return redirect('tributario:tributario_login')
    
    # Obtener parámetros de la URL
    negocio_id = request.GET.get('negocio_id', '')
    rtm = request.GET.get('rtm', '')
    expe = request.GET.get('expe', '')
    
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        # Procesar formulario de configuración de tasas
        accion = request.POST.get('accion', '')
        
        if accion == 'agregar_tarifa':
            # Lógica para agregar nueva tarifa con validación de duplicidad
            try:
                from tributario.models import TarifasICS
                idneg = request.POST.get('idneg')
                rtm = request.POST.get('rtm')
                expe = request.POST.get('expe')
                rubro = request.POST.get('rubro')
                tarifa_rubro = request.POST.get('tarifa_rubro')
                valor_personalizado = request.POST.get('valor_personalizado')
                
                if idneg and rtm and expe and rubro and tarifa_rubro and valor_personalizado:
                    # Validar que no existe una tarifa duplicada
                    tarifa_existente = TarifasICS.objects.filter(
                        empresa=empresa,
                        rtm=rtm,
                        expe=expe,
                        rubro=rubro,
                        cod_tarifa=tarifa_rubro
                    ).first()
                    
                    if tarifa_existente:
                        mensaje = f"⚠️ Ya existe una tarifa con estos datos:\n"
                        mensaje += f"• Empresa: {empresa}\n"
                        mensaje += f"• RTM: {rtm}\n"
                        mensaje += f"• Expediente: {expe}\n"
                        mensaje += f"• Rubro: {rubro}\n"
                        mensaje += f"• Código de Tarifa: {tarifa_rubro}\n\n"
                        mensaje += f"Valor actual: ${tarifa_existente.valor}\n\n"
                        mensaje += "¿Desea actualizar el valor existente?"
                        exito = False
                        
                        # Si es una petición AJAX, devolver JSON con información de duplicidad
                        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                            return JsonResponse({
                                'exito': False,
                                'mensaje': mensaje,
                                'duplicado': True,
                                'tarifa_existente': {
                                    'id': tarifa_existente.id,
                                    'valor_actual': str(tarifa_existente.valor)
                                }
                            })
                    else:
                        # No existe duplicado, crear nueva tarifa ICS
                        # Obtener cuenta y cuentarez del formulario
                        cuenta = request.POST.get('cuenta', '')
                        cuentarez = request.POST.get('cuentarez', '')
                        
                        nueva_tarifa = TarifasICS.objects.create(
                            empresa=empresa,
                            idneg=int(idneg),
                            rtm=rtm,
                            expe=expe,
                            rubro=rubro,
                            cod_tarifa=tarifa_rubro,
                            valor=float(valor_personalizado),
                            cuenta=cuenta,
                            cuentarez=cuentarez
                        )
                        mensaje = "✅ Tarifa agregada exitosamente"
                        exito = True
                        
                        # Si es una petición AJAX, devolver JSON de éxito
                        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                            return JsonResponse({
                                'exito': True,
                                'mensaje': mensaje,
                                'duplicado': False
                            })
                else:
                    mensaje = "❌ Faltan datos obligatorios para agregar la tarifa"
                    exito = False
                    
                    # Si es una petición AJAX, devolver JSON de error
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({
                            'exito': False,
                            'mensaje': mensaje,
                            'duplicado': False
                        })
            except Exception as e:
                mensaje = f"❌ Error al agregar tarifa: {str(e)}"
                exito = False
                
                # Si es una petición AJAX, devolver JSON de error
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'exito': False,
                        'mensaje': mensaje,
                        'duplicado': False
                    })
                
        elif accion == 'actualizar_tarifa_duplicada':
            # Lógica para actualizar tarifa existente cuando se detecta duplicidad
            try:
                from tributario.models import TarifasICS
                tarifa_id = request.POST.get('tarifa_id', '')
                nuevo_valor = request.POST.get('nuevo_valor', '')
                
                if tarifa_id and nuevo_valor:
                    tarifa = TarifasICS.objects.get(id=tarifa_id)
                    valor_anterior = tarifa.valor
                    tarifa.valor = float(nuevo_valor)
                    tarifa.save()
                    
                    mensaje = f"✅ Tarifa actualizada exitosamente\n"
                    mensaje += f"Valor anterior: ${valor_anterior}\n"
                    mensaje += f"Nuevo valor: ${nuevo_valor}"
                    exito = True
                    
                    # Si es una petición AJAX, devolver JSON de éxito
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({
                            'exito': True,
                            'mensaje': mensaje,
                            'valor_anterior': str(valor_anterior),
                            'valor_nuevo': str(nuevo_valor)
                        })
                else:
                    mensaje = "❌ Datos incompletos para actualizar tarifa"
                    exito = False
                    
                    # Si es una petición AJAX, devolver JSON de error
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({
                            'exito': False,
                            'mensaje': mensaje
                        })
            except TarifasICS.DoesNotExist:
                mensaje = "❌ Tarifa no encontrada"
                exito = False
                
                # Si es una petición AJAX, devolver JSON de error
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'exito': False,
                        'mensaje': mensaje
                    })
            except Exception as e:
                mensaje = f"❌ Error al actualizar tarifa: {str(e)}"
                exito = False
                
                # Si es una petición AJAX, devolver JSON de error
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'exito': False,
                        'mensaje': mensaje
                    })
                
        elif accion == 'actualizar_valor':
            # Lógica para actualizar valor de tarifa
            tarifa_id = request.POST.get('tarifa_id', '')
            valor = request.POST.get('valor', '')
            
            if tarifa_id and valor:
                try:
                    from tributario.models import TarifasICS
                    tarifa = TarifasICS.objects.get(id=tarifa_id)
                    tarifa.valor = float(valor)
                    tarifa.save()
                    mensaje = "✅ Valor de tarifa actualizado exitosamente"
                    exito = True
                except TarifasICS.DoesNotExist:
                    mensaje = "❌ Tarifa no encontrada"
                    exito = False
                except Exception as e:
                    mensaje = f"❌ Error al actualizar tarifa: {str(e)}"
                    exito = False
            else:
                mensaje = "❌ Datos incompletos para actualizar tarifa"
                exito = False
                
        elif accion == 'eliminar_tarifa':
            # Lógica para eliminar tarifa
            tarifa_id = request.POST.get('tarifa_id', '')
            
            if tarifa_id:
                try:
                    from tributario.models import TarifasICS
                    tarifa = TarifasICS.objects.get(id=tarifa_id)
                    tarifa.delete()
                    mensaje = "✅ Tarifa eliminada exitosamente"
                    exito = True
                except TarifasICS.DoesNotExist:
                    mensaje = "❌ Tarifa no encontrada"
                    exito = False
                except Exception as e:
                    mensaje = f"❌ Error al eliminar tarifa: {str(e)}"
                    exito = False
            else:
                mensaje = "❌ ID de tarifa no proporcionado"
                exito = False
    
    # Obtener datos del negocio si se proporciona ID
    negocio = None
    if negocio_id:
        try:
            negocio = Negocio.objects.get(id=negocio_id, empresa=empresa)
        except Negocio.DoesNotExist:
            mensaje = "❌ Negocio no encontrado"
            exito = False
    elif rtm and expe:
        try:
            negocio = Negocio.objects.get(rtm=rtm, expe=expe, empresa=empresa)
        except Negocio.DoesNotExist:
            mensaje = "❌ Negocio no encontrado"
            exito = False
    
    # Obtener planes de arbitrio disponibles
    from tributario.models import PlanArbitrio
    # Ordenar por: empresa, Año, Rubro, Cod_Tarifa, Categoría (tipocat), Código
    planes_arbitrio = PlanArbitrio.objects.filter(empresa=empresa).order_by('empresa', 'ano', 'rubro', 'cod_tarifa', 'tipocat', 'codigo')
    
    # Obtener tarifas ICS del negocio si existe
    tarifas_ics = []
    if negocio:
        from tributario.models import TarifasICS
        tarifas_ics = TarifasICS.objects.filter(
            idneg=negocio.id,
            rtm=negocio.rtm,
            expe=negocio.expe
        ).order_by('rubro', 'cod_tarifa')
    
    # Crear formulario para agregar tarifas
    from .forms import TarifasICSForm
    form = TarifasICSForm() if negocio else None
    
    # Obtener rubros disponibles
    from tributario.models import Rubro
    rubros = Rubro.objects.filter(empresa=empresa).order_by('codigo')
    
    print(f"DEBUG: Rendering template with empresa: {empresa}")
    print(f"DEBUG: Negocio: {negocio}")
    print(f"DEBUG: Tarifas ICS: {len(tarifas_ics)} tarifas")
    print(f"DEBUG: Rubros: {len(rubros)} rubros")
    
    return render(request, 'configurar_tasas_negocio.html', {
        'negocio': negocio,
        'planes_arbitrio': planes_arbitrio,
        'tarifas_ics': tarifas_ics,
        'rubros': rubros,
        'form': form,
        'mensaje': mensaje,
        'exito': exito,
        'empresa': empresa
    })

@csrf_exempt
def obtener_tarifas_rubro(request):
    """Vista AJAX para obtener tarifas asociadas a un rubro específico"""
    if request.method == 'POST':
        try:
            rubro_codigo = request.POST.get('rubro', '').strip()
            
            if not rubro_codigo:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Código de rubro requerido',
                    'tarifas': []
                })
            
            # Obtener el código de municipio de la sesión
            empresa = request.session.get('empresa')
            if not empresa:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Sesión no válida',
                    'tarifas': []
                })
            
            # Buscar tarifas asociadas al rubro
            from tributario.models import Tarifas
            tarifas = Tarifas.objects.filter(
                empresa=empresa,
                rubro=rubro_codigo
            ).order_by('cod_tarifa')
            
            # Convertir a formato JSON
            tarifas_data = []
            for tarifa in tarifas:
                tarifas_data.append({
                    'cod_tarifa': tarifa.cod_tarifa,
                    'descripcion': tarifa.descripcion,
                    'valor': str(tarifa.valor),
                    'rubro': tarifa.rubro,
                    'empresa': tarifa.empresa
                })
            
            logger.info(f"Tarifas encontradas para rubro {rubro_codigo}: {len(tarifas_data)}")
            
            return JsonResponse({
                'exito': True,
                'mensaje': f'Se encontraron {len(tarifas_data)} tarifas para el rubro {rubro_codigo}',
                'tarifas': tarifas_data
            })
            
        except Exception as e:
            logger.error(f"Error al obtener tarifas del rubro: {str(e)}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error al obtener tarifas: {str(e)}',
                'tarifas': []
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido',
        'tarifas': []
    })

@csrf_exempt
def buscar_concepto_miscelaneos(request):
    """Vista AJAX para buscar conceptos de cobro en misceláneos"""
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        # Obtener datos del FormData
        empresa = request.POST.get('empresa', '').strip()
        cod_tarifa = request.POST.get('cod_tarifa', '').strip()
        
        # Validar campos requeridos
        if not empresa or not cod_tarifa:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Empresa y código de tarifa son requeridos'
            })
        
        from tributario.models import Tarifas
        
        # Buscar la tarifa en la base de datos
        try:
            tarifa = Tarifas.objects.get(
                empresa=empresa, 
                cod_tarifa=cod_tarifa
            )
            
            return JsonResponse({
                'exito': True,
                'concepto': {
                    'cod_tarifa': tarifa.cod_tarifa or '',
                    'descripcion': tarifa.descripcion or '',
                    'valor': str(tarifa.valor) if tarifa.valor else '0',
                    'frecuencia': tarifa.frecuencia or '',
                    'tipo': tarifa.tipo or '',
                    'ano': str(tarifa.ano) if tarifa.ano else '',
                    'rubro': tarifa.rubro or ''
                },
                'mensaje': 'Concepto encontrado exitosamente'
            })
            
        except Tarifas.DoesNotExist:
            return JsonResponse({
                'exito': False,
                'mensaje': 'No se encontró un concepto con ese código'
            })
            
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al buscar concepto: {str(e)}'
        })

# FUNCIÓN DUPLICADA ELIMINADA: logout_view() - YA EXISTE EN LÍNEA 115
# Esta función duplicada causaba el error de no retornar HttpResponse

@csrf_exempt
def calcular_impuesto_productos_controlados_ajax(request):
    """Vista AJAX para calcular impuesto de productos controlados usando tarifasimptoics"""
    if request.method != 'POST':
        return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'})
    
    try:
        valor_productos_controlados = request.POST.get('valor_productos_controlados', '0')
        valor = float(valor_productos_controlados)
        
        if valor <= 0:
            return JsonResponse({
                'exito': False,
                'mensaje': 'El valor de productos controlados debe ser mayor a 0'
            })
        
        # Usar el método del modelo TarifasImptoics para calcular la tarifa escalonada
        from tributario.models import TarifasImptoics
        resultado = TarifasImptoics.calcular_tarifa_escalonada('2', valor)
        
        if resultado['exito']:
            return JsonResponse({
                'exito': True,
                'total': float(resultado['total']),
                'detalle': resultado['detalle'],
                'valor_original': float(resultado['valor_original']),
                'tipocat': resultado['tipocat']
            })
        else:
            return JsonResponse({
                'exito': False,
                'mensaje': resultado['mensaje']
            })
            
    except ValueError:
        return JsonResponse({
            'exito': False,
            'mensaje': 'El valor ingresado no es un número válido'
        })
    except Exception as e:
        logger.error(f"Error en cálculo de productos controlados: {str(e)}")
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error interno: {str(e)}'
        })

# Importar declaracion_volumen desde modules.tributario.views
from tributario.views import declaracion_volumen


@csrf_exempt
def grabar_plan_arbitrio_ajax(request):
    """
    Vista AJAX simplificada para grabar/actualizar plan de arbitrio
    Guarda directamente según la estructura de la tabla planarbitio
    """
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        from tributario.models import PlanArbitrio, TipoCategoria
        from decimal import Decimal, InvalidOperation
        
        # Obtener todos los datos del POST
        empresa = request.POST.get('empresa', '').strip()
        rubro = request.POST.get('rubro', '').strip()
        cod_tarifa = request.POST.get('cod_tarifa', '').strip() or None
        tipocat = request.POST.get('tipocat', '').strip()
        ano = request.POST.get('ano', '').strip()
        codigo = request.POST.get('codigo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip() or ''
        minimo_str = request.POST.get('minimo', '0.00').strip()
        maximo_str = request.POST.get('maximo', '0.00').strip()
        valor_str = request.POST.get('valor', '0.00').strip()
        
        # Validar campos obligatorios
        if not empresa:
            return JsonResponse({
                'exito': False,
                'mensaje': 'El campo Empresa es obligatorio'
            })
        
        if not ano:
            return JsonResponse({
                'exito': False,
                'mensaje': 'El campo Año es obligatorio'
            })
        
        if not codigo:
            return JsonResponse({
                'exito': False,
                'mensaje': 'El campo Código es obligatorio'
            })
        
        # Convertir año a Decimal
        try:
            ano_decimal = Decimal(str(int(float(ano))))
        except (ValueError, InvalidOperation):
            return JsonResponse({
                'exito': False,
                'mensaje': 'El año debe ser un número válido'
            })
        
        # Procesar tipocat - debe ser código de 1 carácter de tipocategoria
        tipocat_final = ''
        if tipocat:
            tipocat_clean = tipocat.strip()
            # Si viene con formato "1. Descripción", extraer solo el código
            if '.' in tipocat_clean:
                tipocat_final = tipocat_clean.split('.')[0].strip()
            elif '-' in tipocat_clean:
                tipocat_final = tipocat_clean.split('-')[0].strip()
            else:
                tipocat_final = tipocat_clean
            # Limitar a 1 carácter
            tipocat_final = tipocat_final[:1] if tipocat_final else ''
            # Validar que exista en tipocategoria si tiene valor
            if tipocat_final:
                try:
                    categoria_existe = TipoCategoria.objects.filter(codigo=tipocat_final).exists()
                    if not categoria_existe:
                        return JsonResponse({
                            'exito': False,
                            'mensaje': f'El código de categoría "{tipocat_final}" no existe en la tabla tipocategoria'
                        })
                except Exception as e:
                    print(f"Error al validar tipocat: {e}")
        
        # Convertir valores numéricos
        try:
            minimo = Decimal(minimo_str.replace(',', '.')) if minimo_str else Decimal('0.00')
        except (ValueError, InvalidOperation):
            minimo = Decimal('0.00')
        
        try:
            maximo = Decimal(maximo_str.replace(',', '.')) if maximo_str else Decimal('0.00')
        except (ValueError, InvalidOperation):
            maximo = Decimal('0.00')
        
        try:
            valor = Decimal(valor_str.replace(',', '.')) if valor_str else Decimal('0.00')
        except (ValueError, InvalidOperation):
            # Si no hay valor, calcular automáticamente
            if minimo and maximo:
                valor = (minimo + maximo) / 2
            elif minimo:
                valor = minimo
            elif maximo:
                valor = maximo
            else:
                valor = Decimal('0.00')
        
        # Buscar si ya existe un plan con la misma clave única
        filtros_busqueda = {
            'empresa': empresa,
            'rubro': rubro or '',
            'cod_tarifa': cod_tarifa or '',
            'tipocat': tipocat_final or '',
            'ano': ano_decimal,
            'codigo': codigo
        }
        
        try:
            plan_existente = PlanArbitrio.objects.get(**filtros_busqueda)
            # ACTUALIZAR registro existente
            plan_existente.descripcion = descripcion
            plan_existente.minimo = minimo
            plan_existente.maximo = maximo
            plan_existente.valor = valor
            plan_existente.save()
            
            return JsonResponse({
                'exito': True,
                'mensaje': f'✅ Plan de arbitrio {codigo} actualizado exitosamente.',
                'accion': 'actualizado',
                'id': plan_existente.id
            })
        except PlanArbitrio.DoesNotExist:
            # CREAR nuevo registro
            nuevo_plan = PlanArbitrio.objects.create(
                empresa=empresa,
                rubro=rubro or '',
                cod_tarifa=cod_tarifa or '',
                tipocat=tipocat_final or '',
                ano=ano_decimal,
                codigo=codigo,
                descripcion=descripcion,
                minimo=minimo,
                maximo=maximo,
                valor=valor
            )
            
            return JsonResponse({
                'exito': True,
                'mensaje': f'✅ Plan de arbitrio {codigo} creado exitosamente.',
                'accion': 'creado',
                'id': nuevo_plan.id
            })
        except PlanArbitrio.MultipleObjectsReturned:
            # Si hay múltiples registros, actualizar el primero
            plan_existente = PlanArbitrio.objects.filter(**filtros_busqueda).first()
            plan_existente.descripcion = descripcion
            plan_existente.minimo = minimo
            plan_existente.maximo = maximo
            plan_existente.valor = valor
            plan_existente.save()
            
            return JsonResponse({
                'exito': True,
                'mensaje': f'✅ Plan de arbitrio {codigo} actualizado exitosamente.',
                'accion': 'actualizado',
                'id': plan_existente.id
            })
            
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error en grabar_plan_arbitrio_ajax: {e}")
        print(f"Detalle: {error_detail}")
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al grabar plan de arbitrio: {str(e)}'
        })


def tipocategoria_crud(request):
    """Vista principal para el CRUD de tipos de categoría"""
    from .forms import TipoCategoriaForm
    from tributario.models import TipoCategoria
    
    mensaje = None
    exito = False
    categoria = None
    
    if request.method == 'POST':
        accion = request.POST.get('accion', '')
        
        if accion == 'guardar':
            form = TipoCategoriaForm(request.POST)
            if form.is_valid():
                try:
                    codigo = form.cleaned_data.get('codigo', '').strip().upper()
                    descripcion = form.cleaned_data.get('descripcion', '').strip()
                    
                    # Verificar si ya existe una categoría con ese código
                    categoria_existente = TipoCategoria.objects.filter(codigo=codigo).first()
                    
                    if categoria_existente:
                        # Actualizar
                        categoria_existente.descripcion = descripcion
                        categoria_existente.save()
                        mensaje = f'✅ Tipo de categoría {codigo} actualizado exitosamente.'
                        exito = True
                        categoria = categoria_existente
                    else:
                        # Crear nuevo
                        categoria = TipoCategoria.objects.create(
                            codigo=codigo,
                            descripcion=descripcion
                        )
                        mensaje = f'✅ Tipo de categoría {codigo} creado exitosamente.'
                        exito = True
                except Exception as e:
                    mensaje = f'❌ Error al guardar tipo de categoría: {str(e)}'
                    exito = False
            else:
                mensaje = f'❌ Errores en el formulario: {form.errors}'
                exito = False
                form = TipoCategoriaForm()
        
        elif accion == 'eliminar':
            codigo_eliminar = request.POST.get('codigo_eliminar', '').strip().upper()
            try:
                categoria_eliminar = TipoCategoria.objects.get(codigo=codigo_eliminar)
                categoria_eliminar.delete()
                mensaje = f'✅ Tipo de categoría {codigo_eliminar} eliminado exitosamente.'
                exito = True
            except TipoCategoria.DoesNotExist:
                mensaje = f'❌ No se encontró el tipo de categoría con código {codigo_eliminar}.'
                exito = False
            except Exception as e:
                mensaje = f'❌ Error al eliminar tipo de categoría: {str(e)}'
                exito = False
        
        elif accion == 'editar':
            codigo_editar = request.POST.get('codigo_editar', '').strip().upper()
            try:
                categoria = TipoCategoria.objects.get(codigo=codigo_editar)
                form = TipoCategoriaForm(instance=categoria)
            except TipoCategoria.DoesNotExist:
                mensaje = f'❌ No se encontró el tipo de categoría con código {codigo_editar}.'
                exito = False
                form = TipoCategoriaForm()
        else:
            form = TipoCategoriaForm()
    else:
        form = TipoCategoriaForm()
    
    # Obtener todas las categorías para mostrar en la lista
    categorias = TipoCategoria.objects.all().order_by('codigo')
    
    context = {
        'form': form,
        'categorias': categorias,
        'mensaje': mensaje,
        'exito': exito,
        'categoria': categoria,
        'titulo': 'Gestión de Tipos de Categoría'
    }
    
    return render(request, 'tipocategoria.html', context)
