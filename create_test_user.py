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

from usuarios.models import Usuario, UsuarioAccesoModulo
from django.contrib.auth.hashers import make_password

def create_test_user():
    username = "test_catastro"
    raw_pass = "Catastro2026!"
    
    print(f"Creating user: {username}...")
    
    # Create or update main user
    user, created = Usuario.objects.update_or_create(
        usuario=username,
        empresa="01", # Assume default company 01
        defaults={
            "nombre": "Usuario Prueba Catastro",
            "password": raw_pass, # The save() method in our model hashes this automatically
            "is_active": True,
            "es_superusuario": False,
        }
    )
    
    # Enable access to Catastro module
    # Note: UsuarioAccesoModulo also hashes its password field in save()
    access, acc_created = UsuarioAccesoModulo.objects.update_or_create(
        usuario=user,
        codigo_modulo="catastro",
        defaults={
            "password": raw_pass
        }
    )
    
    print(f"Success! User '{username}' is ready.")
    print(f"Username: {username}")
    print(f"Password: {raw_pass}")

if __name__ == "__main__":
    create_test_user()
