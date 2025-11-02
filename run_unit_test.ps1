# =========================================
# CONFIGURACIÓN
# =========================================
$TestClass   = "org.springframework.samples.petclinic.owner.OwnerAddPetDiffblueTest"
$Iteraciones = 5
$OutputCsv   = "unit_metrics_with_pitest_$($TestClass.Split('.')[-1]).csv"

"test_name,iteration,time_seconds,instr_pct,branch_pct,mut_killed,mut_total,mut_score" | Out-File $OutputCsv -Encoding UTF8

./mvnw clean compile -DskipTests -q

Write-Host "🔥 Warm-up..."
for ($i=1; $i -le 2; $i++) {
    ./mvnw -q test -Dtest="$TestClass"
}

Write-Host "⏱ Iniciando mediciones..."
for ($i=1; $i -le $Iteraciones; $i++) {

    Write-Host "  Iteración $i..." -NoNewline -ForegroundColor Yellow

    ./mvnw -q test -Dtest="$TestClass" 2>&1 | Out-Null

    $sureFilePattern = Get-ChildItem "target/surefire-reports" -Filter "TEST-$TestClass.xml" -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $sureFilePattern) {
        Write-Host " ⚠️  No test results"
        continue
    }
    
    $xmlSurefire = [xml](Get-Content $sureFilePattern.FullName)
    
    ./mvnw -q jacoco:report 2>&1 | Out-Null
    
    $jacocoFile = "target/site/jacoco/jacoco.xml"
    if (-not (Test-Path $jacocoFile)) {
        Write-Host " ⚠️  No JaCoCo"
        continue
    }
    
    $jacocoXml = [xml](Get-Content $jacocoFile)

    $instr = $jacocoXml.report.counter | Where-Object { $_.type -eq "INSTRUCTION" }
    $branch = $jacocoXml.report.counter | Where-Object { $_.type -eq "BRANCH" }
    
    if ($instr -and $branch) {
        $instrPct = [math]::Round(100 * $instr.covered / ($instr.covered + $instr.missed), 2)
        $branchPct = [math]::Round(100 * $branch.covered / ($branch.covered + $branch.missed), 2)
    } else {
        $instrPct = 0
        $branchPct = 0
    }

    # Ejecutar PITest
    $pitResult = ./mvnw test-compile pitest:mutationCoverage `
          -Dtest="$TestClass" `
          -Dmutators=DEFAULTS `
          -DoutputFormats=XML -q 2>&1

    $pitestXml = Get-ChildItem "target/pit-reports" -Filter "mutations.xml" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    
    $mutKilled = 0
    $mutTotal  = 0
    $mutScore  = 0

    if ($pitestXml) {
        try {
            $xmlMut = [xml](Get-Content $pitestXml.FullName)
            $mutKilled = ($xmlMut.mutations.mutation | Where-Object { $_.detected -eq "true" }).Count
            $mutTotal  = ($xmlMut.mutations.mutation | Measure-Object).Count
            $mutScore  = if ($mutTotal -gt 0) { [math]::Round(100 * $mutKilled / $mutTotal, 2) } else { 0 }
        }
        catch {
            # Error silencioso
        }
    }

    foreach ($testcase in $xmlSurefire.testsuite.testcase) {
        $testName = $testcase.name
        $time = $testcase.time
        "$testName,$i,$time,$instrPct,$branchPct,$mutKilled,$mutTotal,$mutScore" | Out-File -Append -Encoding UTF8 $OutputCsv
    }

    Write-Host " ✅ (Jac: $instrPct% | Mut: $mutKilled/$mutTotal)" -ForegroundColor Green
}

Write-Host ""
Write-Host "📁 CSV generado: $OutputCsv" -ForegroundColor Green
