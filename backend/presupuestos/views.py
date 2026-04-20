from decimal import Decimal
import json
from datetime import date
from django.db.models import Sum, Q

from django.contrib import messages
from django.db import OperationalError, ProgrammingError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CuentaPresupuestariaForm,
    FondoForm,
    OrdenPagoForm,
    ProyectoInversionForm,
    PresupuestoAnualForm,
    AmpliacionPresupuestariaForm,
    ReduccionPresupuestariaForm,
    TraspasoPresupuestariaForm,
    CompromisoForm,
    OperacionManualForm,
)
from .models import (
    CuentaPresupuestaria,
    Fondo,
    OrdenPago,
    OrdenPagoDetalle,
    ProyectoInversion,
    PresupuestoAnual,
    ReformaPresupuestaria,
    EjecucionPresupuestaria,
    Compromiso,
    OperacionManual,
)
from .rendicion_services import calcular_ejecucion_presupuestaria
from contabilidad.models import EjercicioFiscal, CentroCosto, CuentaContable
from core.models import Municipio


def verificar_sesion(request):
    return request.session.get("user_id") is not None


def get_empresa(request):
    return request.session.get("empresa", "")


def get_empresa_label(request):
    """
    Devuelve etiqueta legible: 'Municipio (0301)'.
    Si no existe el catálogo, cae a solo código.
    """
    codigo = (get_empresa(request) or "").strip()
    if not codigo:
        return ""
    try:
        m = Municipio.objects.filter(codigo=codigo).first()
        if m and m.descripcion:
            return f"{m.descripcion.strip()} ({codigo})"
    except Exception:
        pass
    return codigo


def presupuestos_login(request):
    if verificar_sesion(request):
        return redirect("presupuestos:presupuestos_menu_principal")
    return redirect("modules_core:login_principal")


def presupuestos_logout(request):
    messages.success(request, "Sesión cerrada correctamente")
    return redirect("modules_core:menu_principal")


def presupuestos_menu_principal(request):
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    empresa_label = get_empresa_label(request)
    try:
        tot_fondos = Fondo.objects.filter(empresa=empresa, is_active=True).count()
        tot_ingresos = CuentaPresupuestaria.objects.filter(empresa=empresa, tipo_presupuesto="INGRESO", is_active=True).count()
        tot_egresos = CuentaPresupuestaria.objects.filter(empresa=empresa, tipo_presupuesto="EGRESO", is_active=True).count()
        tot_op = OrdenPago.objects.filter(empresa=empresa, is_active=True).count()
        migracion_pendiente = False
    except (ProgrammingError, OperationalError):
        tot_fondos = 0
        tot_ingresos = 0
        tot_egresos = 0
        tot_op = 0
        migracion_pendiente = True

    context = {
        "modulo": "Presupuestos",
        "descripcion": "Planificación y control presupuestario",
        "usuario": request.session.get("nombre", ""),
        "empresa": empresa,
        "empresa_label": empresa_label,
        "tot_fondos": tot_fondos,
        "tot_ingresos": tot_ingresos,
        "tot_egresos": tot_egresos,
        "tot_op": tot_op,
        "migracion_pendiente": migracion_pendiente,
    }
    return render(request, "presupuestos/menu_principal.html", context)


def fondos(request):
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    if request.method == "POST":
        form = FondoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.empresa = empresa
            obj.save()
            messages.success(request, "Fondo guardado correctamente.")
            return redirect("presupuestos:fondos")
    else:
        form = FondoForm(initial={"empresa": empresa})

    return render(
        request,
        "presupuestos/fondos.html",
        {
            "form": form,
            "items": Fondo.objects.filter(empresa=empresa, is_active=True).order_by("codigo"),
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
        },
    )


