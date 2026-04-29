# Script para ejecutar el proyecto Django Tributario
# Aplicación renombrada de 'hola' a 'tributario_app'
$ErrorActionPreference = "Stop"

$repoRoot = $PSScriptRoot
$backendDir = Join-Path $repoRoot "backend"

# Evitar errores "charmap" en Windows al imprimir tildes/íconos
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

# Arranque definitivo en desarrollo:
# - Usa Postgres LOCAL (no Supabase) para evitar conflictos de migraciones
# - Aplica migraciones y levanta en 8010
$localPg = Join-Path $backendDir "run_local_postgres.ps1"
& $localPg -Port 8010