import os
import sys

# Set up paths like api/index.py does
REPO_ROOT = r'c:\simafiweb'
BACKEND_DIR = os.path.join(REPO_ROOT, 'backend')
TRIBUTARIO_DIR = os.path.join(BACKEND_DIR, 'tributario')

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if TRIBUTARIO_DIR not in sys.path:
    sys.path.insert(0, TRIBUTARIO_DIR)

print(f"PYTHONPATH: {sys.path[:2]}")

try:
    print("Intentando: from tributario_app.models import Negocio")
    from tributario_app.models import Negocio
    print("✅ Portado exitosamente desde tributario_app.models")
except ImportError as e:
    print(f"❌ Error al importar desde tributario_app.models: {e}")

try:
    print("Intentando: from tributario.models import Negocio")
    from tributario.models import Negocio
    print("✅ Portado exitosamente desde tributario.models")
except ImportError as e:
    print(f"❌ Error al importar desde tributario.models: {e}")
