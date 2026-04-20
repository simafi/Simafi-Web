# Script de limpieza TOTAL de caché del navegador
# Versión: 3.0 - Limpieza agresiva

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LIMPIEZA TOTAL DE CACHÉ DEL NAVEGADOR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# PASO 1: Cerrar TODOS los navegadores
Write-Host "PASO 1: Cerrando todos los navegadores..." -ForegroundColor Yellow
Write-Host ""

$navegadores = @('chrome', 'msedge', 'firefox', 'brave', 'opera', 'iexplore')
foreach ($nav in $navegadores) {
    $procesos = Get-Process $nav -ErrorAction SilentlyContinue
    if ($procesos) {
        Write-Host "  → Cerrando $nav..." -ForegroundColor White
        Stop-Process -Name $nav -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "  ✅ Navegadores cerrados" -ForegroundColor Green
Write-Host ""
Write-Host "Esperando 5 segundos..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# PASO 2: Eliminar archivos de caché
Write-Host ""
Write-Host "PASO 2: Eliminando archivos de caché..." -ForegroundColor Yellow
Write-Host ""

# Chrome
$chromeCachePaths = @(
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Code Cache",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\GPUCache"
)

foreach ($path in $chromeCachePaths) {
    if (Test-Path $path) {
        Write-Host "  → Limpiando Chrome: $path" -ForegroundColor White
        Remove-Item -Path "$path\*" -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Edge
$edgeCachePaths = @(
    "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache",
    "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Code Cache",
    "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\GPUCache"
)

foreach ($path in $edgeCachePaths) {
    if (Test-Path $path) {
        Write-Host "  → Limpiando Edge: $path" -ForegroundColor White
        Remove-Item -Path "$path\*" -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "  ✅ Caché eliminado" -ForegroundColor Green

# PASO 3: Limpiar DNS y caché de red
Write-Host ""
Write-Host "PASO 3: Limpiando caché de DNS..." -ForegroundColor Yellow
ipconfig /flushdns | Out-Null
Write-Host "  ✅ DNS limpiado" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ LIMPIEZA COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "PRÓXIMOS PASOS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Espera 5 segundos más" -ForegroundColor White
Write-Host "2. Abre el navegador" -ForegroundColor White
Write-Host "3. Ve a: http://localhost:8080/tributario/maestro-negocios/" -ForegroundColor Green
Write-Host "4. Presiona F12 y verifica la consola" -ForegroundColor White
Write-Host ""
Write-Host "DEBE APARECER:" -ForegroundColor Yellow
Write-Host "  ✅ Template version: 3.0-FINAL" -ForegroundColor Green
Write-Host "  ✅ Override aplicado" -ForegroundColor Green
Write-Host "  🔥 OVERRIDE V3: Redirigiendo a: /tributario/declaraciones/" -ForegroundColor Green
Write-Host ""

Start-Sleep -Seconds 5
Write-Host "Listo para abrir el navegador." -ForegroundColor Green
Write-Host ""


























































