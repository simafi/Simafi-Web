param(
  [int]$Port = 8010,
  # Pega aquí tu URL de Supabase SOLO cuando ejecutes el script (o pásala por parámetro).
  # Ejemplo:
  #   postgresql://postgres:PASS@db.xxxxx.supabase.co:5432/postgres?sslmode=require
  [string]$DatabaseUrl = ""
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
  Write-Host "Ejemplo: .\\run_supabase_dev.ps1 -DatabaseUrl 'postgresql://user:pass@host:5432/db?sslmode=require'" -ForegroundColor Yellow
  exit 1
}

$env:DJANGO_DEBUG = "1"
$env:DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"
$env:DJANGO_LOCAL_HTTP = "1"
$env:DJANGO_SECURE_SSL_REDIRECT = "0"

# Evitar que el entorno se comporte como Vercel en local
$env:VERCEL = ""
$env:DJANGO_VERCEL = ""
$env:DJANGO_VERCEL_URL = ""

# Forzar NO-MySQL
$env:DJANGO_DB_ENGINE = ""
$env:DJANGO_USE_MYSQL = "0"

# Usar Supabase Postgres
$env:DATABASE_URL = $DatabaseUrl

Write-Host "Conectando a Supabase Postgres via DATABASE_URL (dev)..." -ForegroundColor Cyan
Write-Host "NOTA: este script NO ejecuta migrate automáticamente (para evitar tocar producción por accidente)." -ForegroundColor Yellow

Write-Host "Arrancando servidor en http://127.0.0.1:$Port/ ..." -ForegroundColor Green
& $py .\manage.py runserver 127.0.0.1:$Port

