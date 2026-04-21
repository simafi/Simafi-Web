"""
Django settings — SIMAFI Web (tributario).

Desarrollo: `.env` en simafiweb/.env (opcional). Producción VPS: DJANGO_SECRET_KEY,
DJANGO_ALLOWED_HOSTS, DJANGO_DB_*, DJANGO_DEBUG=0
"""
from pathlib import Path
import os
import sys

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Agregar el directorio Scripts al PYTHONPATH para importar módulos como 'core' y 'usuarios'
SCRIPTS_DIR = BASE_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# En este repo, `SCRIPTS_DIR` apunta a `.../backend`; el root real es su padre.
REPO_ROOT = SCRIPTS_DIR.parent

try:
    from dotenv import load_dotenv

    for _env_path in (REPO_ROOT / '.env', SCRIPTS_DIR / '.env', BASE_DIR / '.env'):
        if _env_path.is_file():
            load_dotenv(_env_path)
            break
except ImportError:
    pass


def _env_bool(key, default=False):
    v = os.environ.get(key)
    if v is None:
        return default
    return v.strip().lower() in ('1', 'true', 'yes', 'on')


DEBUG = _env_bool('DJANGO_DEBUG', True)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '').strip()
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'django-insecure-dev-only-not-for-production'
    else:
        raise ImproperlyConfigured(
            'Defina la variable de entorno DJANGO_SECRET_KEY en producción (DEBUG=0).'
        )

_allowed = os.environ.get('DJANGO_ALLOWED_HOSTS', '').strip()
if _allowed:
    ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver', '0.0.0.0']

# Vercel: el subdominio cambia por proyecto/preview; el prefijo "." acepta cualquier `*.vercel.app`.
# Esto evita `DisallowedHost` cuando aún no se ha configurado `DJANGO_ALLOWED_HOSTS`.
if _env_bool('VERCEL', False) or _env_bool('DJANGO_VERCEL', False):
    if '.vercel.app' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append('.vercel.app')

# Túneles (ngrok, localtunnel): el subdominio gratuito cambia; el prefijo "." acepta cualquier subdominio.
if DEBUG:
    ALLOWED_HOSTS.extend(
        [
            '.ngrok-free.dev',
            '.ngrok.io',
            '.ngrok.app',
            '.loca.lt',
        ]
    )
    CSRF_TRUSTED_ORIGINS = [
        'http://127.0.0.1:8000',
        'http://localhost:8000',
        'http://127.0.0.1:8080',
        'http://localhost:8080',
    ]
    _csrf_dev = os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').strip()
    if _csrf_dev:
        CSRF_TRUSTED_ORIGINS.extend([o.strip() for o in _csrf_dev.split(',') if o.strip()])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'widget_tweaks',
    
    # Módulos Simafiweb (estructura modular normalizada)
    'core',
    'usuarios',
    'contabilidad',  # Módulo Contable NIC/IAS
    # 'catastro',  # Comentado por conflicto de db_table 'identificacion'
    # 'catastro.catastro_app',
    # 'presupuestos',
    # 'tesoreria',
    'administrativo',
    'compras',  # Compras públicas, cotizaciones, OC, bodega (integración presupuesto/contabilidad/tesorería)
    # 'ambiental',
    # 'conveniopagos',
    'servicios_publicos',
    'configuracion',
    # 'reportes',
    # 'api',
    # 'tributario',  # COMENTADO - Causa conflicto de registro de modelos. Los modelos se importan directamente.
    'tributario_app',
    
    # Aplicación administrativo
    'administrativo_app',

    # Módulo presupuestos (planificación y control presupuestario)
    'presupuestos',

    # Módulo tesorería (configuración de caja/bancos y chequeras)
    'tesoreria',

    # Portal ciudadano / contribuyente — trámites en línea
    'ciudadano',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'tributario_app.middleware.NgrokCsrfTrustMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.middleware.ModuloAccesoMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'tributario_app', 'templates'),
            os.path.join(BASE_DIR, 'templates'),
            # Agregar templates de otros módulos
            os.path.join(SCRIPTS_DIR, 'catastro', 'templates'),
            os.path.join(SCRIPTS_DIR, 'contabilidad', 'templates'),
            os.path.join(SCRIPTS_DIR, 'compras', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tributario_app.context_processors.cursor_ai_config',
                'tributario_app.context_processors.municipio_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'tributario_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

def _parse_database_url(url: str) -> dict:
    """
    Soporte simple para DATABASE_URL estilo Supabase/Heroku.
    Evita dependencia extra (dj-database-url).
    """
    from urllib.parse import urlparse, parse_qs, unquote

    parsed = urlparse(url)
    if parsed.scheme not in ("postgres", "postgresql"):
        raise ImproperlyConfigured("DATABASE_URL debe ser postgres/postgresql")

    qs = parse_qs(parsed.query or "")
    dbname = unquote((parsed.path or "").lstrip("/")).strip()
    if not dbname:
        # Algunos proveedores omiten el path o dejan "/" (dbname vacío).
        dbname = (qs.get("dbname", [""])[0] or qs.get("database", [""])[0] or "").strip()
    if not dbname:
        dbname = "postgres"

    host = (parsed.hostname or "").strip()
    port = str(parsed.port or 5432)
    if not host:
        raise ImproperlyConfigured("DATABASE_URL inválida: falta el host.")

    options = {}
    # Supabase/Vercel Postgres suelen requerir SSL.
    if host.endswith("supabase.com") or host.endswith("supabase.co"):
        options["sslmode"] = "require"

    pgbouncer = qs.get("pgbouncer", ["false"])[0].lower() in ("1", "true", "yes", "on")
    # Pooler de Supabase (puerto 6543) normalmente implica transaction pooling.
    if (not pgbouncer) and ("pooler.supabase.com" in host) and port == "6543":
        pgbouncer = True

    cfg = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": dbname,
        "USER": unquote(parsed.username or ""),
        "PASSWORD": unquote(parsed.password or ""),
        "HOST": host,
        "PORT": port,
        # Si se usa pgbouncer, conviene no reusar conexiones mucho tiempo.
        "CONN_MAX_AGE": 0 if pgbouncer else 60,
    }
    if options:
        cfg["OPTIONS"] = options
    return cfg


