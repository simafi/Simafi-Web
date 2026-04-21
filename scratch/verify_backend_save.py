import os
import django
import sys

# Añadir el backend al path
sys.path.append(r'c:\simafiweb\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catastro.config.settings')
django.setup()

from tributario.models import Negocio
import uuid

def test_backend_save_logic():
    print("Testing backend save logic (mimicking handle_salvar_negocio)...")
    
    # Datos de prueba
    test_rtm = f"TEST-{uuid.uuid4().hex[:8]}"
    test_expe = "000001"
    test_empresa = "0301"
    
    data = {
        'rtm': test_rtm,
        'expe': test_expe,
        'empresa': test_empresa,
        'nombrenego': 'NEGOCIO DE PRUEBA BACKEND',
        'comerciante': 'COMERCIANTE DE PRUEBA',
        'identidad': '1234567890123',
        'estatus': 'A',
        'catastral': '12345678901234567',
        'direccion': 'DIRECCION DE PRUEBA',
        'cx': '0.0000000',
        'cy': '0.0000000'
    }
    
    # Lógica de truncado (mimicked from views.py)
    def truncar_campo(valor, max_length):
        if valor and len(str(valor)) > max_length:
            return str(valor)[:max_length]
        return valor

    try:
        print(f"Creating/Updating Negocio: RTM={test_rtm}, EXPE={test_expe}")
        negocio, created = Negocio.objects.get_or_create(
            empresa=data.get('empresa'),
            rtm=data.get('rtm'),
            expe=data.get('expe'),
            defaults={
                'nombrenego': truncar_campo(data.get('nombrenego', ''), 100),
                'comerciante': truncar_campo(data.get('comerciante', ''), 100),
                'identidad': truncar_campo(data.get('identidad', ''), 15),
                'estatus': data.get('estatus', 'A'),
                'catastral': data.get('catastral', ''),
                'direccion': truncar_campo(data.get('direccion', ''), 200),
                'cx': data.get('cx', '0.0000000'),
                'cy': data.get('cy', '0.0000000')
            }
        )
        
        if created:
            print("Successfully created test business.")
        else:
            print("Successfully found existing test business.")
            
        # Intentar actualizar
        negocio.nombrenego = "NEGOCIO ACTUALIZADO"
        negocio.save()
        print("Successfully updated test business.")
        
        # Limpiar
        negocio.delete()
        print("Successfully deleted test business.")
        print("\nRESULT: ALL BACKEND DB OPERATIONS PASSED.")
        
    except Exception as e:
        print(f"\nRESULT: FAILED with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_backend_save_logic()