def catalogo_presupuestario(request, tipo):
    """Vista genérica para Ingresos o Egresos"""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    tipo_upper = tipo.upper() # 'INGRESO' o 'EGRESO'
    
    if request.method == "POST":
        accion = request.POST.get("accion", "guardar")
        if accion == "eliminar":
            cuenta_id = request.POST.get("cuenta_id")
            cuenta = CuentaPresupuestaria.objects.filter(
                id=cuenta_id,
                empresa=empresa,
                tipo_presupuesto=tipo_upper,
                is_active=True,
            ).first()
            if not cuenta:
                messages.error(request, "La cuenta no existe o ya fue eliminada.")
            else:
                cuenta.is_active = False
                cuenta.save(update_fields=["is_active"])
                messages.success(request, f"Cuenta {cuenta.codigo} eliminada correctamente.")
            return redirect(request.path)

        form = CuentaPresupuestariaForm(request.POST, empresa=empresa, tipo_presupuesto=tipo_upper)
        if form.is_valid():
            codigo = (form.cleaned_data.get("codigo") or "").strip()
            existente = CuentaPresupuestaria.objects.filter(
                empresa=empresa,
                tipo_presupuesto=tipo_upper,
                codigo=codigo,
            ).first()

            if existente:
                existente.nombre = form.cleaned_data.get("nombre")
                existente.tipo_cuenta = form.cleaned_data.get("tipo_cuenta")
                existente.cuenta_padre = form.cleaned_data.get("cuenta_padre")
                existente.nivel = form.cleaned_data.get("nivel")
                existente.rubro_tributario = form.cleaned_data.get("rubro_tributario")
                existente.cuenta_contable = form.cleaned_data.get("cuenta_contable")
                existente.is_active = True
                existente.save()
                messages.success(request, f"Cuenta {codigo} actualizada correctamente.")
            else:
                obj = form.save(commit=False)
                obj.empresa = empresa
                obj.tipo_presupuesto = tipo_upper
                obj.save()
                messages.success(request, f"Cuenta de {tipo} guardada correctamente.")
            return redirect(request.path)
    else:
        form = CuentaPresupuestariaForm(empresa=empresa, tipo_presupuesto=tipo_upper, initial={"empresa": empresa, "tipo_presupuesto": tipo_upper})

    items = (
        CuentaPresupuestaria.objects.filter(empresa=empresa, tipo_presupuesto=tipo_upper, is_active=True)
        .select_related("cuenta_contable", "cuenta_padre")
        .order_by("codigo")
    )

    cuentas_lookup = {
        (i.codigo or "").strip().upper(): {
            "nombre": i.nombre or "",
            "tipo_cuenta": i.tipo_cuenta or "",
            "nivel": i.nivel or "",
            "cuenta_padre": i.cuenta_padre_id or "",
            "cuenta_contable": i.cuenta_contable_id or "",
        }
        for i in items
    }

    return render(
        request,
        "presupuestos/cuentas_presupuestarias.html",
        {
            "form": form,
            "items": items,
            "tipo_url": tipo.lower(),
            "titulo": f"Presupuesto de {tipo.capitalize()}s",
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
            "cuentas_lookup_json": json.dumps(cuentas_lookup),
        },
    )


def presupuesto_anual(request):
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    # Este formulario queda exclusivo para Presupuesto Inicial de Ingresos.
    tipo_filtro = "INGRESO"
    
    if request.method == "POST":
        form = PresupuestoAnualForm(request.POST, empresa=empresa, tipo_presupuesto=tipo_filtro)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.empresa = empresa
            obj.save()
            messages.success(request, f"Monto presupuestado de {tipo_filtro} guardado.")
            return redirect(request.path)
    else:
        form = PresupuestoAnualForm(empresa=empresa, tipo_presupuesto=tipo_filtro, initial={"empresa": empresa})

    items = (
        PresupuestoAnual.objects.filter(empresa=empresa, cuenta__tipo_presupuesto=tipo_filtro, is_active=True)
        .select_related("ejercicio", "cuenta", "fondo")
        .order_by("-ejercicio__anio", "cuenta__codigo")
    )

    return render(
        request,
        "presupuestos/presupuesto_anual.html",
        {
            "form": form,
            "items": items,
            "titulo": f"Presupuesto Anual de {tipo_filtro}s",
            "tipo": tipo_filtro,
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
        },
    )


def reformas_listado(request):
    """Vista general para ver el historial de todas las reformas filtrado por tipo"""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    tipo_filtro = request.GET.get("tipo", "EGRESO")
    
    items = (
        ReformaPresupuestaria.objects.filter(
            empresa=empresa, 
            is_active=True,
            cuenta_destino__tipo_presupuesto=tipo_filtro
        )
        .select_related("ejercicio", "cuenta_origen", "cuenta_destino", "fondo")
        .order_by("-fecha", "-id")
    )

    return render(
        request,
        "presupuestos/reformas_listado.html",
        {
            "items": items,
            "titulo": f"Reformas de {tipo_filtro}s",
            "tipo": tipo_filtro,
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
        },
    )


