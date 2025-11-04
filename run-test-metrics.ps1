# ================================================================
# AUTOMATIZACIÓN: PRUEBAS FUNCIONALES (IA + Manual)
# Ejecuta todas las clases de pruebas funcionales con métricas
# ================================================================

# ================================
# CONFIGURACIÓN
# ================================
$Iteraciones = 10  # 10 iteraciones por clase de prueba
$OutputDir = "functional_tests_metrics"  # Directorio para guardar CSVs
$CoverageDir = "coverage_reports_functional"  # Directorio para guardar reportes JaCoCo individuales

# Rutas donde buscar pruebas funcionales
$TestPaths = @(
    "src/test/java/org/springframework/samples/petclinic/experimental/ia/funcionalesCHATGPT",
    "src/test/java/org/springframework/samples/petclinic/experimental/manual/funcionales"
)

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🧪 AUTOMATIZACIÓN: PRUEBAS FUNCIONALES (IA + Manual)         ║" -ForegroundColor Cyan
Write-Host "║  Tiempo de ejecución + Cobertura JaCoCo (por test individual) ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# Crear carpetas para almacenar reportes
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

if (-not (Test-Path $CoverageDir)) {
    New-Item -ItemType Directory -Path $CoverageDir -Force | Out-Null
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
    
    # Extraer nombre de clase
    $className = [System.IO.Path]::GetFileNameWithoutExtension($FilePath)
    
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
    
    try {
        $xml = [xml](Get-Content $JaCoCoFile -ErrorAction SilentlyContinue)
        
        if (-not $xml -or -not $xml.report) {
            return @{ instrPct = 0; branchPct = 0 }
        }
        
        $instr = $xml.report.counter | Where-Object { $_.type -eq "INSTRUCTION" } | Select-Object -First 1
        $branch = $xml.report.counter | Where-Object { $_.type -eq "BRANCH" } | Select-Object -First 1
        
        if (-not $instr -or -not $branch) {
            return @{ instrPct = 0; branchPct = 0 }
        }
        
        $instrTotal = [int]$instr.covered + [int]$instr.missed
        $branchTotal = [int]$branch.covered + [int]$branch.missed
        
        $instrPct = if ($instrTotal -gt 0) { [math]::Round(100 * [int]$instr.covered / $instrTotal, 2) } else { 0 }
        $branchPct = if ($branchTotal -gt 0) { [math]::Round(100 * [int]$branch.covered / $branchTotal, 2) } else { 0 }
        
        return @{ instrPct = $instrPct; branchPct = $branchPct }
    } catch {
        return @{ instrPct = 0; branchPct = 0 }
    }
}

# ================================
# PASO 1: CLEAN + COMPILACIÓN
# ================================
Write-Host ""
Write-Host "🛠️  PASO 1: Compilando proyecto..." -ForegroundColor Yellow
./mvnw clean compile -DskipTests -q

# ================================
# PASO 2: DESCUBRIR CLASES DE PRUEBA
# ================================
Write-Host "� PASO 2: Detectando clases de pruebas funcionales..." -ForegroundColor Yellow

$testClasses = @()

foreach ($testPath in $TestPaths) {
    if (Test-Path $testPath) {
        $javaFiles = Get-ChildItem -Path $testPath -Filter "*.java" -Recurse
        
        foreach ($file in $javaFiles) {
            $className = Get-JavaClassName $file.FullName
            $testClasses += @{
                FullPath = $file.FullName
                ClassName = $className
                Group = if ($testPath -like "*ia*") { "IA" } else { "Manual" }
            }
        }
    }
}

