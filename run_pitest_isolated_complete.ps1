# ====================================================================
# AUTOMATIZACIÓN: PRUEBAS UNITARIAS (IA + Manual)
# Ejecuta todas las clases de pruebas unitarias con métricas
# Genera UN CSV SEPARADO para cada clase de prueba
# ====================================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🧪 AUTOMATIZACIÓN: PRUEBAS UNITARIAS (IA + Manual)          ║" -ForegroundColor Cyan
Write-Host "║  Tiempo de ejecución + Cobertura JaCoCo                      ║" -ForegroundColor Cyan
Write-Host "║  📁 Un archivo CSV por clase de prueba                       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# ================================
# CONFIGURACIÓN
# ================================
$Iteraciones = 1  # 10 iteraciones por clase de prueba
$OutputDir = "unit_tests_metrics"  # Directorio para guardar CSVs

# Rutas donde buscar pruebas unitarias
$TestPaths = @(
    "src/test/java/org/springframework/samples/petclinic/experimental/ia/unitariasDIFFBLUECOVER",
    "src/test/java/org/springframework/samples/petclinic/experimental/manual/unitarias"
)

Write-Host ""
Write-Host "⚠️  NOTA: Este proceso recopila tiempo + cobertura JaCoCo" -ForegroundColor Yellow

# Crear carpeta para almacenar reportes
$reportDir = $OutputDir
if (-not (Test-Path $reportDir)) {
    New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
}

# ================================
# FUNCIÓN: Extraer nombre de clase Java desde archivo .java
# ================================
function Get-JavaClassName {
    param([string]$FilePath)
    
    $content = Get-Content $FilePath
    
    # Extraer package
    $packageLine = $content | Where-Object { $_ -match "^package\s+(.+);" } | Select-Object -First 1
    $package = if ($packageLine -match "^package\s+(.+);") { $matches[1] } else { "" }
    
    # Extraer nombre de clase CORRECTAMENTE (busca "class NombreClase" no el nombre del archivo)
    $classLine = $content | Where-Object { $_ -match "^\s*(public\s+)?(abstract\s+)?class\s+(\w+)" } | Select-Object -First 1
    $className = if ($classLine -match "class\s+(\w+)") { $matches[1] } else { [System.IO.Path]::GetFileNameWithoutExtension($FilePath) }
    
    if ($package) {
        return "$package.$className"
    } else {
        return $className
    }
}

# ================================
# FUNCIÓN: Extraer cobertura de jacoco.xml
# ================================
function Get-JaCoCoMetrics {
    param([string]$JaCoCoFile)
    
    if (-not (Test-Path $JaCoCoFile)) {
        return @{ instrPct = 0; branchPct = 0 }
    }
    
    $xml = [xml](Get-Content $JaCoCoFile)
    
    $instr = $xml.report.counter | Where-Object { $_.type -eq "INSTRUCTION" }
    $branch = $xml.report.counter | Where-Object { $_.type -eq "BRANCH" }
    
    $instrTotal = [int]$instr.covered + [int]$instr.missed
    $branchTotal = [int]$branch.covered + [int]$branch.missed
    
    $instrPct = if ($instrTotal -gt 0) { [math]::Round(100 * [int]$instr.covered / $instrTotal, 2) } else { 0 }
    $branchPct = if ($branchTotal -gt 0) { [math]::Round(100 * [int]$branch.covered / $branchTotal, 2) } else { 0 }
    
    return @{ instrPct = $instrPct; branchPct = $branchPct }
}

# ================================
# FUNCIÓN: Extraer mutation score de PITest
# ================================
function Get-MutationMetrics {
    param([string]$FullClassName, [string]$SimpleClassName, [string]$Group)
    
    # Buscar archivo mutations.xml más reciente de PITest
    $mutationsFile = Get-ChildItem "target/pit-reports" -Filter "mutations.xml" -Recurse -ErrorAction SilentlyContinue | 
        Sort-Object -Property LastWriteTime -Descending | 
        Select-Object -First 1 -ExpandProperty FullName
    
    if (-not $mutationsFile -or -not (Test-Path $mutationsFile)) {
        return @{ totalMutations = 0; killedMutations = 0; mutationScore = 0 }
    }
    
    try {
        $xml = [xml](Get-Content $mutationsFile)
        $allMutations = $xml.mutations.mutation
        
        if (-not $allMutations) {
            return @{ totalMutations = 0; killedMutations = 0; mutationScore = 0 }
        }
        
        # Convertir a array si es necesario
        if (-not ($allMutations -is [array])) {
            $allMutations = @($allMutations)
        }
        
        # Filtrar mutaciones por si fueron ejecutadas por este test
        # El killingTest contiene el nombre de la clase que mató la mutación
        $mutations = $allMutations | 
            Where-Object { 
                $killingTest = $_.killingTest
                # Si no fue matada pero tiene coverage, contar como totalMutation
                ($killingTest -like "*$SimpleClassName*") -or 
                ($killingTest -eq "")
            }
        
        if (-not $mutations) {
            return @{ totalMutations = 0; killedMutations = 0; mutationScore = 0 }
        }
        
        # Asegurar que es array
        if (-not ($mutations -is [array])) {
            $mutations = @($mutations)
        }
        
        $totalMutations = $mutations.Count
        $killedMutations = @($mutations | Where-Object { $_.detected -eq "true" -and $_.killingTest -like "*$SimpleClassName*" }).Count
        $mutationScore = if ($totalMutations -gt 0) { [math]::Round(100 * $killedMutations / $totalMutations, 2) } else { 0 }
        
        return @{ 
            totalMutations = $totalMutations
            killedMutations = $killedMutations
            mutationScore = $mutationScore 
        }
    } catch {
        return @{ totalMutations = 0; killedMutations = 0; mutationScore = 0 }
    }
}

