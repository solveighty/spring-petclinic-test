# ====================================================================
# SCRIPT MAESTRO SIMPLE: Ejecutar Ambos Scripts Secuencialmente
# Versión Simplificada (sin logging avanzado)
# ====================================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚀 EJECUCIÓN SECUENCIAL: UNITARIAS → FUNCIONALES              ║" -ForegroundColor Cyan
Write-Host "║                                                                  ║" -ForegroundColor Cyan
Write-Host "║  📊 Pruebas Unitarias (IA + Manual)                            ║" -ForegroundColor Cyan
Write-Host "║  📊 Pruebas Funcionales (IA + Manual)                          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# ================================
# VALIDAR SCRIPTS
# ================================
Write-Host ""
Write-Host "🔍 Validando scripts..." -ForegroundColor Yellow

if (-not (Test-Path ".\run_pitest_isolated_complete.ps1")) {
    Write-Host "❌ ERROR: No se encuentra run_pitest_isolated_complete.ps1" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".\run-test-metrics.ps1")) {
    Write-Host "❌ ERROR: No se encuentra run-test-metrics.ps1" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Ambos scripts encontrados" -ForegroundColor Green

# ================================
# CONFIRMACIÓN
# ================================
Write-Host ""
Write-Host "⚠️  INFORMACIÓN:" -ForegroundColor Yellow
Write-Host "   1. Se ejecutarán PRUEBAS UNITARIAS (puede tomar 12-18 horas)" -ForegroundColor Yellow
Write-Host "   2. Luego PRUEBAS FUNCIONALES (puede tomar 24-30 horas)" -ForegroundColor Yellow
Write-Host "   3. TIEMPO TOTAL ESTIMADO: 36-48 HORAS" -ForegroundColor Yellow
Write-Host ""

$response = Read-Host "¿Continuar? (s/n)"
if ($response -ne "s") {
    Write-Host "Cancelado." -ForegroundColor Yellow
    exit 0
}

# ================================
# FASE 1: UNITARIAS
# ================================
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "FASE 1: EJECUTANDO PRUEBAS UNITARIAS" -ForegroundColor Cyan
Write-Host "Inicio: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$time1 = Measure-Command {
    & ".\run_pitest_isolated_complete.ps1"
}

Write-Host ""
Write-Host "✅ FASE 1 completada en: $($time1.TotalHours) horas" -ForegroundColor Green

# ================================
# PAUSA
# ================================
Write-Host ""
Write-Host "⏸️  Pausa de 1 minuto antes de FASE 2..." -ForegroundColor Gray
Start-Sleep -Seconds 60

# ================================
# FASE 2: FUNCIONALES
# ================================
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "FASE 2: EJECUTANDO PRUEBAS FUNCIONALES" -ForegroundColor Cyan
Write-Host "Inicio: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$time2 = Measure-Command {
    & ".\run-test-metrics.ps1"
}

Write-Host ""
Write-Host "✅ FASE 2 completada en: $($time2.TotalHours) horas" -ForegroundColor Green

# ================================
# RESUMEN
# ================================
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "🎉 ¡EJECUCIÓN COMPLETADA!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Green

$totalTime = $time1 + $time2
Write-Host ""
Write-Host "⏱️  Tiempos:" -ForegroundColor Cyan
Write-Host "   FASE 1 (Unitarias):   $($time1.TotalHours.ToString("F2")) horas" -ForegroundColor Gray
Write-Host "   FASE 2 (Funcionales): $($time2.TotalHours.ToString("F2")) horas" -ForegroundColor Gray
Write-Host "   TOTAL:                $($totalTime.TotalHours.ToString("F2")) horas" -ForegroundColor Cyan

Write-Host ""
Write-Host "📁 Archivos generados:" -ForegroundColor Cyan
Write-Host "   ✅ unit_tests_metrics/*.csv" -ForegroundColor Green
Write-Host "   ✅ functional_tests_metrics/*.csv" -ForegroundColor Green
Write-Host "   ✅ coverage_reports/*.xml" -ForegroundColor Green

Write-Host ""
