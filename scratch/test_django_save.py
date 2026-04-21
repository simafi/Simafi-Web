import os
import django
import sys

# Set up Django environment
sys.path.append(r'c:\simafiweb')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.catastro.config.settings')
django.setup()

from tributario_app.models import Negocio
from django.utils import timezone

def test_save():
    try:
        print("Intentando guardar un negocio de prueba...")
        # Usar datos de prueba
        test_negocio = Negocio(
            empre='0301',
            rtm='TEST1234',
            expe='001',
            nombrenego='NEGOCIO DE PRUEBA',
            identidad='1234567890123',
            catastral='12345678901234567',
            estatus='A',
            socios='Socio Prueba'
        )
        test_negocio.save()
        print("✅ Guardado exitoso")
        
        # Limpiar
        test_negocio.delete()
        print("✅ Borrado exitoso")
        
    except Exception as e:
        print(f"❌ Error al guardar: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_save()