def gestionar_reforma(request, tipo_reforma):
    """Vista genérica para gestionar Ampliaciones, Reducciones o Traspasos"""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    
    # Mapeo de tipos a formularios y títulos
    config = {
        'AMPLIACION': {'form': AmpliacionPresupuestariaForm, 'titulo': 'Ampliación Presupuestaria', 'clase': 'success'},
        'REDUCCION': {'form': ReduccionPresupuestariaForm, 'titulo': 'Reducción Presupuestaria', 'clase': 'danger'},
        'TRASPASO': {'form': TraspasoPresupuestariaForm, 'titulo': 'Traspaso Presupuestario', 'clase': 'warning'},
    }
    
    conf = config.get(tipo_reforma)
    if not conf:
        return redirect("presupuestos:reformas_listado")

    if request.method == "POST":
        form = conf['form'](request.POST, empresa=empresa)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.empresa = empresa
            obj.tipo = tipo_reforma
            obj.save()
            messages.success(request, f"{conf['titulo']} aplicada exitosamente.")
            return redirect("presupuestos:reformas_listado")
    else:
        form = conf['form'](empresa=empresa, initial={"empresa": empresa})

    return render(
        request,
        "presupuestos/reforma_form.html",
        {
            "form": form,
            "titulo": conf['titulo'],
            "clase": conf['clase'],
            "tipo": tipo_reforma,
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
        },
    )


def proyectos_inversion(request):
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    if request.method == "POST":
        form = ProyectoInversionForm(request.POST, empresa=empresa)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.empresa = empresa
            obj.save()
            messages.success(request, "Proyecto de inversión guardado.")
            return redirect("presupuestos:proyectos_inversion")
    else:
        form = ProyectoInversionForm(empresa=empresa, initial={"empresa": empresa})

    return render(
        request,
        "presupuestos/proyectos_inversion.html",
        {
            "form": form,
            "items": ProyectoInversion.objects.filter(empresa=empresa, is_active=True).select_related("ejercicio", "centro_costo").order_by("codigo"),
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
        },
    )


def ordenes_pago(request):
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    # Solo cuentas de EGRESO y tipo DETALLE para las órdenes de pago
    cuentas = CuentaPresupuestaria.objects.filter(
        empresa=empresa, is_active=True, tipo_presupuesto="EGRESO", tipo_cuenta="DETALLE"
    ).order_by("codigo")
    
    fondos_qs = Fondo.objects.filter(empresa=empresa, is_active=True).order_by("codigo")
    proyectos = ProyectoInversion.objects.filter(empresa=empresa, is_active=True).order_by("codigo")

    if request.method == "POST":
        form = OrdenPagoForm(request.POST, empresa=empresa)
        if form.is_valid():
            op = form.save(commit=False)
            op.empresa = empresa
            op.save()

            lineas_cuenta = request.POST.getlist("linea_cuenta")
            lineas_fondo = request.POST.getlist("linea_fondo")
            lineas_proyecto = request.POST.getlist("linea_proyecto")
            lineas_desc = request.POST.getlist("linea_desc")
            lineas_monto = request.POST.getlist("linea_monto")

            total = Decimal("0.00")
            linea_num = 1
            for idx, cuenta_id in enumerate(lineas_cuenta):
                if not cuenta_id:
                    continue
                monto_txt = (lineas_monto[idx] if idx < len(lineas_monto) else "0").strip() or "0"
                monto = Decimal(monto_txt)
                if monto <= 0:
                    continue

                fondo_id = lineas_fondo[idx] if idx < len(lineas_fondo) else ""
                proyecto_id = lineas_proyecto[idx] if idx < len(lineas_proyecto) else ""
                desc = lineas_desc[idx] if idx < len(lineas_desc) else ""

                OrdenPagoDetalle.objects.create(
                    orden_pago=op,
                    linea=linea_num,
                    cuenta_presupuestaria_id=cuenta_id,
                    fondo_id=fondo_id or None,
                    proyecto_id=proyecto_id or None,
                    descripcion=desc,
                    monto=monto,
                )
                total += monto
                linea_num += 1

            op.total = total
            op.save(update_fields=["total"])
            messages.success(request, f"Orden de pago {op.numero} guardada con {linea_num - 1} líneas.")
            return redirect("presupuestos:ordenes_pago")
    else:
        form = OrdenPagoForm(empresa=empresa, initial={"empresa": empresa})

    return render(
        request,
        "presupuestos/ordenes_pago.html",
        {
            "form": form,
            "cuentas": cuentas,
            "fondos": fondos_qs,
            "proyectos": proyectos,
            "items": OrdenPago.objects.filter(empresa=empresa, is_active=True).order_by("-fecha", "-numero")[:80],
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
        },
    )


