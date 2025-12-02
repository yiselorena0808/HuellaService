# Script de diagnóstico para el problema WinError 216
Write-Host "=== DIAGNÓSTICO DEL SISTEMA Y EJECUTABLE ===" -ForegroundColor Cyan

# 1. Verificar arquitectura de Windows
Write-Host "`n1. Arquitectura del Sistema Operativo:" -ForegroundColor Yellow
$osArch = Get-CimInstance Win32_OperatingSystem | Select-Object -ExpandProperty OSArchitecture
$is64bit = [Environment]::Is64BitOperatingSystem
Write-Host "Arquitectura: $osArch"
Write-Host "Es 64-bit: $is64bit"

# 2. Verificar si capturar.exe existe
Write-Host "`n2. Estado del archivo capturar.exe:" -ForegroundColor Yellow
$exePath = ".\capturar.exe"
if (Test-Path $exePath) {
    Write-Host "✓ capturar.exe encontrado"
    $fileInfo = Get-Item $exePath
    Write-Host "Tamaño: $($fileInfo.Length) bytes"
    Write-Host "Fecha creación: $($fileInfo.CreationTime)"
} else {
    Write-Host "✗ capturar.exe NO ENCONTRADO"
    exit 1
}

# 3. Intentar ejecutar el exe y capturar error detallado
Write-Host "`n3. Intentando ejecutar capturar.exe:" -ForegroundColor Yellow
try {
    & ".\capturar.exe" 2>&1
    Write-Host "✓ Ejecutable completó sin errores" -ForegroundColor Green
} catch {
    Write-Host "✗ Error al ejecutar: $($_.Exception.Message)" -ForegroundColor Red
}

# 4. Verificar permisos y atributos del archivo
Write-Host "`n4. Permisos del archivo:" -ForegroundColor Yellow
$acl = Get-Acl $exePath
Write-Host "Propietario: $($acl.Owner)"
Write-Host "Acceso:" 
$acl.Access | ForEach-Object { Write-Host "  - $($_.IdentityReference): $($_.FileSystemRights)" }

# 5. Verificar si es de 32-bit o 64-bit (usando información del ejecutable)
Write-Host "`n5. Análisis del ejecutable:" -ForegroundColor Yellow
$bytes = Get-Content $exePath -Encoding Byte -TotalCount 4
$hexSignature = [BitConverter]::ToString($bytes, 0)
Write-Host "Firma del archivo: $hexSignature (primeros 4 bytes)"
if ($bytes[0] -eq 0x4D -and $bytes[1] -eq 0x5A) {
    Write-Host "✓ Es un ejecutable Windows PE válido (empieza con MZ)"
} else {
    Write-Host "✗ NO es un ejecutable PE válido"
}

# 6. Verificar si hay versión de 32-bit o 64-bit
Write-Host "`n6. Intentando análisis de arquitectura:" -ForegroundColor Yellow
Write-Host "Nota: Para análisis más profundo, necesitarías 'dumpbin' (Visual Studio) o 'sigcheck' (Sysinternals)"
Write-Host "Descarga sigcheck desde: https://learn.microsoft.com/en-us/sysinternals/downloads/sigcheck"

# 7. Verificar dispositivos USB y biométricos
Write-Host "`n7. Dispositivos conectados (USB):" -ForegroundColor Yellow
Get-PnpDevice -Class USB | Where-Object { $_.Status -eq "OK" } | ForEach-Object {
    Write-Host "  - $($_.Name)"
}

Write-Host "`n8. Dispositivos biométricos (si están registrados):" -ForegroundColor Yellow
Get-PnpDevice -PresentOnly | Where-Object { $_.Name -like "*finger*" -or $_.Name -like "*biometric*" -or $_.Name -like "*Bio*" } | ForEach-Object {
    Write-Host "  - $($_.Name) (Estado: $($_.Status))"
}

Write-Host "`n=== FIN DEL DIAGNÓSTICO ===" -ForegroundColor Cyan
Write-Host "Si el problema persiste, comparte los resultados de este script." -ForegroundColor Green
