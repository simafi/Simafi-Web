# Gunicorn — ajustar rutas al desplegar en el VPS.
# Ejemplo: gunicorn -c deploy/gunicorn.conf.py tributario_app.wsgi:application
# (ejecutar con cwd = directorio que contiene el paquete tributario_app, p. ej. .../venv/Scripts/tributario)

import multiprocessing
import os

bind = os.environ.get("GUNICORN_BIND", "127.0.0.1:8001")
workers = int(os.environ.get("GUNICORN_WORKERS", max(2, multiprocessing.cpu_count() * 2 + 1)))
threads = int(os.environ.get("GUNICORN_THREADS", "1"))
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "120"))
graceful_timeout = int(os.environ.get("GUNICORN_GRACEFUL_TIMEOUT", "30"))
worker_class = "sync"
raw_env = [
    "DJANGO_SETTINGS_MODULE=tributario_app.settings",
]
accesslog = "-"
errorlog = "-"
capture_output = True
