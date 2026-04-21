import os
import sys
import django
from pathlib import Path

# 1. Setup Django
REPO_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(BACKEND_DIR / "tributario"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tributario.tributario_app.settings")
django.setup()

from core.models import Municipio

def check_muni_codes():
    for m in Municipio.objects.all():
        print(f"ID: {m.id} | Codigo: {m.codigo} | Nombre: {m.descripcion}")

if __name__ == "__main__":
    check_muni_codes()
