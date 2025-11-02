# ================================
# CONFIGURACIÓN INICIAL
# ================================
$TestClass   = "org.springframework.samples.petclinic.owner.ProcessCreationFormManualTest"
$Iteraciones = 10
$OutputCsv   = "metrics_$($TestClass.Split('.')[-1]).csv"

# Crear cabecera CSV (ya extendido)
"test_name,iteration,time_seconds,instr_covered,instr_total,instr_pct,branch_covered,branch_total,branch_pct" | Out-File -Encoding UTF8 $OutputCsv

# ================================
# 1) CLEAN + COMPILACIÓN
# ================================
Write-Host "🛠 Compilando proyecto sin tests..."
./mvnw clean compile -DskipTests

# ================================
# 2) WARM-UP
# ================================
Write-Host "🔥 Warm-up..."
for ($i=1; $i -le 3; $i++) {
    ./mvnw -q test -Dtest="$TestClass"
}

# ================================
# 3) EJECUCIONES MEDIDAS
# ================================
Write-Host "⏱ Ejecutando mediciones reales..."
for ($i=1; $i -le $Iteraciones; $i++) {

    # Ejecutar el test específico
    ./mvnw -q test -Dtest="$TestClass"

    # Generar reporte de cobertura JaCoCo
    ./mvnw -q jacoco:report

    # Leer cobertura desde jacoco.xml
    $jacocoFile = "target/site/jacoco/jacoco.xml"
    if (Test-Path $jacocoFile) {
        $jacocoXml = [xml](Get-Content $jacocoFile)

        # Obtener contadores globales de instrucciones y branches
        $instr = $jacocoXml.report.counter | Where-Object { $_.type -eq "INSTRUCTION" }
        $branch = $jacocoXml.report.counter | Where-Object { $_.type -eq "BRANCH" }

        $instrMissed  = [int]$instr.missed
        $instrCovered = [int]$instr.covered
        $instrTotal   = $instrMissed + $instrCovered
        $instrPct     = if ($instrTotal -ne 0) { [math]::Round(($instrCovered / $instrTotal) * 100, 2) } else { 0 }

        $branchMissed  = [int]$branch.missed
        $branchCovered = [int]$branch.covered
        $branchTotal   = $branchMissed + $branchCovered
        $branchPct     = if ($branchTotal -ne 0) { [math]::Round(($branchCovered / $branchTotal) * 100, 2) } else { 0 }
    }

    # Buscar el XML generado por Surefire (tiempos de prueba)
    $report = Get-ChildItem -Path "target/surefire-reports" -Filter "TEST-$TestClass.xml" -Recurse -ErrorAction SilentlyContinue

    if ($report) {
        $xmlContent = [xml](Get-Content $report.FullName)

        foreach ($testcase in $xmlContent.testsuite.testcase) {
            $name = $testcase.name
            $time = $testcase.time

            "$name,$i,$time,$instrCovered,$instrTotal,$instrPct,$branchCovered,$branchTotal,$branchPct" |
                Out-File -Encoding UTF8 -Append $OutputCsv
        }
    }

    Write-Host "✅ Iteración $i finalizada"
}

Write-Host "📁 Archivo CSV generado en: $OutputCsv"
