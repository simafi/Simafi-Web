param(
  [int]$Port = 8010,
  # Pasa la URL de Supabase PROD explícitamente (o por variable de entorno).
  [string]$DatabaseUrl = ""
)

$ErrorActionPreference = "Stop"

# Ejecutar desde backend/
Set-Location $PSScriptRoot

# Usar el Python del venv si existe
$venvPython = Join-Path (Split-Path $PSScriptRoot -Parent) "venv\\Scripts\\python.exe"
$py = "python"
if (Test-Path $venvPython) { $py = $venvPython }

if (-not $DatabaseUrl) {
  $DatabaseUrl = ($env:DATABASE_URL | ForEach-Object { if ($_ -ne $null) { "$_".Trim() } else { "" } })
}
if (-not $DatabaseUrl) {
  $DatabaseUrl = ($env:DJANGO_DATABASE_URL | ForEach-Object { if ($_ -ne $null) { "$_".Trim() } else { "" } })
}
if (-not $DatabaseUrl) {
  Write-Host "Falta DatabaseUrl. Pásala como -DatabaseUrl o define DATABASE_URL." -ForegroundColor Yellow
  exit 1
}

# Forzar entorno dev local pero con BD remota
$env:DJANGO_DEBUG = "1"
$env:DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"
$env:DJANGO_LOCAL_HTTP = "1"
$env:DJANGO_SECURE_SSL_REDIRECT = "0"
$env:DJANGO_ENV = "supabase_prod"

# Evitar que el entorno se comporte como Vercel en local
$env:VERCEL = ""
$env:DJANGO_VERCEL = ""
$env:DJANGO_VERCEL_URL = ""

# Forzar NO-MySQL
$env:DJANGO_DB_ENGINE = ""
$env:DJANGO_USE_MYSQL = "0"

# Usar Supabase Postgres (PROD)
$env:DATABASE_URL = $DatabaseUrl

# Evitar errores "charmap" en Windows al imprimir tildes/íconos
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "Conectando a Supabase Postgres (PROD) via DATABASE_URL (dev)..." -ForegroundColor Cyan
Write-Host "NOTA: este script NO ejecuta migrate automáticamente." -ForegroundColor Yellow

Write-Host "Arrancando servidor en http://127.0.0.1:$Port/ ..." -ForegroundColor Green
& $py .\manage.py runserver 127.0.0.1:$Port