def gestionar_compromisos(request):
    """Gestión de reservas de fondo (compromisos)."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    if request.method == "POST":
        form = CompromisoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.empresa = empresa
            obj.save()
            messages.success(request, "Reserva de fondo (Compromiso) registrada correctamente.")
            return redirect("presupuestos:gestionar_compromisos")
    else:
        form = CompromisoForm(initial={"empresa": empresa})

    items = Compromiso.objects.filter(empresa=empresa, is_active=True).order_by("-fecha", "-numero")
    return render(request, "presupuestos/compromisos.html", {
        "form": form,
        "items": items,
        "titulo": "Compromisos (Reserva de Fondo)",
        "empresa": empresa,
    })


def gestionar_operacion_manual(request):
    """Registro directo de operaciones (Ingresos o Egresos)."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    tipo_filtro = request.GET.get("tipo", "EGRESO")
    
    if request.method == "POST":
        form = OperacionManualForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.empresa = empresa
            obj.save()
            messages.success(request, f"{obj.get_tipo_display()} registrado correctamente.")
            return redirect(f"{request.path}?tipo={obj.tipo}")
    else:
        form = OperacionManualForm(initial={"empresa": empresa, "tipo": tipo_filtro})

    items = OperacionManual.objects.filter(empresa=empresa, tipo=tipo_filtro, is_active=True).order_by("-fecha", "-id")
    return render(request, "presupuestos/operaciones_manuales.html", {
        "form": form,
        "items": items,
        "titulo": f"Registro de {tipo_filtro}s Manuales",
        "tipo": tipo_filtro,
        "empresa": empresa,
    })


def informes_presupuestarios(request):
    """Vista de informes (ahora redirige al hub si es ingreso)."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    tipo = request.GET.get("tipo", "EGRESO")
    if tipo == "INGRESO":
        return redirect("presupuestos:informes_ingresos_hub")
        
    empresa = get_empresa(request)
    return render(request, "presupuestos/informes.html", {
        "titulo": "Informes Presupuestarios",
        "empresa": empresa,
    })

def informes_ingresos_hub(request):
    """Panel central de informes de ingresos."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    ejercicios = EjercicioFiscal.objects.all().order_by("-anio")
    
    # Valores por defecto para filtros
    ejercicio_actual = ejercicios.first()
    ejercicio_id = request.GET.get("ejercicio", str(ejercicio_actual.id if ejercicio_actual else ""))
    
    hoy = date.today()
    fecha_desde = request.GET.get("fecha_desde", f"{hoy.year}-01-01")
    fecha_hasta = request.GET.get("fecha_hasta", hoy.strftime("%Y-%m-%d"))

    context = {
        "ejercicios": ejercicios,
        "ejercicio_id": ejercicio_id,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
        "empresa": empresa,
        "usuario": request.session.get("nombre", ""),
    }
    return render(request, "presupuestos/informes_ingresos.html", context)

def _obtener_ejecucion_ingresos(empresa, ejercicio_id, fecha_desde=None, fecha_hasta=None, solo_nivel_2=False):
    """Helper para calcular ejecución jerárquica de ingresos (compatibilidad con plantillas existentes)."""
    raw = calcular_ejecucion_presupuestaria(
        empresa, ejercicio_id, "INGRESO", fecha_desde, fecha_hasta, solo_nivel_2
    )
    resultados = []
    for r in raw:
        resultados.append(
            {
                "codigo": r["codigo"],
                "nombre": r["nombre"],
                "nivel": r["nivel"],
                "tipo": r["tipo"],
                "aprobado": r["aprobado"],
                "reformas": r["reformas"],
                "total_aprobado": r["total_aprobado"],
                "recaudado": r["ejecutado"],
                "recaudado_periodo": r["ejecutado_periodo"],
                "por_recaudar": r["saldo_por_ejecutar"],
                "porcentaje": r["porcentaje"],
            }
        )
    return resultados

