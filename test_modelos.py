import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tributario.tributario_app.settings")
import django
django.setup()

# Probar que el sistema carga correctamente
print("✅ Django iniciado correctamente")

# Verificar modelos
try:
    from tributario.models import TarifasImptoics, DeclaracionVolumen
    print("✅ TarifasImptoics importado correctamente")
    print("✅ DeclaracionVolumen importado correctamente")
except Exception as e:
    print(f"❌ Error importando modelos: {e}")

# Verificar TarifasICS
try:
    from tributario_app.models import TarifasICS
    print("✅ TarifasICS importado correctamente")
except Exception as e:
    print(f"❌ Error importando TarifasICS: {e}")

print("\n📊 Sistema listo para pruebas")
