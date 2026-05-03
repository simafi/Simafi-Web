# Crea en Supabase/Postgres las tablas Mapas Simafi de un solo paso (equiv. migracion 0020_mapas_simafi).
#
# Antes: en la raiz del repo (simafiweb/), archivo .env.supabase_prod o .env con:
#   DATABASE_URL=postgresql://usuario:clave@host:5432/postgres?sslmode=require
# (Si Supabase pooler falla al crear tablas, use la URI "directa" puerto 5432.)
#
# Ejecutar desde esta carpeta backend\:
#   .\crear_tablas_mapas_supabase.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$venvPython = Join-Path (Split-Path $PSScriptRoot -Parent) "venv\Scripts\python.exe"
$py = "python"
if (Test-Path $venvPython) { $py = $venvPython }

$script = Join-Path $PSScriptRoot "catastro\scripts\apply_mapas_sql.py"
if (-not (Test-Path $script)) {
    Write-Error "No se encuentra $script"
    exit 1
}

Write-Host "Creando tablas catastro_mapa_* (una transaccion)..." -ForegroundColor Cyan
& $py $script
exit $LASTEXITCODE