def reporte_ejecucion_general(request):
    """Informe Ejecución General del Presupuesto de Ingresos."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    ejercicio_id = request.GET.get("ejercicio")
    ejercicio = get_object_or_404(EjercicioFiscal, id=ejercicio_id) if ejercicio_id else None
    
    if not ejercicio:
        return redirect("presupuestos:informes_ingresos_hub")

    datos = _obtener_ejecucion_ingresos(empresa, ejercicio.id)
    
    return render(request, "presupuestos/reports/reporte_ejecucion_general.html", {
        "titulo": "Ejecución General del Presupuesto de Ingresos",
        "subtitulo": f"Periodo Fiscal {ejercicio.anio}",
        "empresa_nombre": empresa,
        "ejercicio": ejercicio,
        "datos": datos,
        "hoy": date.today(),
    })

def reporte_ejecucion_periodo(request):
    """Rentístico de ingresos del periodo (Rango de fechas)."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    ejercicio_id = request.GET.get("ejercicio")
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")
    
    ejercicio = get_object_or_404(EjercicioFiscal, id=ejercicio_id)
    datos = _obtener_ejecucion_ingresos(empresa, ejercicio.id, fecha_desde=desde, fecha_hasta=hasta)
    
    return render(request, "presupuestos/reports/reporte_ejecucion_general.html", {
        "titulo": "Ejecución de Ingresos por Periodo",
        "subtitulo": f"Del {desde} al {hasta} - Ejercicio {ejercicio.anio}",
        "empresa_nombre": empresa,
        "ejercicio": ejercicio,
        "datos": datos,
        "es_periodo": True,
        "hoy": date.today(),
    })

def reporte_mensual_ingresos(request):
    """Resumen de ingresos mensual (12 meses)."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    ejercicio_id = request.GET.get("ejercicio")
    ejercicio = get_object_or_404(EjercicioFiscal, id=ejercicio_id)
    
    cuentas = CuentaPresupuestaria.objects.filter(empresa=empresa, tipo_presupuesto="INGRESO", nivel__lte=2, is_active=True).order_by("codigo")
    
    # Obtener recaudación por mes
    # Esto requiere una agregación más compleja o múltiples queries.
    # Por simplicidad en este paso, usaremos agregación por mes.
    meses_nombres = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    
    resultado_final = []
    for c in cuentas:
        fila = {"codigo": c.codigo, "nombre": c.nombre, "nivel": c.nivel, "meses": []}
        total_anio = Decimal("0.00")
        
        # Para cada mes, calcular lo recaudado (incluyendo hijos si es TITULO)
        # Esto es pesado. Optimización: traer toda la ejecución y agrupar en Python.
        hijos_ids = CuentaPresupuestaria.objects.filter(empresa=empresa, codigo__startswith=c.codigo).values_list("id", flat=True)
        
        for mes in range(1, 13):
            monto = EjecucionPresupuestaria.objects.filter(
                empresa=empresa, 
                ejercicio=ejercicio, 
                cuenta_presupuestaria_id__in=hijos_ids,
                fecha__month=mes
            ).aggregate(total=Sum("monto"))["total"] or Decimal("0.00")
            
            monto += OperacionManual.objects.filter(
                empresa=empresa,
                ejercicio=ejercicio,
                tipo="INGRESO",
                cuenta_id__in=hijos_ids,
                fecha__month=mes
            ).aggregate(total=Sum("monto"))["total"] or Decimal("0.00")
            
            fila["meses"].append(monto)
            total_anio += monto
        
        fila["total"] = total_anio
        resultado_final.append(fila)

    return render(request, "presupuestos/reports/reporte_mensual_resumen.html", {
        "ejercicio": ejercicio,
        "meses_nombres": meses_nombres,
        "datos": resultado_final,
        "empresa_nombre": empresa,
    })

def reporte_reformas_ampliaciones(request):
    """Informe de ampliaciones por periodo."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    ejercicio_id = request.GET.get("ejercicio")
    ejercicio = get_object_or_404(EjercicioFiscal, id=ejercicio_id)

    # Ampliaciones: cuenta_origen es None, cuenta_destino tiene tipo INGRESO
    # Disminuciones: Podrían estar en la misma tabla con monto negativo o tipo específico.
    # El modelo ReformaPresupuestaria no tiene "tipo", se deduce por origen/destino y monto.
    # Asumimos que si cuenta_origen es None, es ampliación.
    
    reformas = ReformaPresupuestaria.objects.filter(
        empresa=empresa,
        ejercicio=ejercicio,
        cuenta_origen__isnull=True,
        cuenta_destino__tipo_presupuesto="INGRESO",
        is_active=True
    ).order_by("fecha", "referencia")

    return render(request, "presupuestos/reports/reporte_reformas_detalle.html", {
        "titulo": "Informe de Ampliaciones al Presupuesto",
        "subtitulo": f"Ejercicio Fiscal {ejercicio.anio}",
        "empresa_nombre": empresa,
        "datos": reformas,
        "tipo": "AMPLIACION",
        "hoy": date.today(),
    })

