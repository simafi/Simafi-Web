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

def fix_user_codes():
    users = Usuario.objects.all()
    count = 0
    for u in users:
        if u.municipio:
            expected_code = u.municipio.codigo
            if u.empresa != expected_code:
                print(f"Aligning {u.usuario}: {u.empresa} -> {expected_code}")
                u.empresa = expected_code
                u.save()
                count += 1
    print(f"\nSuccessfully aligned {count} users.")

if __name__ == "__main__":
    fix_user_codes()