if ($testClasses.Count -eq 0) {
    Write-Host "❌ No se encontraron archivos de prueba en las rutas especificadas" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Se encontraron $($testClasses.Count) clases de prueba:" -ForegroundColor Green
foreach ($testClass in $testClasses) {
    Write-Host "   • $($testClass.ClassName) [$($testClass.Group)]" -ForegroundColor Cyan
}

# ================================
# PASO 3: WARM-UP
# ================================
Write-Host ""
Write-Host "🔥 PASO 3: Warm-up (3 ejecuciones)..." -ForegroundColor Yellow
for ($w = 1; $w -le 3; $w++) {
    Write-Host "   Warm-up $w/3..." -NoNewline -ForegroundColor Gray
    foreach ($testClass in $testClasses) {
        ./mvnw -q test -Dtest="$($testClass.ClassName)" 2>&1 | Out-Null
    }
    Write-Host " ✅" -ForegroundColor Green
}

# ================================
# PASO 4: CREAR DIRECTORIO Y ARCHIVOS CSV
# ================================
Write-Host ""
Write-Host "📝 PASO 4: Preparando archivos CSV..." -ForegroundColor Yellow

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
    
    # Crear cabecera del CSV
    "test_class,group,test_name,iteration,time_seconds,instr_pct,branch_pct" | 
        Out-File -Encoding UTF8 $csvFile
    
    $csvFiles[$className] = $csvFile
    Write-Host "   ✅ $($group)_$classSimpleName.csv" -ForegroundColor Green
}

# ================================
# PASO 5: EJECUCIONES MEDIDAS
# ================================
Write-Host ""
Write-Host "⏱️  PASO 5: Ejecutando mediciones ($Iteraciones iteraciones por clase)..." -ForegroundColor Yellow
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
        
        # IMPORTANTE: Limpiar archivos JaCoCo antes de la ejecución para capturar cobertura individual
        if (Test-Path "target/site/jacoco") {
            Remove-Item -Path "target/site/jacoco" -Recurse -Force -ErrorAction SilentlyContinue | Out-Null
        }
        $execFiles = Get-ChildItem "target" -Filter "*.exec" -ErrorAction SilentlyContinue
        if ($execFiles) {
            $execFiles | Remove-Item -Force -ErrorAction SilentlyContinue | Out-Null
        }
        
        # Ejecutar test
        ./mvnw -q test -Dtest="$className" 2>&1 | Out-Null
        
        # Generar reporte JaCoCo
        ./mvnw -q jacoco:report 2>&1 | Out-Null
        
        # Extraer cobertura
        $jacocoMetrics = Get-JaCoCoMetrics "target/site/jacoco/jacoco.xml"
        $instrPct = $jacocoMetrics.instrPct
        $branchPct = $jacocoMetrics.branchPct
        
        # NUEVO: Guardar reporte JaCoCo individual con nombre único
        $jacocoFileName = "$CoverageDir/$($group)_$classSimpleName-iter$iter-jacoco.xml"
        if (Test-Path "target/site/jacoco/jacoco.xml") {
            Copy-Item -Path "target/site/jacoco/jacoco.xml" -Destination $jacocoFileName -Force | Out-Null
        }
        
        # Buscar tiempos de prueba desde Surefire
        $surefireFile = "target/surefire-reports/TEST-$className.xml"
        if (Test-Path $surefireFile) {
            $surefire = [xml](Get-Content $surefireFile)
            
            foreach ($testcase in $surefire.testsuite.testcase) {
                $testName = $testcase.name
                $time = $testcase.time
                
                "$classSimpleName,$group,$testName,$iter,$time,$instrPct,$branchPct" |
                    Out-File -Encoding UTF8 -Append $csvFile
            }
        }
        
        Write-Host " ✅ (Jac: $instrPct% | Branch: $branchPct%)" -ForegroundColor Green
    }
    
    Write-Host ""
}

# ================================
# PASO 6: RESUMEN
# ================================
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                  ✅ EJECUCIÓN COMPLETADA                       ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host ""
Write-Host "📊 RESULTADOS:" -ForegroundColor Green
Write-Host "   Total iteraciones completadas: $testCounter" -ForegroundColor Cyan
Write-Host "   Directorio de salida: $OutputDir" -ForegroundColor Cyan
Write-Host "   Directorio de cobertura (JaCoCo): $CoverageDir" -ForegroundColor Cyan

# Contar archivos XML de cobertura generados
$jacocoXmlFiles = Get-ChildItem -Path $CoverageDir -Filter "*.xml" -ErrorAction SilentlyContinue
$jacocoXmlCount = if ($jacocoXmlFiles) { @($jacocoXmlFiles).Count } else { 0 }
Write-Host "   Reportes JaCoCo individuales: $jacocoXmlCount archivos XML" -ForegroundColor Cyan

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