def reporte_reformas_traspasos(request):
    """Informe de traspasos (Transferencias de más y de menos)."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    ejercicio_id = request.GET.get("ejercicio")
    ejercicio = get_object_or_404(EjercicioFiscal, id=ejercicio_id)

    # Traspasos: ambos tienen cuenta y al menos uno es de INGRESO
    traspasos = ReformaPresupuestaria.objects.filter(
        empresa=empresa,
        ejercicio=ejercicio,
        cuenta_origen__isnull=False,
        cuenta_destino__isnull=False,
        is_active=True
    ).filter(
        Q(cuenta_origen__tipo_presupuesto="INGRESO") | Q(cuenta_destino__tipo_presupuesto="INGRESO")
    ).order_by("fecha")

    return render(request, "presupuestos/reports/reporte_reformas_detalle.html", {
        "titulo": "Informe de Transferencias (Traspasos)",
        "subtitulo": f"Ejercicio Fiscal {ejercicio.anio}",
        "empresa_nombre": empresa,
        "datos": traspasos,
        "tipo": "TRASPASO",
        "hoy": date.today(),
    })

def reporte_liquidacion_f01(request):
    """Liquidación de Ingresos Forma 01 con integración de Tributario."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    ejercicio_id = request.GET.get("ejercicio")
    ejercicio = get_object_or_404(EjercicioFiscal, id=ejercicio_id)
    
    # Obtener todas las cuentas de ingreso
    cuentas = CuentaPresupuestaria.objects.filter(
        empresa=empresa, tipo_presupuesto="INGRESO", is_active=True
    ).order_by("codigo")
    
    data_map = {}
    for c in cuentas:
        data_map[c.id] = {
            "obj": c,
            "inicial": Decimal("0.00"),
            "ampliaciones": Decimal("0.00"),
            "disminuciones": Decimal("0.00"),
            "devengado": Decimal("0.00"),
            "recaudado": Decimal("0.00"),
        }

    # Presupuesto Inicial
    pa_qs = PresupuestoAnual.objects.filter(empresa=empresa, ejercicio=ejercicio)
    for pa in pa_qs:
        if pa.cuenta_id in data_map:
            data_map[pa.cuenta_id]["inicial"] = pa.monto_inicial

    # Reformas (Ampliaciones y Disminuciones)
    ref_qs = ReformaPresupuestaria.objects.filter(empresa=empresa, ejercicio=ejercicio, is_active=True)
    for ref in ref_qs:
        if ref.tipo == "AMPLIACION" and ref.cuenta_destino_id in data_map:
            data_map[ref.cuenta_destino_id]["ampliaciones"] += ref.monto
        elif ref.tipo == "REDUCCION" and ref.cuenta_destino_id in data_map:
            data_map[ref.cuenta_destino_id]["disminuciones"] += ref.monto
        # Nota: Los traspasos afectan a ambas, pero el usuario pidió 
        # columnas específicas para Ampliaciones y Disminuciones aprobadas.

    # Ingreso Recaudado (usamos el helper existente)
    ejecucion = _obtener_ejecucion_ingresos(empresa, ejercicio.id)
    exec_map = {d["codigo"]: d["recaudado"] for d in ejecucion}

    # Ingreso Devengado (Cálculo desde Tributario)
    # 1. De DeclaracionVolumen (Impuestos declarados por año)
    from tributario.models import DeclaracionVolumen, TasasDecla, TarifasICS, Rubro
    
    # Mapear rubros a cuentas presupuestarias
    rubros_map = {r.codigo: r.cuenta for r in Rubro.objects.filter(empresa=empresa)}
    
    decla_qs = DeclaracionVolumen.objects.filter(empresa=empresa, ano=ejercicio.anio)
    # Simplificación: No hay un link directo de DeclaracionVolumen a Cuenta, 
    # pero podemos intentar a través de Actividad o Rubro (asumimos lógica por ahora).
    # Muchos sistemas usan el rubro asociado al negocio.
    
    # Sumar TasasDecla (Directamente tienen 'cuenta')
    tasas_qs = TasasDecla.objects.filter(empresa=empresa, ano=ejercicio.anio).values("cuenta").annotate(total=Sum("valor"))
    for t in tasas_qs:
        c_obj = cuentas.filter(codigo=t["cuenta"]).first()
        if c_obj and c_obj.id in data_map:
            data_map[c_obj.id]["devengado"] += t["total"] or Decimal("0.00")

    # Sumar TarifasICS (Directamente tienen 'cuenta')
    ics_qs = TarifasICS.objects.filter(empresa=empresa).values("cuenta").annotate(total=Sum("valor")) # valor es la tarifa?
    # No, devengado es emisión. Buscaremos registros de facturación si los hay.
    # Por ahora, acumulamos lo que se encuentre en TasasDecla que es lo más cercano a emisión.

    # Agregación ascendente
    cuentas_sorted = sorted(cuentas, key=lambda x: x.nivel, reverse=True)
    for c in cuentas_sorted:
        # Asignar recaudado del exec_map
        if c.codigo in exec_map:
            data_map[c.id]["recaudado"] = exec_map[c.codigo]

        if c.cuenta_padre_id and c.cuenta_padre_id in data_map:
            p_id = c.cuenta_padre_id
            data_map[p_id]["inicial"] += data_map[c.id]["inicial"]
            data_map[p_id]["ampliaciones"] += data_map[c.id]["ampliaciones"]
            data_map[p_id]["disminuciones"] += data_map[c.id]["disminuciones"]
            data_map[p_id]["devengado"] += data_map[c.id]["devengado"]
            # Recaudado ya viene agregado por el helper _obtener_ejecucion_ingresos

    # Resultado Final
    final_data = []
    for c in cuentas:
        d = data_map[c.id]
        if d["inicial"] == 0 and d["ampliaciones"] == 0 and d["disminuciones"] == 0 and d["recaudado"] == 0:
            continue
            
        definitivo = d["inicial"] + d["ampliaciones"] - d["disminuciones"]
        pendiente = d["devengado"] - d["recaudado"]
        
        final_data.append({
            "codigo": c.codigo,
            "nombre": c.nombre,
            "nivel": c.nivel,
            "inicial": d["inicial"],
            "ampliaciones": d["ampliaciones"],
            "disminuciones": d["disminuciones"],
            "definitivo": definitivo,
            "devengado": d["devengado"],
            "recaudado": d["recaudado"],
            "pendiente": pendiente,
        })

    return render(request, "presupuestos/reports/reporte_liquidacion_f01.html", {
        "empresa_nombre": empresa,
        "ejercicio": ejercicio,
        "datos": final_data,
        "hoy": date.today(),
    })

