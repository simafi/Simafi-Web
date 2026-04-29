@echo off
REM Script para ejecutar el proyecto Django Tributario
REM Aplicación renombrada de 'hola' a 'tributario_app'
set "REPO_ROOT=%~dp0"
REM Quitar la barra final si existe
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

REM Arranque definitivo en desarrollo:
REM - Usa Postgres LOCAL (no Supabase) para evitar conflictos de migraciones
REM - Aplica migraciones y levanta en 8010
REM Evitar errores "charmap" de encoding en Windows
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
powershell -ExecutionPolicy Bypass -File "%REPO_ROOT%\backend\run_local_postgres.ps1" -Port 8010
pause 