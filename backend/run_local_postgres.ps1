param(
  [int]$Port = 8010,
  [string]$DbName = "bdsimafi",
  [string]$DbUser = "postgres",
  [string]$DbHost = "127.0.0.1",
  [int]$DbPort = 5432,
  # Si se omite, se pedirá por consola. También puede venir de $env:PG_PASSWORD.
  [string]$PgPassword = ""
)

$ErrorActionPreference = "Stop"

function Read-PlainPassword([string]$Prompt) {
  $secure = Read-Host $Prompt -AsSecureString
  $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
  try {
    return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
  } finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
  }
}

# Ejecutar desde backend/
Set-Location $PSScriptRoot

# Usar el Python del venv si existe (evita correr con otro Python del sistema)
$venvPython = Join-Path (Split-Path $PSScriptRoot -Parent) "venv\\Scripts\\python.exe"
$py = "python"
if (Test-Path $venvPython) {
  $py = $venvPython
}

$pgPass = $PgPassword
if (-not $pgPass) { $pgPass = $env:PG_PASSWORD }
if (-not $pgPass) {
  $pgPass = Read-PlainPassword "Password de PostgreSQL para '$DbUser' (no se mostrará)"
}

$env:DJANGO_DEBUG = "1"
$env:DJANGO_SECRET_KEY = "django-insecure-dev-only-not-for-production"
$env:DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"
# Evitar redirecciones a HTTPS en local por variables heredadas
$env:DJANGO_SECURE_SSL_REDIRECT = "0"
$env:DJANGO_LOCAL_HTTP = "1"

# Asegurar que no se detecte despliegue tipo Vercel (puede forzar DEBUG=0)
$env:VERCEL = ""
$env:DJANGO_VERCEL = ""
$env:DJANGO_VERCEL_URL = ""

# Forzar Postgres (evita que tome MySQL por error)
$env:DJANGO_DB_ENGINE = ""
$env:DJANGO_USE_MYSQL = "0"
$env:DJANGO_DATABASE_URL = "postgresql://$DbUser`:$pgPass@$DbHost`:$DbPort/$DbName"

# Evitar errores "charmap" en Windows al imprimir tildes/íconos
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

# Asegurar que el .env (Supabase) no domine el arranque local
$env:DATABASE_URL = ""
$env:DIRECT_URL = ""
$env:POSTGRES_URL = ""
$env:PRISMA_DATABASE_URL = ""

Write-Host "Aplicando migraciones en Postgres ($DbName)..." -ForegroundColor Cyan
& $py .\manage.py migrate

Write-Host "Arrancando servidor en http://127.0.0.1:$Port/ ..." -ForegroundColor Green
& $py .\manage.py runserver 127.0.0.1:$Port

