# -*- coding: utf-8 -*-
"""Informes de referencia CGR (datos desde módulo presupuestos)."""
from datetime import date

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .models import EjercicioFiscal

from presupuestos.rendicion_services import (
    calcular_ejecucion_presupuestaria,
    detalle_op_con_montos,
    listado_compromisos,
    listado_proyectos,
    listado_reformas_todas,
    tabla_ejecucion_mensual,
)

from .cgr_registry import FORMAS_CGR, get_cgr_by_index
from .views import get_empresa, verificar_sesion


def _ejercicio_o_redirect(request):
    ejercicio_id = request.GET.get("ejercicio")
    if not ejercicio_id:
        messages.warning(request, "Seleccione un ejercicio fiscal para generar el informe.")
        return None, redirect("contabilidad:cgr_informes_hub")
    ejercicio = get_object_or_404(EjercicioFiscal, pk=ejercicio_id)
    return ejercicio, None


def cgr_informes_hub(request):
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")
    empresa = get_empresa(request)
    ejercicios = EjercicioFiscal.objects.all().order_by("-anio")
    if empresa:
        ejercicios = ejercicios.filter(empresa=empresa)
    ejercicio_id = request.GET.get("ejercicio") or (str(ejercicios.first().id) if ejercicios.exists() else "")
    return render(
        request,
        "contabilidad/cgr/hub.html",
        {
            "title": "Informes Contraloría (CGR)",
            "empresa": empresa,
            "usuario": request.session.get("nombre", ""),
            "ejercicios": ejercicios,
            "ejercicio_id": ejercicio_id,
            "formas_cgr": FORMAS_CGR,
            "hoy": date.today(),
        },
    )


def cgr_informe_forma(request, num: int):
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")
    forma = get_cgr_by_index(num)
    if not forma:
        raise Http404("Formato CGR no disponible")

    ejercicio, redir = _ejercicio_o_redirect(request)
    if redir:
        return redir
    empresa = get_empresa(request)
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

    ctx = {
        "title": f"{forma['codigo']} — {forma['titulo'][:48]}",
        "forma": forma,
        "forma_num": num,
        "ejercicio": ejercicio,
        "empresa": empresa,
        "usuario": request.session.get("nombre", ""),
        "hoy": date.today(),
        "meses_nombres": meses,
    }

    if num == 1:
        ctx["es_identificacion"] = True
    elif num == 2:
        ctx["datos_ingreso"] = calcular_ejecucion_presupuestaria(empresa, ejercicio.id, "INGRESO")
        ctx["datos_egreso"] = calcular_ejecucion_presupuestaria(empresa, ejercicio.id, "EGRESO")
    elif num == 3:
        ctx["reformas"] = listado_reformas_todas(empresa, ejercicio.id)
    elif num == 4:
        ctx["compromisos"] = listado_compromisos(empresa, ejercicio.id)
        ctx["ordenes"] = detalle_op_con_montos(empresa, ejercicio.id)
    elif num == 5:
        ctx["proyectos"] = listado_proyectos(empresa, ejercicio.id)
    elif num == 6:
        ctx["tabla_mensual_ing"] = tabla_ejecucion_mensual(empresa, ejercicio, "INGRESO")
        ctx["tabla_mensual_egr"] = tabla_ejecucion_mensual(empresa, ejercicio, "EGRESO")
    elif num == 7:
        ctx["es_control"] = True
    elif num == 8:
        ctx["es_declaracion_cgr"] = True
    else:
        raise Http404()

    return render(request, "contabilidad/cgr/cgr_forma_detalle.html", ctx)
