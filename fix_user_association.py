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

def fix_test_user_association():
    username = "test_catastro"
    
    try:
        user = Usuario.objects.get(usuario=username)
        print(f"User found: {user.usuario}")
        
        # Link to La Ceiba (Code 0101, ID 5)
        user.empresa = "0101"
        user.municipio_id = 5
        user.save()
        
        print(f"Successfully linked {username} to La Ceiba (0101).")
        
    except Usuario.DoesNotExist:
        print(f"Error: User {username} not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_test_user_association()
