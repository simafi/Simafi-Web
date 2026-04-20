import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario.models import TasasDecla

print("Verificando campo tipota...")
total = TasasDecla.objects.count()
print(f"Total registros: {total}")

if total > 0:
    tasa = TasasDecla.objects.first()
    print(f"Primer registro:")
    print(f"  ID: {tasa.id}")
    print(f"  RTM: {tasa.rtm}")
    print(f"  Rubro: {tasa.rubro}")
    print(f"  Tipota: '{tasa.tipota}'")
    print(f"  Valor: {tasa.valor}")
    
    # Verificar si tiene tipota
    if hasattr(tasa, 'tipota'):
        print("✅ Campo tipota existe")
    else:
        print("❌ Campo tipota NO existe")
    
    # Verificar si tiene tipo (antiguo)
    if hasattr(tasa, 'tipo'):
        print("⚠️ Campo tipo (antiguo) aún existe")
    else:
        print("✅ Campo tipo (antiguo) no existe")
else:
    print("No hay registros en la tabla")









































