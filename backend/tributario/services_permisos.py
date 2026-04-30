from datetime import datetime
from django.db.models import Sum
from .models import Negocio, TransaccionesIcs, DeclaracionVolumen, PermisoOperacionRequisito, Rubro

def verificar_requisitos_permiso(negocio, ano):
    """
    Verifica si un negocio cumple con todos los requisitos para emitir el Permiso de Operación.
    Retorna un diccionario con el estado de cada requisito.
    """
    import logging
    logger = logging.getLogger(__name__)
    from django.db.models.functions import Cast, Trim
    from django.db.models import IntegerField, Q
    
    empresa = negocio.empresa
    rtm = negocio.rtm
    expe = negocio.expe
    
    logger.info(f"📋 Verificando requisitos permiso para RTM: {rtm}, EXPE: {expe}, Año: {ano}")
    
    # 1. Estatus Activo
    estatus_ok = (negocio.estatus == 'A')
    
    # 2. Solvencia Municipal (No debe tener mora en ICS hasta el mes actual)
    # Según petición del usuario: controlar hasta el mes que se está emitiendo, no todo el año.
    current_date = datetime.now()
    current_month = current_date.month
    
    # Filtramos transacciones con monto > 0 que:
    # a) Sean de años anteriores
    # b) Sean del año actual pero de meses anteriores o el actual (comparación numérica)
    mora_ics_qs = TransaccionesIcs.objects.filter(
        empresa=empresa,
        rtm=rtm,
        expe=expe,
        monto__gt=0.01 # Tolerancia mínima
    ).annotate(
        mes_num=Cast(Trim('mes'), IntegerField())
    ).filter(
        Q(ano__lt=ano) | 
        Q(ano=ano, mes_num__lte=current_month)
    )
    
    mora_ics = mora_ics_qs.aggregate(total=Sum('monto'))['total'] or 0
    solvencia_ok = (mora_ics <= 0.05) # Pequeño margen de tolerancia
    
    if not solvencia_ok:
        logger.warning(f"❌ Mora detectada: L. {mora_ics} para RTM: {rtm}")
    
    # 3. Declaración Jurada del año corriente
    declara_ok = DeclaracionVolumen.objects.filter(
        empresa=empresa,
        rtm=rtm,
        expe=expe,
        ano=ano
    ).exists()
    
    if not declara_ok:
        logger.warning(f"❌ Falta declaración {ano} para RTM: {rtm}")
    
    # 4. Pago de Tasa de Permiso (Rubro C0002 o similares)
    # Verificamos si existe el cargo del permiso para el año y si su monto pendiente es <= 0
    pago_permiso_ok = TransaccionesIcs.objects.filter(
        empresa=empresa,
        rtm=rtm,
        expe=expe,
        rubro__icontains='C0002', # O usar rubro__startswith='C' si es genérico
        ano=ano,
        monto__lte=0.05
    ).exists()
    
    # Si no existe el rubro C0002, tal vez no se ha cargado. 
    # Consideramos pendiente si no existe registro de cobro para ese rubro en el año.
    if not pago_permiso_ok:
        logger.warning(f"❌ Tasa de Permiso (C0002) no pagada o no cargada para RTM: {rtm}")
    
    # 5. Requisitos Manuales (Bomberos, Salud, etc.)
    requisitos_manuales = PermisoOperacionRequisito.objects.filter(
        negocio=negocio,
        ano=ano
    ).first()
    
    manual_ok = False
    if requisitos_manuales:
        manual_ok = (
            requisitos_manuales.bomberos and 
            requisitos_manuales.salud and 
            requisitos_manuales.ambiente
        )
    
    if not manual_ok:
        logger.warning(f"❌ Requisitos manuales incompletos para RTM: {rtm}")
    
    # Construir respuesta detallada
    exito = estatus_ok and solvencia_ok and declara_ok and pago_permiso_ok and manual_ok
    
    res = {
        'exito': exito,
        'detalles': {
            'estatus': {'ok': estatus_ok, 'mensaje': 'Negocio Activo' if estatus_ok else 'Negocio Inactivo/Cancelado'},
            'solvencia': {'ok': solvencia_ok, 'mensaje': f'Solvente hasta {get_mes_nombre(current_month)} (Mora: L. {mora_ics:,.2f})' if solvencia_ok else f'Tiene Mora hasta {get_mes_nombre(current_month)} (L. {mora_ics:,.2f})'},
            'declaracion': {'ok': declara_ok, 'mensaje': f'Declaración {ano} presentada' if declara_ok else f'Falta declaración {ano}'},
            'pago_permiso': {'ok': pago_permiso_ok, 'mensaje': 'Tasa de Permiso Pagada' if pago_permiso_ok else 'Tasa de Permiso Pendiente (Rubro C0002)'},
            'manuales': {
                'ok': manual_ok,
                'bomberos': requisitos_manuales.bomberos if requisitos_manuales else False,
                'salud': requisitos_manuales.salud if requisitos_manuales else False,
                'ambiente': requisitos_manuales.ambiente if requisitos_manuales else False,
                'mensaje': 'Requisitos institucionales completos' if manual_ok else 'Faltan constancias (Bomberos/Salud/Ambiente)'
            }
        },
        'requisitos_id': requisitos_manuales.id if requisitos_manuales else None
    }
    
    logger.info(f"✅ Resultado verificación para {rtm}: {exito}")
    return res