# ================================
# PASO 1: COMPILACIÓN
# ================================
Write-Host ""
Write-Host "🛠️  PASO 1: Compilando proyecto..." -ForegroundColor Yellow
./mvnw clean compile test-compile -q

# ================================
# PASO 2: DESCUBRIR CLASES DE PRUEBA UNITARIAS
# ================================
Write-Host "🔍 PASO 2: Detectando clases de pruebas unitarias..." -ForegroundColor Yellow

$testClasses = @()

foreach ($testPath in $TestPaths) {
    if (Test-Path $testPath) {
        # Excluir archivos en carpetas "model" y archivos sin patrón de prueba
        $javaFiles = Get-ChildItem -Path $testPath -Filter "*.java" -Recurse | 
            Where-Object { 
                $_.FullName -notmatch "\\model\\" -and 
                ($_.Name -like "*Test*" -or $_.Name -like "*Diffblue*")
            }
        
        foreach ($file in $javaFiles) {
            $className = Get-JavaClassName -FilePath $file.FullName
            $testClasses += @{
                FullPath = $file.FullName
                ClassName = $className
                Group = if ($testPath -like "*unitariasDIFFBLUECOVER*") { "IA" } else { "Manual" }
            }
        }
    }
}

if ($testClasses.Count -eq 0) {
    Write-Host "❌ No se encontraron archivos de prueba en las rutas especificadas" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Se encontraron $($testClasses.Count) clases de prueba unitaria:" -ForegroundColor Green
foreach ($testClass in $testClasses) {
    Write-Host "   • $($testClass.ClassName) [$($testClass.Group)]" -ForegroundColor Cyan
}

# ================================
# PASO 3: GENERAR MUTACIONES CON PITEST
# ================================
Write-Host ""
Write-Host "🧬 PASO 3: Generando mutaciones con PITest para TODAS las pruebas..." -ForegroundColor Yellow

# Ejecutar PITest UNA SOLA VEZ para todas las pruebas unitarias
# Esto genera mutations.xml con las mutaciones detectadas por IA y Manual
./mvnw test-compile pitest:mutationCoverage `
    -DtargetClasses="org.springframework.samples.petclinic.owner.*" `
    -DtargetTests="*Test,*Diffblue*" `
    -DoutputFormats=XML `
    -q 2>&1 | Out-Null

Write-Host "   ✅ Mutaciones generadas" -ForegroundColor Green

# ================================
# PASO 4: WARM-UP GLOBAL (3 ejecuciones)
# ================================
Write-Host ""
Write-Host "🔥 PASO 4: Warm-up global (3 ejecuciones de todas las pruebas)..." -ForegroundColor Yellow
for ($w = 1; $w -le 3; $w++) {
    Write-Host "   Warm-up $w/3..." -NoNewline -ForegroundColor Gray
    foreach ($testClass in $testClasses) {
        ./mvnw -q test -Dtest="$($testClass.ClassName)" 2>&1 | Out-Null
    }
    Write-Host " ✅" -ForegroundColor Green
}

# ================================
# PASO 5: CREAR DIRECTORIO Y ARCHIVOS CSV
# ================================
Write-Host ""
Write-Host "📝 PASO 5: Preparando archivos CSV..." -ForegroundColor Yellow

# Crear directorio de salida
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}
Write-Host "   Directorio: $OutputDir" -ForegroundColor Cyan

# Crear un CSV para cada clase de prueba
$csvFiles = @{}
foreach ($testClass in $testClasses) {
    $className = $testClass.ClassName
    $classSimpleName = $className.Split('.')[-1]
    $group = $testClass.Group
    $csvFile = "$OutputDir/$($group)_$classSimpleName.csv"
    
    # Crear cabecera del CSV con columnas de mutation score
    "test_class,group,test_name,iteration,time_seconds,instr_pct,branch_pct,total_mutations,mutations_killed,mutation_score" | 
        Out-File -Encoding UTF8 $csvFile
    
    $csvFiles[$className] = $csvFile
    Write-Host "   ✅ $($group)_$classSimpleName.csv" -ForegroundColor Green
}

