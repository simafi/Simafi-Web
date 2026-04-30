from datetime import datetime
from django.db.models import Sum
from .models import Negocio, TransaccionesIcs, DeclaracionVolumen, PermisoOperacionRequisito, Rubro

def verificar_requisitos_permiso(negocio, ano):
    """
    Verifica si un negocio cumple con todos los requisitos para emitir el Permiso de Operación.
    Retorna un diccionario con el estado de cada requisito.
    """
    empresa = negocio.empresa
    rtm = negocio.rtm
    expe = negocio.expe
    
    # 1. Estatus Activo
    estatus_ok = negocio.estatus == 'A'
    
    # 2. Solvencia Municipal (No debe tener mora en ICS)
    # Sumamos todos los montos pendientes en transaccionesics
    mora_ics = TransaccionesIcs.objects.filter(
        empresa=empresa,
        rtm=rtm,
        expe=expe,
        monto__gt=0
    ).aggregate(total=Sum('monto'))['total'] or 0
    
    solvencia_ok = (mora_ics <= 0)
    
    # 3. Declaración Jurada del año corriente
    # La declaración de volumen de ventas para el año fiscal actual
    declara_ok = DeclaracionVolumen.objects.filter(
        empresa=empresa,
        rtm=rtm,
        expe=expe,
        ano=ano
    ).exists()
    
    # 4. Pago de Tasa de Permiso (Rubro C0002)
    # Verificamos si existe el cargo del permiso para el año y si su monto pendiente es 0
    pago_permiso_ok = TransaccionesIcs.objects.filter(
        empresa=empresa,
        rtm=rtm,
        expe=expe,
        rubro__icontains='C0002',
        ano=ano,
        monto__lte=0
    ).exists()
    
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
    
    return {
        'exito': estatus_ok and solvencia_ok and declara_ok and pago_permiso_ok and manual_ok,
        'detalles': {
            'estatus': {'ok': estatus_ok, 'mensaje': 'Negocio Activo' if estatus_ok else 'Negocio Inactivo/Cancelado'},
            'solvencia': {'ok': solvencia_ok, 'mensaje': f'Solvente (Mora: L. {mora_ics:,.2f})' if solvencia_ok else f'Tiene Mora (L. {mora_ics:,.2f})'},
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