def generar_permiso_pdf(negocio, ano):
    """
    Genera el PDF del Permiso de Operación utilizando ReportLab.
    """
    import io
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.lib.styles import getSampleStyleSheet
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # --- Encabezado ---
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height - 1*inch, "REPÚBLICA DE HONDURAS")
    p.setFont("Helvetica", 12)
    p.drawCentredString(width/2, height - 1.3*inch, "MUNICIPALIDAD DE SIMAFIWEB")
    p.drawCentredString(width/2, height - 1.5*inch, "DEPARTAMENTO DE CONTROL TRIBUTARIO")
    
    p.setLineWidth(2)
    p.line(1*inch, height - 1.7*inch, width - 1*inch, height - 1.7*inch)
    
    # --- Título ---
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width/2, height - 2.2*inch, "PERMISO DE OPERACIÓN")
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height - 2.5*inch, f"AÑO FISCAL {ano}")
    
    # --- Cuerpo ---
    styles = getSampleStyleSheet()
    p.setFont("Helvetica", 11)
    
    y = height - 3.2*inch
    line_height = 0.3*inch
    
    p.drawString(1*inch, y, "EL SUSCRITO JEFE DE CONTROL TRIBUTARIO, HACE CONSTAR QUE:")
    y -= line_height * 1.5
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(1*inch, y, f"NOMBRE DEL NEGOCIO: {negocio.nombrenego.strip()}")
    y -= line_height
    p.drawString(1*inch, y, f"RTM / EXPEDIENTE: {negocio.rtm} / {negocio.expe}")
    y -= line_height
    p.drawString(1*inch, y, f"PROPIETARIO: {negocio.comerciante.strip()}")
    y -= line_height
    p.drawString(1*inch, y, f"DIRECCIÓN: {negocio.direccion.strip()}")
    y -= line_height
    p.drawString(1*inch, y, f"ACTIVIDAD ECONÓMICA: {negocio.descriactividad.strip()}")
    y -= line_height * 2
    
    p.setFont("Helvetica", 11)
    texto_legal = (
        "Cumple con todos los requisitos establecidos en la Ley de Municipalidades y su Reglamento, "
        "así como con el Plan de Arbitrios vigente. Habiendo presentado su Declaración Jurada de Ingresos "
        "y encontrándose SOLVENTE con el Tesoro Municipal."
    )
    
    # Word wrap simple
    from reportlab.lib.utils import simpleSplit
    lines = simpleSplit(texto_legal, "Helvetica", 11, width - 2*inch)
    for line in lines:
        p.drawString(1*inch, y, line)
        y -= 0.2*inch
        
    y -= 0.5*inch
    p.drawString(1*inch, y, f"Dado en la ciudad de SimafiWeb, a los {datetime.now().day} días del mes de {get_mes_nombre(datetime.now().month)} del {datetime.now().year}.")
    
    # --- Firmas ---
    y -= 1.5*inch
    p.line(1.5*inch, y, 3.5*inch, y)
    p.line(width - 3.5*inch, y, width - 1.5*inch, y)
    
    p.setFont("Helvetica", 9)
    p.drawCentredString(2.5*inch, y - 0.2*inch, "JEFE DE CONTROL TRIBUTARIO")
    p.drawCentredString(width - 2.5*inch, y - 0.2*inch, "SECRETARIO MUNICIPAL")
    
    # --- Footer / QR Placeholder ---
    p.setFont("Helvetica-Oblique", 8)
    p.drawCentredString(width/2, 0.5*inch, "Este documento es personal e intransferible. Debe colocarse en un lugar visible del establecimiento.")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer

def get_mes_nombre(n):
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    return meses[n-1]
