# Script para limpiar caché del navegador de forma agresiva
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LIMPIEZA AGRESIVA DE CACHÉ" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Matar procesos de navegadores
Write-Host "1. Cerrando todos los navegadores..." -ForegroundColor Yellow
Get-Process chrome,msedge,firefox,brave -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Limpiar caché de Chrome
$chromeCachePath = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache"
if (Test-Path $chromeCachePath) {
    Write-Host "2. Limpiando caché de Chrome..." -ForegroundColor Yellow
    Remove-Item -Path "$chromeCachePath\*" -Recurse -Force -ErrorAction SilentlyContinue
}

# Limpiar caché de Edge
$edgeCachePath = "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache"
if (Test-Path $edgeCachePath) {
    Write-Host "3. Limpiando caché de Edge..." -ForegroundColor Yellow
    Remove-Item -Path "$edgeCachePath\*" -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "✅ Caché limpiado completamente" -ForegroundColor Green
Write-Host ""
Write-Host "📌 PRÓXIMO PASO:" -ForegroundColor Cyan
Write-Host "   1. Espera 5 segundos"
Write-Host "   2. Abre el navegador"
Write-Host "   3. Accede a: http://localhost:8080/tributario/maestro-negocios/"
Write-Host ""
Write-Host "🔍 VERIFICACIÓN:" -ForegroundColor Cyan
Write-Host "   El título debe decir: 'Gestión de Negocios v2.0'"
Write-Host ""


























