# ================================
# PASO 6: EJECUCIONES MEDIDAS CON RECOLECCIÓN DE MÉTRICAS
# ================================
Write-Host ""
Write-Host "⏱️  PASO 6: Ejecutando mediciones ($Iteraciones iteraciones por clase)..." -ForegroundColor Yellow
Write-Host ""

$totalTests = $testClasses.Count * $Iteraciones
$testCounter = 0

foreach ($testClass in $testClasses) {
    $className = $testClass.ClassName
    $classSimpleName = $className.Split('.')[-1]
    $group = $testClass.Group
    $csvFile = $csvFiles[$className]
    
    Write-Host "🧪 $classSimpleName [$group]" -ForegroundColor Magenta
    
    for ($iter = 1; $iter -le $Iteraciones; $iter++) {
        $testCounter++
        Write-Host "   Iteración $iter/$Iteraciones..." -NoNewline -ForegroundColor Gray
        
        # Ejecutar test
        ./mvnw -q test -Dtest="$className" 2>&1 | Out-Null
        
        # Generar reporte JaCoCo
        ./mvnw -q jacoco:report 2>&1 | Out-Null
        
        # Extraer cobertura JaCoCo
        $jacocoMetrics = Get-JaCoCoMetrics "target/site/jacoco/jacoco.xml"
        $instrPct = $jacocoMetrics.instrPct
        $branchPct = $jacocoMetrics.branchPct
        
        # Extraer mutation metrics (del reporte generado en PASO 3)
        $mutationMetrics = Get-MutationMetrics -FullClassName $className -SimpleClassName $classSimpleName -Group $group
        $totalMutations = $mutationMetrics.totalMutations
        $killedMutations = $mutationMetrics.killedMutations
        $mutationScore = $mutationMetrics.mutationScore
        
        # Buscar tiempos de prueba desde Surefire
        # Primero intentar con el nombre exacto de la clase
        $surefireFile = "target/surefire-reports/TEST-$className.xml"
        
        # Si no existe, buscar cualquier archivo Surefire que contenga el nombre simple de la clase
        if (-not (Test-Path $surefireFile)) {
            $surefireFile = Get-ChildItem "target/surefire-reports" -Filter "*$classSimpleName*" -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
        }
        
        if ($surefireFile -and (Test-Path $surefireFile)) {
            $surefire = [xml](Get-Content $surefireFile)
            
            foreach ($testcase in $surefire.testsuite.testcase) {
                $testName = $testcase.name
                $time = $testcase.time
                
                "$classSimpleName,$group,$testName,$iter,$time,$instrPct,$branchPct,$totalMutations,$killedMutations,$mutationScore" |
                    Out-File -Encoding UTF8 -Append $csvFile
            }
        }
        
        Write-Host " ✅ (Instr: $instrPct% | Branch: $branchPct% | Mutations: $mutationScore%)" -ForegroundColor Green
    }
    
    Write-Host ""
}

# ================================
# PASO 7: RESUMEN FINAL
# ================================
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                  ✅ EJECUCIÓN COMPLETADA                       ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host ""
Write-Host "📊 RESULTADOS:" -ForegroundColor Green
Write-Host "   Total iteraciones completadas: $testCounter" -ForegroundColor Cyan
Write-Host "   Directorio de salida: $OutputDir" -ForegroundColor Cyan

Write-Host ""
Write-Host "📁 ARCHIVOS CSV GENERADOS:" -ForegroundColor Green
$csvFiles.GetEnumerator() | ForEach-Object {
    $file = $_.Value
    if (Test-Path $file) {
        $lines = @(Get-Content $file).Count
        $csvFileName = Split-Path $file -Leaf
        Write-Host "   ✅ $csvFileName ($lines registros)" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "📄 VISTA PREVIA DE ARCHIVOS:" -ForegroundColor Green
$csvFiles.GetEnumerator() | ForEach-Object {
    $file = $_.Value
    if (Test-Path $file) {
        $csvFileName = Split-Path $file -Leaf
        Write-Host ""
        Write-Host "   $($csvFileName):" -ForegroundColor Yellow
        Get-Content $file | Select-Object -First 4 | ForEach-Object { 
            Write-Host "      $_" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "💡 PRÓXIMOS PASOS:" -ForegroundColor Yellow
Write-Host "   1. Abre los archivos CSV en Excel o Python para análisis" -ForegroundColor Gray
Write-Host "   2. Compara tiempo_ejecución entre IA y Manual" -ForegroundColor Gray
Write-Host "   3. Compara cobertura (instr_pct, branch_pct)" -ForegroundColor Gray
Write-Host "   4. Los archivos están organizados en: $OutputDir/" -ForegroundColor Gray

Write-Host ""

