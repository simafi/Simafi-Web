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

from usuarios.models import Usuario
from core.models import Municipio

def audit_migrated_users():
    print(f"{'User':<20} | {'Empresa':<10} | {'Muni ID':<8} | {'Muni Name':<20} | {'Pass Format'}")
    print("-" * 80)
    
    users = Usuario.objects.all().order_by('usuario')
    for u in users:
        muni_name = u.municipio.descripcion if u.municipio else "MISSING"
        muni_id = u.municipio_id or "NULL"
        
        # Check password format
        pw = u.password or ""
        if pw.startswith('pbkdf2_'):
            fmt = "Django (PBKDF2)"
        elif len(pw) == 64:
            fmt = "Legacy (SHA256)"
        else:
            fmt = f"Unknown (len={len(pw)})"
            
        print(f"{u.usuario[:20]:<20} | {u.empresa:<10} | {str(muni_id):<8} | {muni_name:<20} | {fmt}")

if __name__ == "__main__":
    audit_migrated_users()
