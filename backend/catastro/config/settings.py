"""
Django settings for catastro project.

Configuración específica para el módulo de Catastro.
"""

import pymysql
pymysql.install_as_MySQLdb()

from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# IMPORTANTE: Agregar el directorio catastro al PYTHONPATH PRIMERO (prioridad)
# Esto permite que Django encuentre el módulo catastro con los modelos
CATASTRO_DIR = BASE_DIR  # Este es el directorio venv/Scripts/catastro/
if str(CATASTRO_DIR) not in sys.path:
    # Insertar el directorio catastro al principio para que tenga máxima prioridad
    sys.path.insert(0, str(CATASTRO_DIR))

# Agregar el directorio Scripts al PYTHONPATH para importar módulos como 'core' y 'usuarios'
# PERO solo si no está ya en el path (para evitar conflictos con tributario)
SCRIPTS_DIR = BASE_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    # Insertar después de catastro para que catastro tenga prioridad
    sys.path.insert(1, str(SCRIPTS_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-catastro-x6&)ag9x7h)*noe#0v$aze%344^nh@+e#1@sx_hbovca7^0hn0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'widget_tweaks',
    
    # Módulos Simafiweb (estructura modular normalizada)
    'core',
    'usuarios',
    'catastro',  # Módulo de catastro
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Templates del módulo catastro (BASE_DIR es venv/Scripts/catastro/)
            os.path.join(BASE_DIR, 'templates'),
            # Templates de módulos compartidos si existen
            os.path.join(SCRIPTS_DIR, 'templates') if os.path.exists(os.path.join(SCRIPTS_DIR, 'templates')) else None,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# Filtrar None de TEMPLATES['DIRS']
TEMPLATES[0]['DIRS'] = [d for d in TEMPLATES[0]['DIRS'] if d is not None]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bdsimafipy',
        'USER': 'root',        # Cambia por tu usuario de MySQL
        'PASSWORD': 'sandres', # Cambia por tu contraseña de MySQL
        'HOST': 'localhost',
        'PORT': '3307',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'latin1',
        },
    }
}


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

# Configuración de formato de fechas y números para español
# NOTA: Para campos DateInput con type="date" (HTML5), el formato debe ser YYYY-MM-DD
# Los formatos d/m/Y se usan para visualización, pero los inputs type="date" requieren YYYY-MM-DD
DATE_FORMAT = 'd/m/Y'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'd/m/Y H:i:s'
SHORT_DATE_FORMAT = 'd/m/Y'
SHORT_DATETIME_FORMAT = 'd/m/Y H:i'

# Formato para inputs HTML5 type="date" (debe ser YYYY-MM-DD)
DATE_INPUT_FORMATS = [
    '%Y-%m-%d',  # Formato requerido por HTML5 input type="date"
    '%d/%m/%Y',  # Formato español para compatibilidad
    '%Y-%m-%d',  # Formato ISO
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Configuración adicional para archivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'catastro.log',
        },
    },
    'loggers': {
        'catastro': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Configuración de sesiones específica para catastro
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'catastro_sessionid'
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

