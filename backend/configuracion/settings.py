# Configuración específica para la aplicación administrativo
# Este archivo puede contener configuraciones específicas de la aplicación

# Configuración de la base de datos para la aplicación administrativo
DATABASE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'simafiweb',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'latin1',
            'collation': 'latin1_swedish_ci',
        },
    }
}

# Configuración de la aplicación
APP_CONFIG = {
    'name': 'administrativo',
    'verbose_name': 'Administrativo',
    'description': 'Sistema de configuración administrativa para todos los municipios',
}







