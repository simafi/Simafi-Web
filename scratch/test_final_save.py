import os
import django
import sys

# Set up Django environment
REPO_ROOT = r'c:\simafiweb'
BACKEND_DIR = os.path.join(REPO_ROOT, 'backend')
TRIBUTARIO_DIR = os.path.join(BACKEND_DIR, 'tributario')

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if TRIBUTARIO_DIR not in sys.path:
    sys.path.insert(0, TRIBUTARIO_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

from tributario.models import Negocio
from django.utils import timezone

def test_final_save():
    try:
        print("Intentando guardar un negocio de prueba con los cambios aplicados...")
        # Usar datos de prueba
        test_negocio, created = Negocio.objects.get_or_create(
            empresa='0301',
            rtm='TESTF_123',
            expe='001',
            defaults={
                'nombrenego': 'NEGOCIO PRUEBA FINAL',
                'identidad': '1234567890123',
                'catastral': '12345678901234567',
                'estatus': 'A',
                'socios': 'Socio Prueba'
            }
        )
        if not created:
            print("El registro ya existia, actualizando...")
            test_negocio.nombrenego = 'NEGOCIO PRUEBA FINAL UPD'
            test_negocio.save()
            
        print("SUCCESS: Guardado/Actualizacion exitosa en Supabase!")
        
        # Verificar que podemos leerlo
        obj = Negocio.objects.get(rtm='TESTF_123', expe='001')
        print(f"SUCCESS: Lectura exitosa: {obj.nombrenego}")
        
        # Limpiar
        obj.delete()
        print("SUCCESS: Borrado exitoso")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_final_save()