def consulta_por_cuenta(request):
    """Generar ingresos por una cuenta o fracción de cuenta."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")
        
    empresa = get_empresa(request)
    ejercicio_id = request.GET.get("ejercicio")
    cuenta_filtro = request.GET.get("cuenta", "").strip()
    nivel_filtro = request.GET.get("nivel", "5")
    
    ejercicios = EjercicioFiscal.objects.all().order_by("-anio")
    
    if not ejercicio_id:
        ejercicio_actual = ejercicios.first()
        ejercicio_id = str(ejercicio_actual.id) if ejercicio_actual else ""
    
    ejercicio = get_object_or_404(EjercicioFiscal, id=ejercicio_id)
    
    # Solo consultar si se proporcionó un filtro de cuenta
    datos_filtrados = []
    if cuenta_filtro:
        datos_completos = _obtener_ejecucion_ingresos(empresa, ejercicio.id)
        for d in datos_completos:
            if d["codigo"].startswith(cuenta_filtro) and d["nivel"] <= int(nivel_filtro):
                datos_filtrados.append(d)
            
    return render(request, "presupuestos/reports/consulta_por_cuenta.html", {
        "empresa_nombre": empresa,
        "ejercicio": ejercicio,
        "ejercicio_id": ejercicio_id,
        "ejercicios": ejercicios,
        "cuenta_filtro": cuenta_filtro,
        "nivel_filtro": nivel_filtro,
        "datos": datos_filtrados,
        "hoy": date.today(),
    })
