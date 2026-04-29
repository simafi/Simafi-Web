#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Windows: evitar errores 'charmap' al imprimir tildes/íconos en consola.
# Esto aplica incluso si se arranca sin scripts .ps1/.bat.
os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # py>=3.7
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Este `manage.py` se ejecuta desde `backend/` como raíz del sistema modular.
# Ajusta `sys.path` para que Django pueda importar los módulos (core, usuarios, etc.)
# y el proyecto `tributario_app` que vive en `backend/tributario/`.
_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_BACKEND_DIR)
_TRIBUTARIO_DIR = os.path.join(_BACKEND_DIR, "tributario")

for p in (_BACKEND_DIR, _TRIBUTARIO_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

def main():
    """Run administrative tasks."""
    # Proyecto principal del repo (settings en `backend/tributario/tributario_app/settings.py`)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tributario_app.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
