from decimal import Decimal
from datetime import date
from django.utils import timezone
from .models import TarifasPersonal, DeclaracionPersonal

def calcular_impuesto_personal(renta_bruta, deducciones, ano_fiscal):
    """
    Calcula el impuesto personal basado en las escalas (tarifas) del año fiscal.
    Honduras: Impuesto sobre la renta personal suele tener una base exenta y escalas progresivas.
    """
    renta_neta = max(Decimal('0.00'), Decimal(renta_bruta) - Decimal(deducciones))
    tarifas = TarifasPersonal.objects.filter(ano=ano_fiscal).order_by('desde')
    
    impuesto_total = Decimal('0.00')
    
    if not tarifas.exists():
        # Fallback o log error - debería haber tarifas en la BD
        return Decimal('0.00'), renta_neta

    for tarifa in tarifas:
        if renta_neta > tarifa.desde:
            rango_gravable = min(renta_neta, tarifa.hasta) - tarifa.desde
            if rango_gravable > 0:
                # La tasa suele ser por millar o porcentaje. Aquí asumimos millar si es > 1, o porcentaje si es < 1.
                # Ajustar según la ley específica.
                impuesto_total += (rango_gravable * tarifa.tasa) / Decimal('1000.00')
                impuesto_total += tarifa.valor_fijo
                
    return impuesto_total.quantize(Decimal('0.01')), renta_neta

def calcular_multa_y_recargos(monto_impuesto, fecha_declaracion, ano_fiscal):
    """
    Calcula multa por declaración tardía (5% usualmente) y recargos por mora (1% mensual).
    Fecha límite usual en Honduras: 30 de Abril.
    """
    fecha_limite = date(ano_fiscal + 1, 4, 30)
    fecha_dec = fecha_declaracion.date() if hasattr(fecha_declaracion, 'date') else fecha_declaracion
    
    multa = Decimal('0.00')
    recargo = Decimal('0.00')
    
    if fecha_dec > fecha_limite:
        # Multa por presentación tardía (5% del impuesto)
        multa = (monto_impuesto * Decimal('0.05')).quantize(Decimal('0.01'))
        
        # Recargos por mora (intereses) - 1% por mes o fracción
        meses_atraso = (fecha_dec.year - fecha_limite.year) * 12 + (fecha_dec.month - fecha_limite.month)
        if fecha_dec.day > fecha_limite.day:
            meses_atraso += 1
            
        if meses_atraso > 0:
            recargo = (monto_impuesto * Decimal('0.01') * Decimal(meses_atraso)).quantize(Decimal('0.01'))
            
import openpyxl
import csv
import io
from .models import DetallePlanilla

def procesar_archivo_planilla(planilla_id):
    """
    Procesa un archivo de planilla (Excel o CSV) y crea los registros de detalle.
    """
    planilla = PlanillaEmpresa.objects.get(id=planilla_id)
    archivo = planilla.archivo
    
    # Identificar tipo de archivo por extensión
    extension = archivo.name.split('.')[-1].lower()
    
    detalles_creados = 0
    
    if extension in ['xlsx', 'xls']:
        # Procesar Excel
        wb = openpyxl.load_workbook(archivo)
        sheet = wb.active
        # Asumimos encabezados en la fila 1: Identidad, Nombre, Sueldo, Retenido
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not row[0]: continue # Saltar filas vacías
            
            DetallePlanilla.objects.create(
                planilla=planilla,
                identidad=str(row[0]).strip(),
                nombre_empleado=str(row[1]).strip(),
                sueldo_bruto=Decimal(str(row[2] or 0)),
                impuesto_retenido=Decimal(str(row[3] or 0))
            )
            detalles_creados += 1
            
    elif extension == 'csv':
        # Procesar CSV
        content = archivo.read().decode('utf-8')
        csv_reader = csv.reader(io.StringIO(content))
        next(csv_reader) # Saltar encabezado
        for row in csv_reader:
            if not row[0]: continue
            
            DetallePlanilla.objects.create(
                planilla=planilla,
                identidad=row[0].strip(),
                nombre_empleado=row[1].strip(),
                sueldo_bruto=Decimal(row[2] or 0),
                impuesto_retenido=Decimal(row[3] or 0)
            )
            detalles_creados += 1
            
    planilla.procesado = True
    planilla.save()
    return detalles_creados
