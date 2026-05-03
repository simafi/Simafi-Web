# Aplica en Supabase/Postgres las tablas Mapas Simafi (catastro_mapa_*).
# Opción A (recomendada): Supabase → SQL Editor → abrir y ejecutar:
#   backend/catastro/sql/mapas_simafi_supabase.sql
#
# Opción B: desde esta carpeta backend/, si tienes psql en PATH y DATABASE_URL:
#   psql "$env:DATABASE_URL" -f catastro/sql/mapas_simafi_supabase.sql

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$sql = Join-Path $PSScriptRoot "catastro\sql\mapas_simafi_supabase.sql"
if (-not (Test-Path $sql)) {
    Write-Error "No se encuentra $sql"
    exit 1
}

Write-Host "Archivo SQL:" -ForegroundColor Cyan
Write-Host "  $sql" -ForegroundColor White
Write-Host ""
Write-Host "1) Copia el contenido en Supabase Dashboard → SQL Editor → Run" -ForegroundColor Yellow
Write-Host "2) O con psql (Git Bash / WSL / cliente Postgres):" -ForegroundColor Yellow
Write-Host '   psql "$env:DATABASE_URL" -f catastro/sql/mapas_simafi_supabase.sql' -ForegroundColor Gray
Write-Host ""

$open = Read-Host "¿Abrir el archivo en el editor predeterminado? (s/N)"
if ($open -eq "s" -or $open -eq "S") {
    Invoke-Item $sql
}
