import os
import django
import sys
from pathlib import Path

# Setup environment
repo_root = Path(r"c:\simafiweb")
backend_dir = repo_root / "backend"
tributario_dir = backend_dir / "tributario"
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(tributario_dir))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tributario_app.settings")
django.setup()

from contabilidad.models import EjercicioFiscal, PeriodoContable
from django.db import transaction, IntegrityError, InternalError

def test_create_ejercicio():
    print("--- Test Create Ejercicio Fiscal ---")
    empresa = "0301" # Default test empresa
    anio = 2025
    
    try:
        with transaction.atomic():
            # Mimic view logic
            ejercicio = EjercicioFiscal(
                anio=anio,
                descripcion=f"Ejercicio Fiscal {anio}",
                fecha_inicio=f"{anio}-01-01",
                fecha_fin=f"{anio}-12-31",
                estado='ABIERTO',
                empresa=empresa,
                created_by='TestRunner'
            )
            print("Attempting to save EjercicioFiscal...")
            ejercicio.save()
            print(f"EjercicioFiscal saved with ID: {ejercicio.id}")

            # Mimic period creation
            import calendar
            for mes in range(1, 13):
                ultimo_dia = calendar.monthrange(anio, mes)[1]
                PeriodoContable.objects.create(
                    ejercicio=ejercicio,
                    numero=mes,
                    nombre=f"{calendar.month_name[mes]} {anio}",
                    fecha_inicio=f"{anio}-{mes:02d}-01",
                    fecha_fin=f"{anio}-{mes:02d}-{ultimo_dia:02d}",
                    estado='ABIERTO'
                )
            print("12 Períodos successfully created.")
            
    except Exception as e:
        print(f"\n[FAIL] Error occurred: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_create_ejercicio()
