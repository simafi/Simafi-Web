# Aplica en Supabase/Postgres las tablas Mapas Simafi (catastro_mapa_*).
#
# Requiere: variable DATABASE_URL (o DIRECT_URL / DJANGO_DATABASE_URL / SUPABASE_DATABASE_URL).
# No necesita "psql": usa Python + psycopg (requirements.txt).
#
# Ejemplo (PowerShell, desde esta carpeta backend\):
#   $env:DATABASE_URL = "postgresql://postgres.xxxx:TU_CLAVE@aws-0-xxx.pooler.supabase.com:6543/postgres?sslmode=require"
#   .\run_supabase_apply_mapas_tables.ps1
#
# Opción sin Python: Supabase Dashboard → SQL Editor → pegar contenido de:
#   catastro/sql/mapas_simafi_supabase.sql

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$sql = Join-Path $PSScriptRoot "catastro\sql\mapas_simafi_supabase.sql"
$pyScript = Join-Path $PSScriptRoot "catastro\scripts\apply_mapas_sql.py"

if (-not (Test-Path $sql)) {
    Write-Error "No se encuentra $sql"
    exit 1
}
if (-not (Test-Path $pyScript)) {
    Write-Error "No se encuentra $pyScript"
    exit 1
}

$venvPython = Join-Path (Split-Path $PSScriptRoot -Parent) "venv\Scripts\python.exe"
$py = "python"
if (Test-Path $venvPython) { $py = $venvPython }

function Test-EnvNonEmpty([string]$Name) {
    $v = [Environment]::GetEnvironmentVariable($Name)
    return ($null -ne $v -and $v.Trim() -ne "")
}
$urlSet =
    (Test-EnvNonEmpty "DATABASE_URL") -or
    (Test-EnvNonEmpty "DIRECT_URL") -or
    (Test-EnvNonEmpty "DJANGO_DATABASE_URL") -or
    (Test-EnvNonEmpty "SUPABASE_DATABASE_URL")

Write-Host ""
Write-Host "Tablas Mapas Simafi — aplicar SQL en PostgreSQL/Supabase" -ForegroundColor Cyan
Write-Host "  SQL: $sql" -ForegroundColor Gray
Write-Host ""

if (-not $urlSet) {
    # Usar comillas simples: en comillas dobles "(ni ..." puede ejecutar el alias ni = New-Item.
    Write-Host 'No hay DATABASE_URL ni DIRECT_URL (u otras URLs de BD) en el entorno.' -ForegroundColor Yellow
    Write-Host 'Define por ejemplo: $env:DATABASE_URL = "postgresql://..."' -ForegroundColor Yellow
    Write-Host ""
}

if ($urlSet) {
    Write-Host "Ejecutando con: $py" -ForegroundColor Green
    & $py $pyScript
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    exit 0
}

Write-Host "Sin URL: opciones manuales —" -ForegroundColor Yellow
Write-Host "  A) Supabase → SQL Editor → pegar el contenido del archivo .sql y Run" -ForegroundColor White
Write-Host "  B) Instalar cliente Postgres y usar psql (opcional)" -ForegroundColor White
Write-Host ""

$open = Read-Host "¿Abrir el archivo SQL en el editor? (s/N)"
if ($open -eq "s" -or $open -eq "S") {
    Invoke-Item $sql
}
