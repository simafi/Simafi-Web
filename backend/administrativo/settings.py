# Configuración específica para la aplicación administrativo
# Este archivo puede contener configuraciones específicas de la aplicación

# Configuración de la base de datos para la aplicación administrativo
import os
_db_url = os.environ.get('DATABASE_URL', '').strip()
if _db_url:
    from urllib.parse import urlparse, unquote
    p = urlparse(_db_url)
    DATABASE_CONFIG = {'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': unquote((p.path or "").lstrip("/")).strip() or "postgres",
        'USER': unquote(p.username or ""), 'PASSWORD': unquote(p.password or ""),
        'HOST': p.hostname, 'PORT': str(p.port or 5432),
    }}
else:
    DATABASE_CONFIG = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'simafiweb',
            'USER': 'root', 'PASSWORD': '', 'HOST': 'localhost', 'PORT': '3306',
            'OPTIONS': {'charset': 'latin1', 'collation': 'latin1_swedish_ci'},
        }
    }

# Configuración de la aplicación
APP_CONFIG = {
    'name': 'administrativo',
    'verbose_name': 'Administrativo',
    'description': 'Sistema de configuración administrativa para todos los municipios',
}





































