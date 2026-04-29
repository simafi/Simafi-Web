# Pruebas locales con PostgreSQL (bdsimafi)

## 1) Pre-requisitos
- PostgreSQL corriendo en `localhost:5432`
- Base de datos: `bdsimafi`
- Usuario: `postgres`
- Contraseña: `sandres`

## 2) Arranque rápido (PowerShell)
En `C:\simafiweb\backend` puedes usar el script que pide la contraseña y arranca en un puerto libre (por defecto 8010):

```powershell
cd C:\simafiweb\backend
.\run_local_postgres.ps1 -Port 8010
```

## 3) Alternativa manual (si prefieres variables)

```powershell
cd C:\simafiweb

$env:DJANGO_DEBUG='1'
$env:DJANGO_SECRET_KEY='django-insecure-dev-only-not-for-production'
$env:DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'

$env:DJANGO_DB_ENGINE=''
$env:DJANGO_USE_MYSQL='0'
$env:DJANGO_SECURE_SSL_REDIRECT='0'
$env:DJANGO_DATABASE_URL='postgresql://postgres:TU_PASSWORD@127.0.0.1:5432/bdsimafi'

python backend\manage.py migrate
python backend\manage.py runserver 127.0.0.1:8010
```

## 5) Verificación rápida
- Portal ciudadano: `http://127.0.0.1:8010/ciudadano/`
- Nueva solicitud: `http://127.0.0.1:8010/ciudadano/solicitud/nueva/`