_database_url = (
    (os.environ.get("DJANGO_DATABASE_URL") or "").strip().strip('"').strip("'")
    or (os.environ.get("DATABASE_URL") or "").strip().strip('"').strip("'")
)

if _database_url:
    DATABASES = {"default": _parse_database_url(_database_url)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DJANGO_DB_NAME", "").strip(),
            "USER": os.environ.get("DJANGO_DB_USER", "").strip(),
            "PASSWORD": os.environ.get("DJANGO_DB_PASSWORD", ""),
            "HOST": os.environ.get("DJANGO_DB_HOST", "").strip(),
            "PORT": os.environ.get("DJANGO_DB_PORT", "5432").strip() or "5432",
            "CONN_MAX_AGE": int(os.environ.get("DJANGO_CONN_MAX_AGE", "60")),
        }
    }

if not DEBUG:
    if not _database_url:
        missing = [k for k in ('DJANGO_DB_NAME', 'DJANGO_DB_USER', 'DJANGO_DB_PASSWORD', 'DJANGO_DB_HOST') if not (os.environ.get(k) or '').strip()]
        if missing:
            raise ImproperlyConfigured(
                'Faltan variables de entorno de base de datos para producción: ' + ', '.join(missing)
            )


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Tegucigalpa'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Configuración de idiomas disponibles
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
]

# Configuración de localización
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Configuración de formato de fechas y números para español
DATE_FORMAT = 'd/m/Y'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'd/m/Y H:i:s'
SHORT_DATE_FORMAT = 'd/m/Y'
SHORT_DATETIME_FORMAT = 'd/m/Y H:i'

# Configuración de separadores decimales para español
# Comentado para evitar conflictos con el sistema
# DECIMAL_SEPARATOR = ','
# THOUSAND_SEPARATOR = '.'
# NUMBER_GROUPING = 3


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Configuración adicional para archivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / 'tributario_app' / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise (Vercel / serverless): servir estáticos empaquetados con la app.
STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# Archivos subidos (constancias, PDFs, documentación proveedores). En VPS: ruta absoluta persistente.
MEDIA_URL = os.environ.get('DJANGO_MEDIA_URL', '/media/').strip() or '/media/'
_media_root = os.environ.get('DJANGO_MEDIA_ROOT', '').strip()
if _media_root:
    MEDIA_ROOT = Path(_media_root)
else:
    MEDIA_ROOT = SCRIPTS_DIR / 'media'

# Correo (configurar SMTP en producción). En desarrollo suele bastar consola.
EMAIL_BACKEND = os.environ.get(
    'DJANGO_EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend',
)
DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL', 'noreply@simafi.local')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Proxy (ngrok, Nginx): el cliente usa HTTPS pero Gunicorn/runserver recibe HTTP.
# Sin esto, request.is_secure() es False, las cookies de sesión fallan en https://*.ngrok-free.dev
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# --- HTTPS duro — solo con DEBUG=False (producción) ---
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = _env_bool('DJANGO_SECURE_SSL_REDIRECT', True)
    SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = False
    SECURE_CONTENT_TYPE_NOSNIFF = True
    # Para tiles (OSM) y recursos cross-origin, no bloquear el Referer completamente.
    # OSM bloquea tráfico sin Referer; esta política envía el origen en requests cross-origin.
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    X_FRAME_OPTIONS = 'DENY'

    _csrf_origins = os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').strip()
    if _csrf_origins:
        CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(',') if o.strip()]
    else:
        CSRF_TRUSTED_ORIGINS = []

    # Vercel: si no se definió CSRF explícitamente, intentar inferir el origen HTTPS desde VERCEL_URL.
    if not CSRF_TRUSTED_ORIGINS and (_env_bool('VERCEL', False) or _env_bool('DJANGO_VERCEL', False)):
        from urllib.parse import urlparse

        _vercel_url = (os.environ.get('VERCEL_URL') or os.environ.get('DJANGO_VERCEL_URL') or '').strip()
        if _vercel_url:
            parsed = urlparse(_vercel_url if '://' in _vercel_url else f'https://{_vercel_url}')
            if parsed.scheme and parsed.netloc:
                CSRF_TRUSTED_ORIGINS = [f'{parsed.scheme}://{parsed.netloc}']

# filepath: tu_proyecto/settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'tributario_app': {  # Cambiado de 'hola' a 'tributario_app'
            'handlers': ['console'],
            'level': 'INFO',  # Puedes cambiar a DEBUG para más detalles
            'propagate': True,
        },
    },
}

# Configuración de sesiones
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'simafiweb_sessionid'
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
