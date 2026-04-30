param(
  [switch]$ClearCache
)

$ErrorActionPreference = "Stop"

function Backup-And-RemoveFile([string]$Path, [string]$BackupDir) {
  if (-not (Test-Path $Path)) { return }
  New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
  $name = Split-Path $Path -Leaf
  $dest = Join-Path $BackupDir $name
  Copy-Item -Force $Path $dest
  Remove-Item -Force $Path
}

function Clear-ChromiumHttpsState([string]$BrowserName, [string]$UserDataDir) {
  $default = Join-Path $UserDataDir "Default"
  $network = Join-Path $default "Network"
  if (-not (Test-Path $network)) { return }

  $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
  $backupRoot = Join-Path $PSScriptRoot "..\\.browser-backups\\$BrowserName\\$stamp"
  # No usar Resolve-Path aquí: el directorio aún no existe.

  Write-Host "Cerrando procesos de $BrowserName si existen..." -ForegroundColor Cyan
  if ($BrowserName -eq "chrome") { Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue }
  if ($BrowserName -eq "edge") { Get-Process msedge -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue }

  Write-Host "Respaldando y limpiando HSTS/HTTPS state ($BrowserName)..." -ForegroundColor Cyan
  Backup-And-RemoveFile (Join-Path $network "TransportSecurity") $backupRoot
  Backup-And-RemoveFile (Join-Path $network "Network Persistent State") $backupRoot

  if ($ClearCache) {
    # Borrado "fuerte" de cache de red (puede cerrar sesiones).
    $cacheDir = Join-Path $network "Cache"
    $codeCacheDir = Join-Path $default "Code Cache"
    foreach ($d in @($cacheDir, $codeCacheDir)) {
      if (Test-Path $d) {
        Write-Host "Borrando cache: $d" -ForegroundColor Yellow
        Remove-Item -Recurse -Force $d
      }
    }
  }

  Write-Host "OK. Backup en: $backupRoot" -ForegroundColor Green
}

$chromeUserData = Join-Path $env:LOCALAPPDATA "Google\\Chrome\\User Data"
$edgeUserData = Join-Path $env:LOCALAPPDATA "Microsoft\\Edge\\User Data"

if (Test-Path $chromeUserData) { Clear-ChromiumHttpsState -BrowserName "chrome" -UserDataDir $chromeUserData }
if (Test-Path $edgeUserData) { Clear-ChromiumHttpsState -BrowserName "edge" -UserDataDir $edgeUserData }

Write-Host ""
Write-Host "Ahora abre: http://127.0.0.1:8010/ (IMPORTANTE: http, no https)" -ForegroundColor Green

