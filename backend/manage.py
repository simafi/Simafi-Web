#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Asegurar que se use el entorno virtual: agregar venv/Lib/site-packages al path
_script_dir = os.path.dirname(os.path.abspath(__file__))
_venv_root = os.path.dirname(_script_dir)
_site_packages = os.path.join(_venv_root, 'Lib', 'site-packages')
if os.path.isdir(_site_packages) and _site_packages not in sys.path:
    sys.path.insert(0, _site_packages)

def main():
    """Run administrative tasks."""
    # Agregar el directorio tributario al path de Python
    tributario_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tributario')
    if tributario_path not in sys.path:
        sys.path.insert(0, tributario_path)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.tributario_app.settings')
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
