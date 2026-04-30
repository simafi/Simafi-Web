from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Contribuyente, DeclaracionPersonal, PlanillaEmpresa, DetallePlanilla
from .forms import DeclaracionPersonalForm, PlanillaUploadForm
from .services import calcular_impuesto_personal, calcular_multa_y_recargos
from tributario.models import Identificacion, Negocio, TransaccionesIcs, TransaccionesBienesInmuebles
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch

class DeclaracionListView(ListView):
    model = DeclaracionPersonal
    template_name = 'impuesto_personal/declaracion_list.html'
    context_object_name = 'declaraciones'

def crear_declaracion(request, identidad):
    persona = get_object_or_404(Identificacion, identidad=identidad)
    contribuyente, created = Contribuyente.objects.get_or_create(persona=persona)
    
    # Año actual para la declaración
    ano_actual = timezone.now().year
    
    if request.method == 'POST':
        form = DeclaracionPersonalForm(request.POST)
        if form.is_valid():
            declaracion = form.save(commit=False)
            declaracion.contribuyente = contribuyente
            declaracion.renta_neta = form.cleaned_data['renta_neta']
            declaracion.impuesto_calculado = form.cleaned_data['impuesto_calculado']
            declaracion.multa = form.cleaned_data['multa']
            declaracion.recargo = form.cleaned_data['recargo']
            declaracion.total_pagar = form.cleaned_data['total_pagar']
            declaracion.estado = 'presentada'
            declaracion.usuario = request.user.username if request.user.is_authenticated else 'admin'
            declaracion.save()
            messages.success(request, f"Declaración del año {declaracion.ano_fiscal} creada exitosamente.")
            return redirect('impuesto_personal:declaracion_list')
    else:
        form = DeclaracionPersonalForm(initial={'contribuyente': contribuyente, 'ano_fiscal': ano_actual})
        
    return render(request, 'impuesto_personal/declaracion_form.html', {
        'form': form,
        'persona': persona,
        'contribuyente': contribuyente
    })

def verificar_solvencia(request, identidad):
    """
    Verifica si un ciudadano tiene mora en Bienes Inmuebles o Negocios.
    """
    # 1. Buscar en Bienes Inmuebles
    # Nota: cocata1 está ligada a identidad en BDCata1
    mora_bi = TransaccionesBienesInmuebles.objects.filter(
        cocata1__in=Identificacion.objects.filter(identidad=identidad).values_list('identidad', flat=True), # Simplificación, usualmente hay un join
        estado='A'
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    # 2. Buscar en Negocios (ICS)
    # RTM/EXPE ligados a identidad en Negocio
    negocios = Negocio.objects.filter(identidad=identidad)
    mora_ics = TransaccionesIcs.objects.filter(
        idneg__in=negocios.values_list('id', flat=True),
        operacion='F' # Facturación
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    pagos_ics = TransaccionesIcs.objects.filter(
        idneg__in=negocios.values_list('id', flat=True),
        operacion='P' # Pago
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    saldo_ics = mora_ics + pagos_ics # Pagos suelen ser negativos o restarse
    
    tiene_mora = (mora_bi > 0) or (saldo_ics > 0)
    
    return JsonResponse({
        'identidad': identidad,
        'tiene_mora': tiene_mora,
        'mora_bienes_inmuebles': float(mora_bi),
        'mora_negocios': float(saldo_ics),
        'puede_imprimir_solvencia': not tiene_mora
    })

def importar_planilla(request):
    if request.method == 'POST':
        form = PlanillaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            planilla = form.save()
            try:
                from .services import procesar_archivo_planilla
                cant = procesar_archivo_planilla(planilla.id)
                messages.success(request, f"Planilla cargada y procesada correctamente. Se crearon {cant} registros de empleados.")
            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {str(e)}")
            return redirect('impuesto_personal:planilla_list')
    else:
        form = PlanillaUploadForm()
    return render(request, 'impuesto_personal/importar_planilla.html', {'form': form})

class PlanillaListView(ListView):
    model = PlanillaEmpresa
    template_name = 'impuesto_personal/planilla_list.html'
    context_object_name = 'planillas'

def generar_pdf_solvencia(request, identidad):
    # 1. Validar mora antes de generar
    persona = get_object_or_404(Identificacion, identidad=identidad)
    
    mora_bi = TransaccionesBienesInmuebles.objects.filter(
        cocata1__in=Identificacion.objects.filter(identidad=identidad).values_list('identidad', flat=True),
        estado='A'
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    negocios = Negocio.objects.filter(identidad=identidad)
    mora_ics = TransaccionesIcs.objects.filter(
        idneg__in=negocios.values_list('id', flat=True),
        operacion='F'
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    pagos_ics = TransaccionesIcs.objects.filter(
        idneg__in=negocios.values_list('id', flat=True),
        operacion='P'
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    saldo_ics = mora_ics + pagos_ics
    
    if (mora_bi > 0) or (saldo_ics > 0):
        messages.error(request, f"No se puede generar la solvencia para {identidad} porque presenta mora pendiente (Bienes: {mora_bi}, Negocios: {saldo_ics}).")
        return redirect('impuesto_personal:declaracion_list')

    # 2. Generar PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="solvencia_{identidad}.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Dibujar encabezado
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height - 1*inch, "MUNICIPALIDAD DE SIMAFI")
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height - 1.3*inch, "CONSTANCIA DE SOLVENCIA MUNICIPAL")
    
    p.line(1*inch, height - 1.5*inch, width - 1*inch, height - 1.5*inch)
    
    # Cuerpo del documento
    p.setFont("Helvetica", 12)
    p.drawString(1*inch, height - 2*inch, "POR MEDIO DE LA PRESENTE SE HACE CONSTAR QUE EL CIUDADANO(A):")
    
    p.setFont("Helvetica-Bold", 13)
    p.drawCentredString(width/2, height - 2.5*inch, f"{persona.nombres} {persona.apellidos}")
    p.drawCentredString(width/2, height - 2.7*inch, f"CON NÚMERO DE IDENTIDAD: {persona.identidad}")
    
    p.setFont("Helvetica", 12)
    p.drawCentredString(width/2, height - 3.5*inch, "SE ENCUENTRA EN SOLVENCIA CON SUS OBLIGACIONES TRIBUTARIAS MUNICIPALES")
    p.drawCentredString(width/2, height - 3.7*inch, "A LA FECHA DE EMISIÓN DE ESTE DOCUMENTO.")
    
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(width/2, height - 4.5*inch, "ESTA SOLVENCIA TIENE UNA VIGENCIA DE 30 DÍAS CALENDARIO.")
    
    # Firma y Sello
    p.line(width/2 - 1.5*inch, 2.5*inch, width/2 + 1.5*inch, 2.5*inch)
    p.drawCentredString(width/2, 2.3*inch, "DEPTO. DE CONTROL TRIBUTARIO")
    
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(1*inch, 0.5*inch, f"Generado el: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
    p.drawString(width - 3*inch, 0.5*inch, f"ID de Verificación: {identidad}-{int(timezone.now().timestamp())}")
    
    p.showPage()
    p.save()
    
    return response
