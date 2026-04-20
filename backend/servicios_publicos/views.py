"""
Vistas para Módulo de Servicios Públicos / Facturación de Agua Potable
"""
import json
import logging
from decimal import Decimal
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Sum, Count, Q

from .models import (
    SPRubro, SPTarifa, SPTramoTarifa, SPCatastroUsuario,
    SPMedidor, SPCicloRuta, SPLectura, SPFactura, SPDetalleFactura,
    SPOrdenTrabajo, SPInsumoOrdenTrabajo, SPCorteSuspension, SPConsecutivo,
    SPProcesoCalendario,
    SPResponsable, SPConceptoOT,
)

from django.utils import timezone
from tributario.models import PagoVariosTemp, NoRecibos, Rubro as TributarioRubro
from core.models import Municipio
from catastro.models import Barrios

logger = logging.getLogger(__name__)


def _get_empresa(request):
    return request.session.get('empresa', '')


def _requiere_sesion(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return None


# ═══════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════
def sp_dashboard(request):
    redir = _requiere_sesion(request)
    if redir:
        return redir
    empresa = _get_empresa(request)
    
    # Estadísticas rápidas
    total_abonados   = SPCatastroUsuario.objects.filter(empresa=empresa).count()
    abonados_activos = SPCatastroUsuario.objects.filter(empresa=empresa, estado='A').count()
    facturas_pendientes = SPFactura.objects.filter(empresa=empresa, estado__in=['E', 'V']).count()
    ordenes_pendientes  = SPOrdenTrabajo.objects.filter(empresa=empresa, estado__in=['P', 'A', 'E']).count()
    lecturas_pendientes = SPLectura.objects.filter(empresa=empresa, estado='P').count()
    
    # Recaudación del mes actual
    hoy = date.today()
    recaudacion_mes = SPFactura.objects.filter(
        empresa=empresa,
        estado='P',
        fecha_pago__year=hoy.year,
        fecha_pago__month=hoy.month,
    ).aggregate(total=Sum('total'))['total'] or Decimal('0')
    
    # Últimas facturas emitidas
    ultimas_facturas = SPFactura.objects.filter(empresa=empresa).order_by('-fecha_creacion')[:8]
    
    # Últimas órdenes de trabajo
    ultimas_ordenes = SPOrdenTrabajo.objects.filter(empresa=empresa).order_by('-fecha_creacion')[:6]

    ctx = {
        'total_abonados': total_abonados,
        'abonados_activos': abonados_activos,
        'facturas_pendientes': facturas_pendientes,
        'ordenes_pendientes': ordenes_pendientes,
        'lecturas_pendientes': lecturas_pendientes,
        'recaudacion_mes': recaudacion_mes,
        'ultimas_facturas': ultimas_facturas,
        'ultimas_ordenes': ultimas_ordenes,
        'empresa': empresa,
        'usuario': request.session.get('nombre', ''),
        'modulo': 'Servicios Públicos',
        'ano_actual': hoy.year,
        'mes_actual': hoy.month,
    }
    return render(request, 'servicios_publicos/dashboard.html', ctx)


# ═══════════════════════════════════════════════════════════
# CALENDARIO DE PROCESOS
# ═══════════════════════════════════════════════════════════
def sp_calendario(request):
    redir = _requiere_sesion(request)
    if redir:
        return redir
    empresa = _get_empresa(request)
    return render(request, "servicios_publicos/calendario.html", {"empresa": empresa, "usuario": request.session.get("nombre", "")})


def sp_calendario_eventos(request):
    if not request.session.get("user_id"):
        return JsonResponse({"detail": "No autenticado"}, status=401)

    empresa = _get_empresa(request)
    qs = SPProcesoCalendario.objects.filter(empresa=empresa)

    # FullCalendar envía start/end (ISO) para limitar carga.
    start = request.GET.get("start")
    end = request.GET.get("end")
    if start and end:
        try:
            # Filtrar por rango aproximado usando strings ISO (Django parsea a datetime si usamos fromisoformat)
            start_dt = timezone.datetime.fromisoformat(start.replace("Z", "+00:00"))
            end_dt = timezone.datetime.fromisoformat(end.replace("Z", "+00:00"))
            qs = qs.filter(inicio__lt=end_dt).filter(Q(fin__gte=start_dt) | Q(fin__isnull=True, inicio__gte=start_dt))
        except Exception:
            pass

    eventos = []
    for e in qs[:2000]:
        eventos.append(
            {
                "id": e.id,
                "title": e.titulo,
                "start": e.inicio.isoformat(),
                "end": e.fin.isoformat() if e.fin else None,
                "allDay": bool(e.todo_el_dia),
                "color": e.color or None,
                "extendedProps": {
                    "tipo": e.tipo,
                    "descripcion": e.descripcion or "",
                },
            }
        )

    return JsonResponse(eventos, safe=False)


@require_POST
def sp_calendario_crear(request):
    redir = _requiere_sesion(request)
    if redir:
        return redir

    empresa = _get_empresa(request)
    titulo = (request.POST.get("titulo") or "").strip()
    tipo = (request.POST.get("tipo") or "O").strip()[:1]
    descripcion = (request.POST.get("descripcion") or "").strip() or None
    inicio_raw = (request.POST.get("inicio") or "").strip()
    fin_raw = (request.POST.get("fin") or "").strip()
    todo_el_dia = request.POST.get("todo_el_dia") == "1"
    color = (request.POST.get("color") or "").strip() or None

    if not titulo or not inicio_raw:
        messages.error(request, "Título e inicio son obligatorios.")
        return redirect("servicios_publicos:calendario")

    try:
        # input type="datetime-local" viene sin zona; guardamos en timezone local del servidor
        inicio = timezone.make_aware(timezone.datetime.fromisoformat(inicio_raw))
        fin = None
        if fin_raw:
            fin = timezone.make_aware(timezone.datetime.fromisoformat(fin_raw))
    except Exception:
        messages.error(request, "Fechas inválidas. Use el selector del formulario.")
        return redirect("servicios_publicos:calendario")

    SPProcesoCalendario.objects.create(
        empresa=empresa,
        tipo=tipo if tipo in dict(SPProcesoCalendario.TIPO_CHOICES) else "O",
        titulo=titulo,
        descripcion=descripcion,
        inicio=inicio,
        fin=fin,
        todo_el_dia=todo_el_dia,
        color=color,
        usuario=request.session.get("usuario", "") or request.session.get("nombre", ""),
    )
    messages.success(request, "✅ Proceso agregado al calendario.")
    return redirect("servicios_publicos:calendario")


# ═══════════════════════════════════════════════════════════
# RUBROS
# ═══════════════════════════════════════════════════════════
def rubros_lista(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    rubros = SPRubro.objects.filter(empresa=empresa).order_by('codigo')
    return render(request, 'servicios_publicos/rubros/lista.html', {
        'rubros': rubros, 'empresa': empresa,
    })


def rubro_form(request, pk=None):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    instance = get_object_or_404(SPRubro, pk=pk, empresa=empresa) if pk else None
    
    if request.method == 'POST':
        data = {
            'empresa': empresa,
            'codigo': request.POST.get('codigo', '').strip().upper(),
            'descripcion': request.POST.get('descripcion', '').strip(),
            'tipo_cobro': request.POST.get('tipo_cobro', 'F'),
            'cuenta': request.POST.get('cuenta', '').strip() or None,
            'cuentarez': request.POST.get('cuentarez', '').strip() or None,
            'activo': request.POST.get('activo') == '1',
            'usuario': request.session.get('usuario', ''),
        }
        if not data['codigo'] or not data['descripcion']:
            messages.error(request, 'Código y descripción son obligatorios.')
        else:
            try:
                if instance:
                    for k, v in data.items():
                        setattr(instance, k, v)
                    instance.save()
                    messages.success(request, f'✅ Rubro {data["codigo"]} actualizado.')
                else:
                    SPRubro.objects.create(**data)
                    messages.success(request, f'✅ Rubro {data["codigo"]} creado exitosamente.')
                return redirect('servicios_publicos:rubros_lista')
            except Exception as e:
                messages.error(request, f'❌ Error: {e}')
    
    return render(request, 'servicios_publicos/rubros/formulario.html', {
        'instance': instance, 'empresa': empresa,
        'titulo': 'Editar Rubro' if instance else 'Nuevo Rubro',
    })


def rubro_eliminar(request, pk):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    rubro = get_object_or_404(SPRubro, pk=pk, empresa=empresa)
    if request.method == 'POST':
        codigo = rubro.codigo
        rubro.delete()
        messages.success(request, f'Rubro {codigo} eliminado.')
    return redirect('servicios_publicos:rubros_lista')


# ═══════════════════════════════════════════════════════════
# TARIFAS
# ═══════════════════════════════════════════════════════════
def tarifas_lista(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    rubros  = SPRubro.objects.filter(empresa=empresa, activo=True)
    rubro_sel = request.GET.get('rubro', '')
    tarifas = SPTarifa.objects.filter(empresa=empresa)
    if rubro_sel:
        tarifas = tarifas.filter(rubro=rubro_sel)
    return render(request, 'servicios_publicos/tarifas/lista.html', {
        'tarifas': tarifas, 'rubros': rubros, 'rubro_sel': rubro_sel, 'empresa': empresa,
    })


def tarifa_form(request, pk=None):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    instance = get_object_or_404(SPTarifa, pk=pk, empresa=empresa) if pk else None
    rubros = SPRubro.objects.filter(empresa=empresa, activo=True)
    
    if request.method == 'POST':
        try:
            rubro_codigo = request.POST.get('rubro', '').strip()
            rubro_obj = SPRubro.objects.filter(empresa=empresa, codigo=rubro_codigo, activo=True).first() if rubro_codigo else None
            if not rubro_obj:
                raise ValueError("Debe seleccionar un rubro válido.")

            tipo_cobro = rubro_obj.tipo_cobro  # F=fija, M=medición, A=anual
            data = {
                'empresa': empresa,
                'rubro': rubro_codigo,
                'ano': int(request.POST.get('ano', date.today().year)),
                'descripcion': request.POST.get('descripcion', '').strip() or None,
                'cargo_fijo': Decimal(request.POST.get('cargo_fijo', '0') or '0'),
                'precio_m3': Decimal(request.POST.get('precio_m3', '0') or '0'),
                'minimo_m3': Decimal(request.POST.get('minimo_m3', '0') or '0'),
                'usa_tramos': request.POST.get('usa_tramos') == '1',
                'activo': request.POST.get('activo') == '1',
                'usuario': request.session.get('usuario', ''),
            }

            # Normalizar y validar según el tipo de cobro del rubro
            if tipo_cobro in ('F', 'A'):
                # Tarifa fija/anual: solo cargo fijo aplica
                if data['cargo_fijo'] <= 0:
                    raise ValueError("Para rubros de tarifa fija/anual, el cargo fijo debe ser mayor que 0.")
                data['precio_m3'] = Decimal('0')
                data['minimo_m3'] = Decimal('0')
                data['usa_tramos'] = False
            elif tipo_cobro == 'M':
                # Medición: puede ser precio por m3 o por tramos; cargo fijo opcional
                if data['usa_tramos']:
                    data['precio_m3'] = Decimal('0')
                    data['minimo_m3'] = Decimal('0')
                else:
                    if data['precio_m3'] <= 0:
                        raise ValueError("Para tarifa por medición sin tramos, el precio por m³ debe ser mayor que 0.")
            else:
                raise ValueError("Tipo de cobro de rubro no soportado.")

            if instance:
                for k, v in data.items():
                    setattr(instance, k, v)
                instance.save()
                messages.success(request, f'✅ Tarifa actualizada.')
                if instance.usa_tramos:
                    return redirect('servicios_publicos:tarifa_tramos', pk=instance.pk)
                return redirect('servicios_publicos:tarifas_lista')
            else:
                obj = SPTarifa.objects.create(**data)
                messages.success(request, '✅ Tarifa creada. Configure tramos si aplica.')
                if obj.usa_tramos:
                    return redirect('servicios_publicos:tarifa_tramos', pk=obj.pk)
                return redirect('servicios_publicos:tarifas_lista')
        except Exception as e:
            messages.error(request, f'❌ Error: {e}')
    
    return render(request, 'servicios_publicos/tarifas/formulario.html', {
        'instance': instance, 'rubros': rubros, 'empresa': empresa,
        'titulo': 'Editar Tarifa' if instance else 'Nueva Tarifa',
        'ano_actual': date.today().year,
    })


def tarifa_tramos(request, pk):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    tarifa = get_object_or_404(SPTarifa, pk=pk, empresa=empresa)
    tramos = tarifa.tramos.all().order_by('orden')
    return render(request, 'servicios_publicos/tarifas/tramos.html', {
        'tarifa': tarifa, 'tramos': tramos, 'empresa': empresa,
    })


# ═══════════════════════════════════════════════════════════
# CATASTRO DE USUARIOS
# ═══════════════════════════════════════════════════════════
def catastro_lista(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    
    # Filtros
    q_nombre   = request.GET.get('nombre', '').strip()
    q_estado   = request.GET.get('estado', '')
    q_categoria = request.GET.get('categoria', '')
    q_ciclo    = request.GET.get('ciclo', '')
    
    qs = SPCatastroUsuario.objects.filter(empresa=empresa)
    if q_nombre:
        qs = qs.filter(Q(nombre__icontains=q_nombre) | Q(codigo_abonado__icontains=q_nombre) | Q(identidad__icontains=q_nombre))
    if q_estado:
        qs = qs.filter(estado=q_estado)
    if q_categoria:
        qs = qs.filter(categoria=q_categoria)
    if q_ciclo:
        qs = qs.filter(ciclo=q_ciclo)
    
    qs = qs.order_by('ciclo', 'ruta', 'secuencia', 'nombre')
    ciclos = SPCicloRuta.objects.filter(empresa=empresa).values_list('ciclo', flat=True).distinct()
    
    return render(request, 'servicios_publicos/catastro/lista.html', {
        'abonados': qs, 'empresa': empresa,
        'q_nombre': q_nombre, 'q_estado': q_estado, 'q_categoria': q_categoria, 'q_ciclo': q_ciclo,
        'ciclos': ciclos,
        'CATEGORIA_CHOICES': SPCatastroUsuario.CATEGORIA_CHOICES,
        'ESTADO_CHOICES': SPCatastroUsuario.ESTADO_CHOICES,
        'total': qs.count(),
    })


def catastro_form(request, pk=None):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    instance = get_object_or_404(SPCatastroUsuario, pk=pk, empresa=empresa) if pk else None
    ciclos = SPCicloRuta.objects.filter(empresa=empresa, activo=True)
    municipio_desc = request.session.get("municipio_descripcion") or None
    if not municipio_desc:
        municipio_obj = Municipio.objects.filter(codigo=empresa).first()
        municipio_desc = municipio_obj.descripcion if municipio_obj else ""

    depto = (empresa or "")[:2]
    codmuni = (empresa or "")[2:4]
    barrios = Barrios.objects.filter(empresa=empresa, depto=depto, codmuni=codmuni).order_by("descripcion", "codbarrio")
    
    if request.method == 'POST':
        try:
            barrio_id = request.POST.get("barrio_id") or ""
            barrio_obj = Barrios.objects.filter(pk=barrio_id, empresa=empresa, depto=depto, codmuni=codmuni).first() if barrio_id else None
            data = {
                'empresa': empresa,
                'codigo_abonado': request.POST.get('codigo_abonado', '').strip(),
                'identidad': request.POST.get('identidad', '').strip() or None,
                'nombre': request.POST.get('nombre', '').strip(),
                'direccion': request.POST.get('direccion', '').strip(),
                'barrio': (barrio_obj.descripcion or "").strip() if barrio_obj else None,
                'municipio_nombre': (municipio_desc or "").strip() or None,
                'categoria': request.POST.get('categoria', 'D'),
                'estado': request.POST.get('estado', 'A'),
                'ciclo': request.POST.get('ciclo', '').strip() or None,
                'ruta': request.POST.get('ruta', '').strip() or None,
                'secuencia': int(request.POST.get('secuencia', '0') or '0'),
                'telefono': request.POST.get('telefono', '').strip() or None,
                'celular': request.POST.get('celular', '').strip() or None,
                'correo': request.POST.get('correo', '').strip() or None,
                'referencia': request.POST.get('referencia', '').strip() or None,
                'latitud': Decimal(request.POST.get('latitud') or '0') if request.POST.get('latitud') else None,
                'longitud': Decimal(request.POST.get('longitud') or '0') if request.POST.get('longitud') else None,
                'comentario': request.POST.get('comentario', '').strip() or None,
                'fecha_conexion': request.POST.get('fecha_conexion') or None,
                'usuario': request.session.get('usuario', ''),
            }
            if not data['codigo_abonado'] or not data['nombre']:
                messages.error(request, 'Código de abonado y nombre son obligatorios.')
            else:
                if instance:
                    for k, v in data.items():
                        setattr(instance, k, v)
                    instance.save()
                    messages.success(request, f'✅ Abonado {data["codigo_abonado"]} actualizado.')
                else:
                    SPCatastroUsuario.objects.create(**data)
                    messages.success(request, f'✅ Abonado {data["codigo_abonado"]} creado.')
                return redirect('servicios_publicos:catastro_lista')
        except Exception as e:
            messages.error(request, f'❌ Error: {e}')
    
    return render(request, 'servicios_publicos/catastro/formulario.html', {
        'instance': instance, 'empresa': empresa, 'ciclos': ciclos,
        'titulo': 'Editar Abonado' if instance else 'Nuevo Abonado',
        'CATEGORIA_CHOICES': SPCatastroUsuario.CATEGORIA_CHOICES,
        'ESTADO_CHOICES': SPCatastroUsuario.ESTADO_CHOICES,
        'municipio_desc': municipio_desc,
        'barrios': barrios,
    })


def catastro_mapa(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    
    # Filtros para el mapa
    q_ciclo = request.GET.get('ciclo', '')
    
    # Solo mostrar abonados con lat/long
    qs = SPCatastroUsuario.objects.filter(empresa=empresa).filter(
        Q(latitud__isnull=False, longitud__isnull=False)
    )
    if q_ciclo:
        qs = qs.filter(ciclo=q_ciclo)
        
    ciclos = SPCicloRuta.objects.filter(empresa=empresa).values_list('ciclo', flat=True).distinct()
    
    abonados_geo = []
    for a in qs:
        if a.latitud is None or a.longitud is None:
            continue
        abonados_geo.append(
            {
                "id": a.pk,
                "codigo_abonado": a.codigo_abonado,
                "nombre": a.nombre,
                "estado": a.estado,
                "estado_label": a.get_estado_display(),
                "barrio": a.barrio or "N/A",
                "lat": round(float(a.latitud), 7),
                "lon": round(float(a.longitud), 7),
            }
        )

    return render(request, 'servicios_publicos/catastro/mapa.html', {
        'abonados': abonados_geo,
        'empresa': empresa, 
        'ciclos': ciclos, 
        'q_ciclo': q_ciclo,
        'nav_mapa': 'active',
        'titulo': 'Mapa Catastral'
    })


def catastro_detalle(request, pk):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    abonado = get_object_or_404(SPCatastroUsuario, pk=pk, empresa=empresa)
    medidores = abonado.medidores.all().order_by('-fecha_instalacion')
    ultimas_lecturas = abonado.lecturas.all().order_by('-periodo_ano', '-periodo_mes')[:12]
    facturas = abonado.facturas.all().order_by('-periodo_ano', '-periodo_mes')[:12]
    ordenes  = abonado.ordenes_trabajo.all().order_by('-fecha_emision')[:8]
    saldo_pendiente = abonado.facturas.filter(estado__in=['E','V','PP']).aggregate(s=Sum('saldo_pendiente'))['s'] or Decimal('0')
    
    return render(request, 'servicios_publicos/catastro/detalle.html', {
        'abonado': abonado, 'empresa': empresa,
        'medidores': medidores, 'ultimas_lecturas': ultimas_lecturas,
        'facturas': facturas, 'ordenes': ordenes,
        'saldo_pendiente': saldo_pendiente,
    })


def catastro_eliminar(request, pk):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    abonado = get_object_or_404(SPCatastroUsuario, pk=pk, empresa=empresa)
    if request.method == 'POST':
        codigo = abonado.codigo_abonado
        abonado.delete()
        messages.success(request, f'Abonado {codigo} eliminado.')
    return redirect('servicios_publicos:catastro_lista')


# ═══════════════════════════════════════════════════════════
# MEDIDORES
# ═══════════════════════════════════════════════════════════
def medidores_lista(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    q = request.GET.get('q', '').strip()
    qs = SPMedidor.objects.filter(empresa=empresa).select_related('abonado')
    if q:
        qs = qs.filter(Q(numero_serie__icontains=q) | Q(abonado__nombre__icontains=q) | Q(abonado__codigo_abonado__icontains=q))
    return render(request, 'servicios_publicos/medidores/lista.html', {
        'medidores': qs.order_by('-fecha_instalacion'), 'empresa': empresa, 'q': q,
    })


def medidor_form(request, pk=None):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    instance = get_object_or_404(SPMedidor, pk=pk, empresa=empresa) if pk else None
    abonados = SPCatastroUsuario.objects.filter(empresa=empresa, estado='A').order_by('nombre')
    
    if request.method == 'POST':
        try:
            abonado_id = request.POST.get('abonado')
            abonado = get_object_or_404(SPCatastroUsuario, pk=abonado_id, empresa=empresa)
            data = {
                'empresa': empresa,
                'abonado': abonado,
                'numero_serie': request.POST.get('numero_serie', '').strip(),
                'marca': request.POST.get('marca', '').strip() or None,
                'diametro': request.POST.get('diametro', '').strip() or None,
                'lectura_inicial': Decimal(request.POST.get('lectura_inicial', '0') or '0'),
                'fecha_instalacion': request.POST.get('fecha_instalacion') or None,
                'estado': request.POST.get('estado', 'A'),
                'observacion': request.POST.get('observacion', '').strip() or None,
                'usuario': request.session.get('usuario', ''),
            }
            if instance:
                for k, v in data.items(): setattr(instance, k, v)
                instance.save()
                messages.success(request, '✅ Medidor actualizado.')
            else:
                SPMedidor.objects.create(**data)
                messages.success(request, '✅ Medidor registrado.')
            return redirect('servicios_publicos:medidores_lista')
        except Exception as e:
            messages.error(request, f'❌ Error: {e}')
    
    return render(request, 'servicios_publicos/medidores/formulario.html', {
        'instance': instance, 'abonados': abonados, 'empresa': empresa,
        'titulo': 'Editar Medidor' if instance else 'Registrar Medidor',
        'ESTADO_CHOICES': SPMedidor.ESTADO_CHOICES,
    })


# ═══════════════════════════════════════════════════════════
# CICLOS Y RUTAS
# ═══════════════════════════════════════════════════════════
def ciclos_lista(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    ciclos = SPCicloRuta.objects.filter(empresa=empresa).order_by('ciclo', 'ruta')
    return render(request, 'servicios_publicos/ciclos/lista.html', {'ciclos': ciclos, 'empresa': empresa})


def ciclo_form(request, pk=None):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    instance = get_object_or_404(SPCicloRuta, pk=pk, empresa=empresa) if pk else None
    
    if request.method == 'POST':
        try:
            data = {
                'empresa': empresa,
                'ciclo': request.POST.get('ciclo', '').strip().upper(),
                'descripcion': request.POST.get('descripcion', '').strip(),
                'ruta': request.POST.get('ruta', '').strip() or None,
                'lecturador': request.POST.get('lecturador', '').strip() or None,
                'dia_lectura': int(request.POST.get('dia_lectura', '0') or '0') or None,
                'activo': request.POST.get('activo') == '1',
            }
            if instance:
                for k, v in data.items(): setattr(instance, k, v)
                instance.save()
                messages.success(request, '✅ Ciclo/Ruta actualizado.')
            else:
                SPCicloRuta.objects.create(**data)
                messages.success(request, '✅ Ciclo/Ruta creado.')
            return redirect('servicios_publicos:ciclos_lista')
        except Exception as e:
            messages.error(request, f'❌ Error: {e}')
    
    return render(request, 'servicios_publicos/ciclos/formulario.html', {
        'instance': instance, 'empresa': empresa,
        'titulo': 'Editar Ciclo/Ruta' if instance else 'Nuevo Ciclo/Ruta',
    })


# ═══════════════════════════════════════════════════════════
# LECTURAS DE MEDIDORES
# ═══════════════════════════════════════════════════════════
MESES_CHOICES = [
    (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
    (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
    (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
]

def lecturas_lista(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    hoy = date.today()
    q_ano = int(request.GET.get('ano', hoy.year))
    q_mes = int(request.GET.get('mes', hoy.month))
    q_ciclo = request.GET.get('ciclo', '')
    q_estado = request.GET.get('estado', '')
    
    qs = SPLectura.objects.filter(empresa=empresa, periodo_ano=q_ano, periodo_mes=q_mes).select_related('abonado', 'medidor')
    if q_ciclo:
        qs = qs.filter(abonado__ciclo=q_ciclo)
    if q_estado:
        qs = qs.filter(estado=q_estado)
    
    ciclos = SPCicloRuta.objects.filter(empresa=empresa, activo=True).values_list('ciclo', flat=True).distinct()
    
    return render(request, 'servicios_publicos/lecturas/lista.html', {
        'lecturas': qs.order_by('abonado__ruta', 'abonado__secuencia', 'abonado__nombre'),
        'empresa': empresa, 'q_ano': q_ano, 'q_mes': q_mes, 'q_ciclo': q_ciclo, 'q_estado': q_estado,
        'ciclos': ciclos, 'total': qs.count(),
        'ESTADO_CHOICES': SPLectura.ESTADO_CHOICES,
        'MESES': MESES_CHOICES,
    })


def lectura_form(request, pk=None):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    instance = get_object_or_404(SPLectura, pk=pk, empresa=empresa) if pk else None
    abonados = SPCatastroUsuario.objects.filter(empresa=empresa, estado='A').order_by('nombre')
    
    if request.method == 'POST':
        try:
            abonado_id = request.POST.get('abonado')
            abonado = get_object_or_404(SPCatastroUsuario, pk=abonado_id, empresa=empresa)
            medidor_activo = abonado.medidores.filter(estado='A').first()
            
            lectura_anterior = Decimal(request.POST.get('lectura_anterior', '0') or '0')
            lectura_actual   = Decimal(request.POST.get('lectura_actual', '0') or '0')
            consumo          = max(Decimal('0'), lectura_actual - lectura_anterior)
            
            data = {
                'empresa': empresa,
                'abonado': abonado,
                'medidor': medidor_activo,
                'periodo_ano': int(request.POST.get('periodo_ano', date.today().year)),
                'periodo_mes': int(request.POST.get('periodo_mes', date.today().month)),
                'lectura_anterior': lectura_anterior,
                'lectura_actual': lectura_actual,
                'consumo_m3': consumo,
                'es_estimado': request.POST.get('es_estimado') == '1',
                'fecha_lectura': request.POST.get('fecha_lectura') or date.today(),
                'lecturador': request.POST.get('lecturador', '').strip() or request.session.get('nombre', ''),
                'observacion': request.POST.get('observacion', '').strip() or None,
                'estado': 'V',  # Validada al ingresar manualmente
                'usuario': request.session.get('usuario', ''),
            }
            
            if instance:
                for k, v in data.items(): setattr(instance, k, v)
                # Manejar foto si se subió
                if request.FILES.get('foto_medidor'):
                    instance.foto_medidor = request.FILES['foto_medidor']
                instance.save()
                messages.success(request, '✅ Lectura actualizada.')
            else:
                new_lectura = SPLectura(**data)
                if request.FILES.get('foto_medidor'):
                    new_lectura.foto_medidor = request.FILES['foto_medidor']
                new_lectura.save()
                messages.success(request, f'✅ Lectura registrada. Consumo: {consumo:.2f} m³')
            return redirect('servicios_publicos:lecturas_lista')
        except Exception as e:
            messages.error(request, f'❌ Error: {e}')
            logger.exception(e)
    
    hoy = date.today()
    # Obtener última lectura del abonado si se sugiere
    abonado_sel = request.GET.get('abonado_id')
    lectura_anterior_sugerida = 0
    if abonado_sel:
        ultima = SPLectura.objects.filter(empresa=empresa, abonado_id=abonado_sel).order_by('-periodo_ano', '-periodo_mes').first()
        if ultima:
            lectura_anterior_sugerida = ultima.lectura_actual
    
    return render(request, 'servicios_publicos/lecturas/formulario.html', {
        'instance': instance, 'abonados': abonados, 'empresa': empresa,
        'titulo': 'Editar Lectura' if instance else 'Nueva Lectura',
        'ano_actual': hoy.year, 'mes_actual': hoy.month,
        'lectura_anterior_sugerida': lectura_anterior_sugerida,
        'MESES': MESES_CHOICES,
    })


def lecturas_cargar_ciclo(request):
    """Generar hoja de campo de lecturas para un ciclo/mes"""
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    hoy = date.today()
    
    ciclos  = SPCicloRuta.objects.filter(empresa=empresa, activo=True).order_by('ciclo', 'ruta')
    q_ciclo = request.GET.get('ciclo', '')
    q_ano   = int(request.GET.get('ano', hoy.year))
    q_mes   = int(request.GET.get('mes', hoy.month))
    
    abonados_ciclo = []
    if q_ciclo:
        abonados_en_ciclo = SPCatastroUsuario.objects.filter(
            empresa=empresa, ciclo=q_ciclo, estado='A'
        ).order_by('ruta', 'secuencia', 'nombre')
        
        for ab in abonados_en_ciclo:
            lectura_existente = SPLectura.objects.filter(
                empresa=empresa, abonado=ab, periodo_ano=q_ano, periodo_mes=q_mes
            ).first()
            ultima_lectura = SPLectura.objects.filter(
                empresa=empresa, abonado=ab
            ).exclude(periodo_ano=q_ano, periodo_mes=q_mes).order_by('-periodo_ano', '-periodo_mes').first()
            
            abonados_ciclo.append({
                'abonado': ab,
                'lectura_existente': lectura_existente,
                'ultima_lectura': ultima_lectura,
                'lectura_anterior': ultima_lectura.lectura_actual if ultima_lectura else 0,
                'medidor_activo': ab.medidores.filter(estado='A').first(),
            })
    
    return render(request, 'servicios_publicos/lecturas/cargar_ciclo.html', {
        'ciclos': ciclos, 'q_ciclo': q_ciclo, 'q_ano': q_ano, 'q_mes': q_mes,
        'abonados_ciclo': abonados_ciclo, 'empresa': empresa,
    })


# ═══════════════════════════════════════════════════════════
# FACTURACIÓN
# ═══════════════════════════════════════════════════════════
def _calcular_cargo_consumo(tarifa, consumo_m3):
    """Calcula el cargo por consumo según tarifa fija o tramos"""
    if tarifa.usa_tramos:
        tramos = tarifa.tramos.all().order_by('orden')
        cargo = Decimal('0')
        consumo_restante = consumo_m3
        for tramo in tramos:
            if consumo_restante <= 0:
                break
            desde = tramo.desde_m3
            hasta = tramo.hasta_m3
            if consumo_m3 <= desde:
                break
            fin_tramo = min(hasta if hasta else consumo_m3, consumo_m3)
            m3_en_tramo = fin_tramo - max(desde, 0)
            if m3_en_tramo > 0:
                cargo += m3_en_tramo * tramo.precio_m3
            if hasta and consumo_m3 <= hasta:
                break
        return cargo
    else:
        m3_cobrar = max(consumo_m3, tarifa.minimo_m3)
        return m3_cobrar * tarifa.precio_m3


def facturacion_lista(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    hoy = date.today()
    q_ano = int(request.GET.get('ano', hoy.year))
    q_mes = int(request.GET.get('mes', hoy.month))
    q_estado = request.GET.get('estado', '')
    q_ciclo  = request.GET.get('ciclo', '')
    
    qs = SPFactura.objects.filter(empresa=empresa, periodo_ano=q_ano, periodo_mes=q_mes).select_related('abonado')
    if q_estado:
        qs = qs.filter(estado=q_estado)
    if q_ciclo:
        qs = qs.filter(abonado__ciclo=q_ciclo)
    
    totales = qs.aggregate(
        suma_total=Sum('total'),
        suma_pendiente=Sum('saldo_pendiente'),
    )
    ciclos = SPCicloRuta.objects.filter(empresa=empresa, activo=True).values_list('ciclo', flat=True).distinct()
    
    return render(request, 'servicios_publicos/facturacion/lista.html', {
        'facturas': qs.order_by('abonado__ciclo', 'abonado__nombre'),
        'empresa': empresa, 'q_ano': q_ano, 'q_mes': q_mes, 'q_estado': q_estado, 'q_ciclo': q_ciclo,
        'totales': totales, 'ciclos': ciclos, 'total_registros': qs.count(),
        'ESTADO_CHOICES': SPFactura.ESTADO_CHOICES,
    })


def facturacion_generar(request):
    """Generar facturas para un ciclo/mes completo"""
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    hoy = date.today()
    rubros  = SPRubro.objects.filter(empresa=empresa, activo=True)
    ciclos  = SPCicloRuta.objects.filter(empresa=empresa, activo=True).values_list('ciclo', flat=True).distinct()
    
    if request.method == 'POST':
        try:
            ano   = int(request.POST.get('ano', hoy.year))
            mes   = int(request.POST.get('mes', hoy.month))
            ciclo = request.POST.get('ciclo', '').strip()
            rubro_codigo = request.POST.get('rubro', '').strip()
            
            # Obtener tarifa vigente
            tarifa = SPTarifa.objects.filter(empresa=empresa, rubro=rubro_codigo, ano=ano, activo=True).first()
            if not tarifa:
                # Intentar con el año anterior
                tarifa = SPTarifa.objects.filter(empresa=empresa, rubro=rubro_codigo, activo=True).order_by('-ano').first()
            if not tarifa:
                messages.error(request, f'❌ No hay tarifa configurada para el rubro {rubro_codigo}. Configure primero las tarifas.')
                return redirect('servicios_publicos:facturacion_generar')
            
            rubro_obj = SPRubro.objects.filter(empresa=empresa, codigo=rubro_codigo).first()
            
            # Abonados del ciclo
            qs_abonados = SPCatastroUsuario.objects.filter(empresa=empresa, estado='A')
            if ciclo:
                qs_abonados = qs_abonados.filter(ciclo=ciclo)
            
            creadas = 0
            omitidas = 0
            
            with transaction.atomic():
                for abonado in qs_abonados:
                    # Evitar duplicados
                    existe = SPFactura.objects.filter(
                        empresa=empresa, abonado=abonado,
                        periodo_ano=ano, periodo_mes=mes,
                    ).filter(detalles__rubro=rubro_codigo).exists()
                    if existe:
                        omitidas += 1
                        continue
                    
                    # Obtener lectura del período
                    lectura = SPLectura.objects.filter(
                        empresa=empresa, abonado=abonado,
                        periodo_ano=ano, periodo_mes=mes, estado__in=['V', 'F'],
                    ).first()
                    
                    consumo = lectura.consumo_m3 if lectura else Decimal('0')
                    
                    # Calcular montos
                    cargo_fijo    = tarifa.cargo_fijo
                    cargo_consumo = Decimal('0')
                    if rubro_obj and rubro_obj.tipo_cobro == 'M' and lectura:
                        cargo_consumo = _calcular_cargo_consumo(tarifa, consumo)
                    
                    subtotal = cargo_fijo + cargo_consumo
                    total    = subtotal
                    
                    # Número de factura
                    num_factura = SPConsecutivo.siguiente_factura(empresa)
                    
                    # Calcular vencimiento (15 días después)
                    from datetime import timedelta
                    import calendar
                    _, ultimo_dia = calendar.monthrange(ano, mes)
                    fecha_venc = date(ano, mes, ultimo_dia)
                    
                    factura = SPFactura.objects.create(
                        empresa=empresa,
                        numero_factura=num_factura,
                        abonado=abonado,
                        periodo_ano=ano,
                        periodo_mes=mes,
                        ciclo=ciclo or abonado.ciclo or '',
                        fecha_emision=hoy,
                        fecha_vencimiento=fecha_venc,
                        lectura=lectura,
                        subtotal=subtotal,
                        total=total,
                        saldo_pendiente=total,
                        estado='E',
                        usuario=request.session.get('usuario', ''),
                    )
                    
                    SPDetalleFactura.objects.create(
                        factura=factura,
                        rubro=rubro_codigo,
                        descripcion=rubro_obj.descripcion if rubro_obj else rubro_codigo,
                        consumo_m3=consumo,
                        cargo_fijo=cargo_fijo,
                        cargo_consumo=cargo_consumo,
                        subtotal=subtotal,
                    )
                    
                    # Marcar lectura como facturada
                    if lectura:
                        lectura.estado = 'F'
                        lectura.save()
                    
                    creadas += 1
            
            messages.success(request, f'✅ Se generaron {creadas} facturas. ({omitidas} ya existían).')
            return redirect('servicios_publicos:facturacion_lista')
        except Exception as e:
            messages.error(request, f'❌ Error al generar facturas: {e}')
            logger.exception(e)
    
    return render(request, 'servicios_publicos/facturacion/generar.html', {
        'empresa': empresa, 'rubros': rubros, 'ciclos': ciclos,
        'ano_actual': hoy.year, 'mes_actual': hoy.month,
    })


def factura_detalle(request, pk):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    factura = get_object_or_404(SPFactura, pk=pk, empresa=empresa)
    detalles = factura.detalles.all()
    return render(request, 'servicios_publicos/facturacion/detalle.html', {
        'factura': factura, 'detalles': detalles, 'empresa': empresa,
    })


def factura_anular(request, pk):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    factura = get_object_or_404(SPFactura, pk=pk, empresa=empresa)
    if request.method == 'POST' and factura.estado not in ['P', 'A']:
        factura.estado = 'A'
        factura.save()
        messages.success(request, f'Factura #{factura.numero_factura} anulada.')
    return redirect('servicios_publicos:factura_detalle', pk=pk)


def estado_cuenta_abonado(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    q = request.GET.get('q', '').strip()
    abonado = None
    facturas_pendientes = []
    total_pendiente = Decimal('0')
    
    if q:
        abonado = SPCatastroUsuario.objects.filter(
            empresa=empresa
        ).filter(
            Q(codigo_abonado__icontains=q) | Q(nombre__icontains=q) | Q(identidad__icontains=q)
        ).first()
        
        if abonado:
            facturas_pendientes = SPFactura.objects.filter(
                empresa=empresa, abonado=abonado, estado__in=['E', 'V', 'PP']
            ).order_by('periodo_ano', 'periodo_mes')
            total_pendiente = facturas_pendientes.aggregate(s=Sum('saldo_pendiente'))['s'] or Decimal('0')
    
    return render(request, 'servicios_publicos/facturacion/estado_cuenta.html', {
        'abonado': abonado, 'facturas_pendientes': facturas_pendientes,
        'total_pendiente': total_pendiente, 'q': q, 'empresa': empresa,
    })


# ═══════════════════════════════════════════════════════════
# ÓRDENES DE TRABAJO
# ═══════════════════════════════════════════════════════════
def ordenes_lista(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    q_estado = request.GET.get('estado', '')
    q_tipo   = request.GET.get('tipo', '')
    q_texto  = request.GET.get('q', '').strip()
    
    qs = SPOrdenTrabajo.objects.filter(empresa=empresa).select_related('abonado')
    if q_estado: qs = qs.filter(estado=q_estado)
    if q_tipo:   qs = qs.filter(tipo=q_tipo)
    if q_texto:  qs = qs.filter(Q(descripcion__icontains=q_texto) | Q(abonado__nombre__icontains=q_texto))
    
    return render(request, 'servicios_publicos/ordenes/lista.html', {
        'ordenes': qs.order_by('-fecha_emision'), 'empresa': empresa,
        'q_estado': q_estado, 'q_tipo': q_tipo, 'q_texto': q_texto,
        'TIPO_CHOICES': SPOrdenTrabajo.TIPO_CHOICES,
        'ESTADO_CHOICES': SPOrdenTrabajo.ESTADO_CHOICES,
        'total': qs.count(),
    })


def orden_form(request, pk=None):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    instance = get_object_or_404(SPOrdenTrabajo, pk=pk, empresa=empresa) if pk else None
    abonados = SPCatastroUsuario.objects.filter(empresa=empresa).order_by('nombre')
    conceptos = SPConceptoOT.objects.filter(empresa=empresa, activo=True).order_by("codigo")
    responsables = SPResponsable.objects.filter(empresa=empresa, activo=True).order_by("codigo")
    
    if request.method == 'POST':
        try:
            abonado_id = request.POST.get('abonado') or None
            abonado = SPCatastroUsuario.objects.filter(pk=abonado_id, empresa=empresa).first() if abonado_id else None
            concepto_id = request.POST.get("concepto") or None
            concepto = SPConceptoOT.objects.filter(pk=concepto_id, empresa=empresa).first() if concepto_id else None
            data = {
                'empresa': empresa,
                'abonado': abonado,
                'concepto': concepto,
                'tipo': request.POST.get('tipo', 'IN'),
                'descripcion': request.POST.get('descripcion', '').strip(),
                'prioridad': request.POST.get('prioridad', 'M'),
                'tecnico_asignado': request.POST.get('tecnico_asignado', '').strip() or None,
                'responsable_asignado': None,
                'fecha_programada': request.POST.get('fecha_programada') or None,
                'observacion': request.POST.get('observacion', '').strip() or None,
                'usuario': request.session.get('usuario', ''),
            }

            # Asignación por código de responsable (catálogo)
            codigo_asig = (request.POST.get("responsable_asignado_codigo") or "").strip()
            if codigo_asig:
                resp_asig = SPResponsable.objects.filter(empresa=empresa, codigo=codigo_asig, activo=True).first()
                if not resp_asig:
                    raise ValueError(f"No existe responsable activo con código '{codigo_asig}'")
                data["responsable_asignado"] = resp_asig
            if instance:
                for k, v in data.items(): setattr(instance, k, v)
                instance.save()
                messages.success(request, '✅ Orden de trabajo actualizada.')
            else:
                num_ot = SPConsecutivo.siguiente_ot(empresa)
                data['numero_ot'] = num_ot
                data['estado'] = 'P'
                SPOrdenTrabajo.objects.create(**data)
                messages.success(request, f'✅ Orden de trabajo #{num_ot} creada.')
            return redirect('servicios_publicos:ordenes_lista')
        except Exception as e:
            messages.error(request, f'❌ Error: {e}')
    
    return render(request, 'servicios_publicos/ordenes/formulario.html', {
        'instance': instance, 'abonados': abonados, 'empresa': empresa,
        'titulo': 'Editar OT' if instance else 'Nueva Orden de Trabajo',
        'TIPO_CHOICES': SPOrdenTrabajo.TIPO_CHOICES,
        'PRIORIDAD_CHOICES': SPOrdenTrabajo.PRIORIDAD_CHOICES,
        'conceptos': conceptos,
        'responsables': responsables,
    })


def orden_detalle(request, pk):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    orden = get_object_or_404(SPOrdenTrabajo, pk=pk, empresa=empresa)
    insumos = orden.insumos.all()
    total_insumos = insumos.aggregate(s=Sum('subtotal'))['s'] or Decimal('0')
    return render(request, 'servicios_publicos/ordenes/detalle.html', {
        'orden': orden, 'insumos': insumos, 'total_insumos': total_insumos, 'empresa': empresa,
    })


def orden_cerrar(request, pk):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    orden = get_object_or_404(SPOrdenTrabajo, pk=pk, empresa=empresa)
    if request.method == 'POST':
        codigo_resp = (request.POST.get("responsable_codigo") or "").strip()
        if not codigo_resp:
            messages.error(request, "Debe ingresar el código del responsable (fontanero) para cerrar la orden.")
            return redirect('servicios_publicos:orden_detalle', pk=pk)

        resp = SPResponsable.objects.filter(empresa=empresa, codigo=codigo_resp, activo=True).first()
        if not resp:
            messages.error(request, f"No existe un responsable activo con código '{codigo_resp}'. Regístrelo en Fontaneros/Responsables.")
            return redirect('servicios_publicos:orden_detalle', pk=pk)

        orden.estado = 'C'
        orden.fecha_cierre = date.today()
        orden.resultado = request.POST.get('resultado', '').strip()
        costo = Decimal(request.POST.get('costo_total', '0') or '0')
        orden.costo_total = costo
        orden.responsable_cierre = resp
        orden.save()
        messages.success(request, f'✅ Orden #{orden.numero_ot} cerrada exitosamente.')
    return redirect('servicios_publicos:orden_detalle', pk=pk)


# ═══════════════════════════════════════════════════════════
# CORTES Y RECONEXIONES
# ═══════════════════════════════════════════════════════════
def cortes_lista(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    qs = SPCorteSuspension.objects.filter(empresa=empresa).select_related('abonado').order_by('-fecha')[:100]
    return render(request, 'servicios_publicos/cortes/lista.html', {'cortes': qs, 'empresa': empresa})


def corte_form(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    abonados = SPCatastroUsuario.objects.filter(empresa=empresa, estado__in=['A', 'M']).order_by('nombre')
    
    if request.method == 'POST':
        try:
            abonado = get_object_or_404(SPCatastroUsuario, pk=request.POST.get('abonado'), empresa=empresa)
            tipo = request.POST.get('tipo', 'C')
            
            SPCorteSuspension.objects.create(
                empresa=empresa, abonado=abonado, tipo=tipo,
                fecha=date.today(),
                monto_adeudado=Decimal(request.POST.get('monto_adeudado', '0') or '0'),
                observacion=request.POST.get('observacion', '').strip() or None,
                usuario=request.session.get('usuario', ''),
            )
            # Actualizar estado del abonado
            if tipo in ['C', 'CS']:
                abonado.estado = 'S'
            elif tipo in ['R', 'RS']:
                abonado.estado = 'A'
            abonado.save()
            messages.success(request, f'✅ {dict(SPCorteSuspension.TIPO_CHOICES).get(tipo, tipo)} registrado para {abonado.nombre}.')
            return redirect('servicios_publicos:cortes_lista')
        except Exception as e:
            messages.error(request, f'❌ Error: {e}')
    
    return render(request, 'servicios_publicos/cortes/formulario.html', {
        'abonados': abonados, 'empresa': empresa,
        'TIPO_CHOICES': SPCorteSuspension.TIPO_CHOICES,
    })


# ═══════════════════════════════════════════════════════════
# REPORTES
# ═══════════════════════════════════════════════════════════
def reportes_dashboard(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    return render(request, 'servicios_publicos/reportes/dashboard.html', {'empresa': empresa})

def reporte_reclamos_por_concepto(request):
    redir = _requiere_sesion(request)
    if redir:
        return redir
    empresa = _get_empresa(request)

    conceptos = SPConceptoOT.objects.filter(empresa=empresa).order_by("codigo")
    ordenes = SPOrdenTrabajo.objects.filter(empresa=empresa).select_related("concepto")

    # Resumen: completadas vs pendientes (todo lo que no sea 'C' cuenta pendiente)
    data = []
    for c in conceptos:
        total = ordenes.filter(concepto=c).count()
        atendidas = ordenes.filter(concepto=c, estado="C").count()
        pendientes = ordenes.filter(concepto=c).exclude(estado="C").count()
        data.append({"concepto": c, "total": total, "atendidas": atendidas, "pendientes": pendientes})

    # Sin clasificar
    total_sc = ordenes.filter(concepto__isnull=True).count()
    atendidas_sc = ordenes.filter(concepto__isnull=True, estado="C").count()
    pendientes_sc = ordenes.filter(concepto__isnull=True).exclude(estado="C").count()

    return render(
        request,
        "servicios_publicos/reportes/reclamos_concepto.html",
        {
            "empresa": empresa,
            "data": data,
            "sin_clasificar": {"total": total_sc, "atendidas": atendidas_sc, "pendientes": pendientes_sc},
        },
    )


# ═══════════════════════════════════════════════════════════
# CATÁLOGOS: RESPONSABLES (FONTANEROS) y CONCEPTOS DE OT
# ═══════════════════════════════════════════════════════════
def responsables_lista(request):
    redir = _requiere_sesion(request)
    if redir:
        return redir
    empresa = _get_empresa(request)
    qs = SPResponsable.objects.filter(empresa=empresa).order_by("codigo")
    return render(request, "servicios_publicos/responsables/lista.html", {"responsables": qs, "empresa": empresa})


def responsable_form(request, pk=None):
    redir = _requiere_sesion(request)
    if redir:
        return redir
    empresa = _get_empresa(request)
    instance = get_object_or_404(SPResponsable, pk=pk, empresa=empresa) if pk else None

    if request.method == "POST":
        codigo = (request.POST.get("codigo") or "").strip().upper()
        nombre = (request.POST.get("nombre") or "").strip()
        telefono = (request.POST.get("telefono") or "").strip() or None
        activo = request.POST.get("activo") == "1"
        observacion = (request.POST.get("observacion") or "").strip() or None

        if not codigo or not nombre:
            messages.error(request, "Código y nombre son obligatorios.")
        else:
            try:
                if instance:
                    instance.codigo = codigo
                    instance.nombre = nombre
                    instance.telefono = telefono
                    instance.activo = activo
                    instance.observacion = observacion
                    instance.usuario = request.session.get("usuario", "") or request.session.get("nombre", "")
                    instance.save()
                    messages.success(request, "✅ Responsable actualizado.")
                else:
                    SPResponsable.objects.create(
                        empresa=empresa,
                        codigo=codigo,
                        nombre=nombre,
                        telefono=telefono,
                        activo=activo,
                        observacion=observacion,
                        usuario=request.session.get("usuario", "") or request.session.get("nombre", ""),
                    )
                    messages.success(request, "✅ Responsable creado.")
                return redirect("servicios_publicos:responsables_lista")
            except Exception as e:
                messages.error(request, f"❌ Error: {e}")

    return render(
        request,
        "servicios_publicos/responsables/formulario.html",
        {"instance": instance, "empresa": empresa, "titulo": "Editar Responsable" if instance else "Nuevo Responsable"},
    )


def conceptos_ot_lista(request):
    redir = _requiere_sesion(request)
    if redir:
        return redir
    empresa = _get_empresa(request)
    qs = SPConceptoOT.objects.filter(empresa=empresa).order_by("codigo")
    return render(request, "servicios_publicos/conceptos_ot/lista.html", {"conceptos": qs, "empresa": empresa})


def concepto_ot_form(request, pk=None):
    redir = _requiere_sesion(request)
    if redir:
        return redir
    empresa = _get_empresa(request)
    instance = get_object_or_404(SPConceptoOT, pk=pk, empresa=empresa) if pk else None

    if request.method == "POST":
        codigo = (request.POST.get("codigo") or "").strip().upper()
        descripcion = (request.POST.get("descripcion") or "").strip()
        activo = request.POST.get("activo") == "1"

        if not codigo or not descripcion:
            messages.error(request, "Código y descripción son obligatorios.")
        else:
            try:
                if instance:
                    instance.codigo = codigo
                    instance.descripcion = descripcion
                    instance.activo = activo
                    instance.usuario = request.session.get("usuario", "") or request.session.get("nombre", "")
                    instance.save()
                    messages.success(request, "✅ Concepto actualizado.")
                else:
                    SPConceptoOT.objects.create(
                        empresa=empresa,
                        codigo=codigo,
                        descripcion=descripcion,
                        activo=activo,
                        usuario=request.session.get("usuario", "") or request.session.get("nombre", ""),
                    )
                    messages.success(request, "✅ Concepto creado.")
                return redirect("servicios_publicos:conceptos_ot_lista")
            except Exception as e:
                messages.error(request, f"❌ Error: {e}")

    return render(
        request,
        "servicios_publicos/conceptos_ot/formulario.html",
        {"instance": instance, "empresa": empresa, "titulo": "Editar Concepto" if instance else "Nuevo Concepto"},
    )


def reporte_morosos(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    morosos = SPCatastroUsuario.objects.filter(empresa=empresa).annotate(
        deuda=Sum('facturas__saldo_pendiente', filter=Q(facturas__estado__in=['E','V','PP']))
    ).filter(deuda__gt=0).order_by('-deuda')
    return render(request, 'servicios_publicos/reportes/morosos.html', {
        'morosos': morosos, 'empresa': empresa,
        'total_mora': morosos.aggregate(t=Sum('deuda'))['t'] or Decimal('0'),
    })


def reporte_consumos(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    hoy = date.today()
    q_ano = int(request.GET.get('ano', hoy.year))
    q_mes = int(request.GET.get('mes', hoy.month))
    lecturas = SPLectura.objects.filter(empresa=empresa, periodo_ano=q_ano, periodo_mes=q_mes).select_related('abonado').order_by('-consumo_m3')
    total_m3 = lecturas.aggregate(s=Sum('consumo_m3'))['s'] or Decimal('0')
    return render(request, 'servicios_publicos/reportes/consumos.html', {
        'lecturas': lecturas, 'empresa': empresa, 'q_ano': q_ano, 'q_mes': q_mes, 'total_m3': total_m3,
    })


def reporte_facturacion_ciclo(request):
    redir = _requiere_sesion(request)
    if redir: return redir
    empresa = _get_empresa(request)
    hoy = date.today()
    q_ano   = int(request.GET.get('ano', hoy.year))
    q_mes   = int(request.GET.get('mes', hoy.month))
    q_ciclo = request.GET.get('ciclo', '')
    qs = SPFactura.objects.filter(empresa=empresa, periodo_ano=q_ano, periodo_mes=q_mes)
    if q_ciclo:
        qs = qs.filter(abonado__ciclo=q_ciclo)
    resumen = qs.aggregate(
        total_facturas=Count('id'),
        total_monto=Sum('total'),
        total_pendiente=Sum('saldo_pendiente'),
        pagadas=Count('id', filter=Q(estado='P')),
    )
    ciclos = SPCicloRuta.objects.filter(empresa=empresa, activo=True).values_list('ciclo', flat=True).distinct()
    return render(request, 'servicios_publicos/reportes/facturacion_ciclo.html', {
        'facturas': qs.select_related('abonado').order_by('abonado__ciclo', 'abonado__nombre'),
        'resumen': resumen, 'empresa': empresa, 'q_ano': q_ano, 'q_mes': q_mes, 'q_ciclo': q_ciclo,
        'ciclos': ciclos,
    })


# ═══════════════════════════════════════════════════════════
# AJAX
# ═══════════════════════════════════════════════════════════
def ajax_buscar_abonado(request):
    empresa = _get_empresa(request)
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'results': []})
    abonados = SPCatastroUsuario.objects.filter(
        empresa=empresa
    ).filter(
        Q(nombre__icontains=q) | Q(codigo_abonado__icontains=q) | Q(identidad__icontains=q)
    )[:15]
    results = [{'id': a.pk, 'text': f'{a.codigo_abonado} - {a.nombre}', 'estado': a.estado} for a in abonados]
    return JsonResponse({'results': results})


def ajax_calcular_factura(request):
    """Calcula el monto de una factura para un abonado/rubro/consumo dado"""
    empresa = _get_empresa(request)
    rubro_codigo = request.GET.get('rubro', '')
    consumo = Decimal(request.GET.get('consumo', '0') or '0')
    ano = int(request.GET.get('ano', date.today().year))
    
    tarifa = SPTarifa.objects.filter(empresa=empresa, rubro=rubro_codigo, ano=ano, activo=True).first()
    if not tarifa:
        tarifa = SPTarifa.objects.filter(empresa=empresa, rubro=rubro_codigo, activo=True).order_by('-ano').first()
    
    if not tarifa:
        return JsonResponse({'error': 'No hay tarifa configurada para este rubro.'})
    
    cargo_fijo    = float(tarifa.cargo_fijo)
    cargo_consumo = float(_calcular_cargo_consumo(tarifa, consumo))
    total = cargo_fijo + cargo_consumo
    
    return JsonResponse({
        'cargo_fijo': cargo_fijo,
        'cargo_consumo': cargo_consumo,
        'total': total,
        'tarifa_id': tarifa.pk,
        'usa_tramos': tarifa.usa_tramos,
    })


@csrf_exempt
def ajax_guardar_tramo(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    empresa = _get_empresa(request)
    try:
        data = json.loads(request.body)
        tarifa_id = data.get('tarifa_id')
        tarifa = get_object_or_404(SPTarifa, pk=tarifa_id, empresa=empresa)
        tramo = SPTramoTarifa.objects.create(
            tarifa=tarifa,
            desde_m3=Decimal(str(data.get('desde_m3', 0))),
            hasta_m3=Decimal(str(data['hasta_m3'])) if data.get('hasta_m3') else None,
            precio_m3=Decimal(str(data.get('precio_m3', 0))),
            orden=tarifa.tramos.count() + 1,
        )
        return JsonResponse({'ok': True, 'id': tramo.pk})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def ajax_eliminar_tramo(request, pk):
    if request.method == 'POST':
        empresa = _get_empresa(request)
        tramo = get_object_or_404(SPTramoTarifa, pk=pk, tarifa__empresa=empresa)
        tramo.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
@require_POST
def facturacion_enviar_a_caja(request):
    """Vista AJAX para enviar facturas de SP a caja"""
    try:
        empresa = _get_empresa(request)
        usuario = request.session.get('usuario', 'SISTEMA')
        
        data = json.loads(request.body)
        factura_ids = data.get('factura_ids', [])
        identidad_pago = data.get('identidad_pago', '').strip()
        nombre_pago = data.get('nombre_pago', '').strip()
        comentario_pago = data.get('comentario', '').strip()
        
        if not factura_ids:
            return JsonResponse({'ok': False, 'error': 'No se seleccionaron facturas'})

        # Obtener facturas ordenadas por fecha para validar FIFO
        facturas = SPFactura.objects.filter(
            id__in=factura_ids, 
            empresa=empresa, 
            estado__in=['E', 'V']
        ).select_related('abonado').order_by('periodo_ano', 'periodo_mes')

        if not facturas.exists():
            return JsonResponse({'ok': False, 'error': 'No se encontraron facturas pendientes válidas'})

        abonado = facturas[0].abonado
        
        # Validar FIFO: No puede pagar factura actual si debe meses anteriores (fuera de la selección)
        # 1. Encontrar la fecha más antigua de la selección
        f_min = facturas[0]
        # 2. Buscar si hay facturas pendientes más antiguas que no están en la selección
        pendientes_anteriores = SPFactura.objects.filter(
            abonado=abonado,
            empresa=empresa,
            estado__in=['E', 'V']
        ).exclude(id__in=factura_ids).filter(
            Q(periodo_ano__lt=f_min.periodo_ano) | 
            Q(periodo_ano=f_min.periodo_ano, periodo_mes__lt=f_min.periodo_mes)
        )

        if pendientes_anteriores.exists():
            faltante = pendientes_anteriores.order_by('periodo_ano', 'periodo_mes').first()
            return JsonResponse({
                'ok': False, 
                'error': f'Regla FIFO: Debe incluir la factura pendiende del periodo {faltante.periodo_mes:02d}/{faltante.periodo_ano} antes de pagar periodos posteriores.'
            })

        # Generar número de recibo usando la secuencia oficial
        numero_recibo = NoRecibos.obtener_siguiente_numero_por_empresa(empresa)
        numero_recibo_decimal = Decimal(str(numero_recibo))
        
        ahora = timezone.now()
        current_year = ahora.year
        
        # Cache de rubros tributarios para códigos contables
        rubros_t = TributarioRubro.objects.filter(empresa=empresa)
        rubros_cache = {r.codigo: r for r in rubros_t}
        
        registros_caja = []
        with transaction.atomic():
            for f in facturas:
                detalles = f.detalles.all()
                for d in detalles:
                    # Determinar código contable (Corriente vs Rezago)
                    r_obj = rubros_cache.get(d.rubro)
                    if int(f.periodo_ano) == current_year:
                        codigo_contable = r_obj.cuenta if r_obj else d.rubro
                    else:
                        codigo_contable = r_obj.cuentarez if r_obj else d.rubro
                    
                    # Descripción para caja
                    desc = f"AGUA POTABLE {f.periodo_mes:02d}/{f.periodo_ano}"
                    if d.rubro != 'T0001':
                        desc += f" - {d.descripcion}"

                    pago_temp = PagoVariosTemp(
                        empresa=empresa,
                        recibo=numero_recibo_decimal,
                        rubro=d.rubro,
                        codigo=str(codigo_contable)[:16],
                        fecha=ahora.date(),
                        identidad=identidad_pago or abonado.identidad or '',
                        nombre=nombre_pago or abonado.nombre,
                        descripcion=desc,
                        valor=d.subtotal,
                        comentario=comentario_pago or f"Abonado: {abonado.codigo_abonado}",
                        oficina='001',
                        facturadora='SERVICIOS PUBLICOS',
                        aplicado='0',
                        traslado='0',
                        cantidad=Decimal('1.00'),
                        vl_unit=d.subtotal,
                        cajero=usuario,
                        usuario=usuario,
                        Rtm=abonado.codigo_abonado, # Usamos código de abonado como referencia RTM
                        Rfechapag=ahora.date(),
                    )
                    registros_caja.append(pago_temp)
                
                # Si la factura tiene mora, agregar el rubro de mora (usualmente T0002 o configurable)
                if f.mora > 0:
                    r_mora = rubros_cache.get('T0002') # Asumimos T0002 para mora
                    c_mora = r_mora.cuenta if r_mora else 'T0002'
                    registros_caja.append(PagoVariosTemp(
                        empresa=empresa,
                        recibo=numero_recibo_decimal,
                        rubro='T0002',
                        codigo=str(c_mora)[:16],
                        fecha=ahora.date(),
                        identidad=identidad_pago or abonado.identidad or '',
                        nombre=nombre_pago or abonado.nombre,
                        descripcion=f"MORA AGUA {f.periodo_mes:02d}/{f.periodo_ano}",
                        valor=f.mora,
                        comentario=f"Abonado: {abonado.codigo_abonado}",
                        oficina='001',
                        facturadora='SERVICIOS PUBLICOS',
                        aplicado='0',
                        traslado='0',
                        cantidad=Decimal('1.00'),
                        vl_unit=f.mora,
                        cajero=usuario,
                        usuario=usuario,
                        Rtm=abonado.codigo_abonado,
                    ))
                
                # Actualizar estado de la factura (E = Emitida, V = Vencida, C = En Caja)
                # Opcional: Podríamos dejarla como E/V hasta que caja confirme, 
                # pero marcarla ayuda a evitar duplicados en caja.
                # f.estado = 'C' 
                # f.save()

            PagoVariosTemp.objects.bulk_create(registros_caja)

        return JsonResponse({
            'ok': True, 
            'recibo': numero_recibo,
            'mensaje': f'Se han enviado {len(facturas)} facturas a caja exitosamente.'
        })

    except Exception as e:
        logger.error(f"Error al enviar a caja: {str(e)}")
        return JsonResponse({'ok': False, 'error': f'Error interno: {str(e)}'})
