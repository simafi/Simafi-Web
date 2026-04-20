# Despliegue en VPS Linux (opción 1)

## Resumen de rutas del proyecto

- Código Django: `venv/Scripts/tributario/` (contiene `manage.py` y el paquete `tributario_app`).
- Módulos compartidos: `venv/Scripts/` (debe estar en `PYTHONPATH`; `settings.py` lo añade).
- Variables de entorno: copiar `../.env.example` a `simafiweb/.env` o usar `/etc/simafi.env` en el servidor.

## Comandos típicos (después de clonar en el VPS)

```bash
cd /srv/simafi/venv/Scripts/tributario
python3 -m venv /srv/simafi/venv
source /srv/simafi/venv/bin/activate
pip install -r /srv/simafi/requirements.txt
export $(grep -v '^#' /etc/simafi.env | xargs)   # o usar EnvironmentFile en systemd
python manage.py migrate
python manage.py collectstatic --noinput
```

## Gunicorn

Ejemplo manual (ajustar rutas):

```bash
cd /srv/simafi/venv/Scripts/tributario
export PYTHONPATH=/srv/simafi/venv/Scripts
export DJANGO_SETTINGS_MODULE=tributario_app.settings
gunicorn -c /srv/simafi/deploy/gunicorn.conf.py tributario_app.wsgi:application
```

Servicio systemd: ver `systemd/simafi-gunicorn.service.example`.

## Nginx

Plantilla: `nginx/simafi.conf.example`.  
`DJANGO_MEDIA_ROOT` en el servidor debe coincidir con el `alias` de `/media/`.

## Variables obligatorias en producción

- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY` (valor aleatorio largo)
- `DJANGO_ALLOWED_HOSTS` (dominio/s)
- `DJANGO_DB_*` (sobre todo `DJANGO_DB_PASSWORD`)
- `DJANGO_CSRF_TRUSTED_ORIGINS` (p. ej. `https://tu-dominio.gob.hn`)

Ver `../.env.example`.
