# Comparative Study: AI-Generated vs Manual Tests in Spring PetClinic

[![Build Status](https://github.com/solveighty/spring-petclinic-test/actions/workflows/maven-build.yml/badge.svg)](https://github.com/solveighty/spring-petclinic-test/actions/workflows/maven-build.yml)[![Build Status](https://github.com/solveighty/spring-petclinic-test/actions/workflows/gradle-build.yml/badge.svg)](https://github.com/solveighty/spring-petclinic-test/actions/workflows/gradle-build.yml)

## About This Fork: IA-Generated Tests vs Manual Tests Study

This is a research fork of Spring PetClinic used to conduct a **comparative study of IA-generated tests (DiffBlue, ChatGPT) vs manually written tests** in terms of code coverage, mutation testing effectiveness, and test execution performance.

**Study Objective:** Evaluate the effectiveness of IA tools in automatically generating test cases across unit tests (Unitarias) and functional tests (Funcionales) for a real-world Spring Boot application.

**Research Output:** Complete statistical analysis report available in `analisis/reports/Comparative_Study_AI_vs_Manual_Tests.pdf`

### Directory Structure for Results and Tests

```
spring-petclinic/
├── analisis/
│   ├── data/                                     # Raw experimental data
│   ├── experimental/                             # Experimental configurations and logs
│   ├── figures/                                  # Generated plots and visualizations
│   ├── numerical_data/                           # Processed statistical data
│   ├── reports/
│   │   ├── Comparative_Study_AI_vs_Manual_Tests.pdf   # Main statistical report
│   │   └── Supplementary_Technical_Record.pdf             # Supplementary technical record
│   ├── scripts/                                  # Analysis and processing scripts
│   ├── unit_tests_metrics/                        # Unit test CSV results
│   │   ├── DiffBlue_metrics_*.csv                # IA-generated tests metrics
│   │   └── Manual_metrics_*.csv                  # Manual tests metrics
│   └── functional_tests_metrics/                 # Functional test CSV results
│       ├── ChatGPT_metrics_*.csv                 # IA-generated tests metrics
│       └── Manual_metrics_*.csv                  # Manual tests metrics
├── coverage_reports/                             # JaCoCo coverage reports (unit tests)
├── coverage_reports_functional/                  # JaCoCo coverage reports (functional tests)
├── src/test/java/org/springframework/samples/petclinic/experimental/
│   ├── ia/
│   │   ├── unitariasDIFFBLUECOVER/               # DiffBlue IA-generated unit tests
│   │   │   └── [Test classes covering business logic]
│   │   └── funcionalesCHATGPT/                   # ChatGPT IA-generated functional tests
│   │       └── [Integration and E2E test classes]
│   └── manual/
│       ├── unitarias/                            # Hand-written unit tests
│       │   └── [Test classes covering business logic]
│       └── funcionales/                          # Hand-written functional tests
│           └── [Integration and E2E test classes]
├── run_pitest_isolated_complete.ps1             # Unit tests execution script
├── run-test-metrics.ps1                         # Functional tests execution script
└── run_all_metrics_simple.ps1                   # Master orchestrator script
```

#### Test Structure Details

**IA-Generated Unit Tests (DiffBlue):**
- Location: `src/test/java/org/springframework/samples/petclinic/experimental/ia/unitariasDIFFBLUECOVER/`
- Purpose: Automatically generated unit tests using DiffBlue Core
- Test Coverage: Business logic, services, repositories
- Metrics: Instruction coverage, branch coverage, mutation score

**IA-Generated Functional Tests (ChatGPT):**
- Location: `src/test/java/org/springframework/samples/petclinic/experimental/ia/funcionalesCHATGPT/`
- Purpose: Integration and E2E tests created by ChatGPT
- Test Coverage: API endpoints, controller interactions, user workflows
- Metrics: Same as above plus performance metrics

**Manual Unit Tests:**
- Location: `src/test/java/org/springframework/samples/petclinic/experimental/manual/unitarias/`
- Purpose: Hand-written unit tests following Spring best practices
- Test Coverage: Same business logic scope as DiffBlue tests
- Metrics: Comparable coverage and quality metrics

**Manual Functional Tests:**
- Location: `src/test/java/org/springframework/samples/petclinic/experimental/manual/funcionales/`
- Purpose: Hand-written integration and E2E tests
- Test Coverage: Same API/controller scope as ChatGPT tests
- Metrics: Comparable to ChatGPT-generated tests

## Running the Comparative Study

This section documents how to reproduce the IA vs Manual test comparison study.

### Prerequisites

- **Java:** 17 or newer (full JDK)
- **Python:** 3.12.6 or newer
- **Maven:** 3.8.x or newer
- **Git:** Latest version

### Research Environment Setup

The study was conducted with the following specifications:

| Component | Specification |
|-----------|---------------|
| **CPU** | Intel i7-12700KF |
| **Memory** | 32GB DDR4 3200MHz |
| **GPU** | NVIDIA RTX 2060 12GB |
| **Storage** | NVMe SSD (5000MB/s read) |
| **OS** | Windows 11 Pro 23H2 |
| **Isolation** | Dedicated machine, no concurrent programs |

### Python Dependencies for Analysis

Install the required Python libraries for statistical analysis:

```bash
pip install pandas==2.3.3 numpy==2.3.4 scipy==1.16.3 matplotlib==3.10.7 seaborn==0.13.2 openpyxl==3.1.5
```

### Test Automation Scripts

Three PowerShell scripts orchestrate the test execution and metrics collection:

#### 1. Unit Tests Execution (`run_pitest_isolated_complete.ps1`)

Executes 40 iterations of unit tests with JaCoCo coverage and PiTest mutation testing:

```powershell
.\run_pitest_isolated_complete.ps1
```

**What it does:**
- Runs 40 iterations of IA-generated unit tests (DiffBlue)
- Runs 40 iterations of manually written unit tests
- Collects JaCoCo metrics: Instruction Coverage (%), Branch Coverage (%)
- Collects PiTest metrics: Mutation Score (%)
- Collects Surefire timing: Test execution time (seconds)
- Outputs CSV files to `unit_tests_metrics/`

**Estimated duration:** 12-18 hours

**Output files:** `unit_tests_metrics/*.csv`

#### 2. Functional Tests Execution (`run-test-metrics.ps1`)

Executes 40 iterations of functional tests with same metrics:

```powershell
.\run-test-metrics.ps1
```

**What it does:**
- Runs 40 iterations of IA-generated functional tests (ChatGPT)
- Runs 40 iterations of manually written functional tests
- Collects identical metrics to unit tests
- Outputs CSV files to `functional_tests_metrics/`

**Estimated duration:** 24-30 hours

**Output files:** `functional_tests_metrics/*.csv`

#### 3. Master Orchestrator (`run_all_metrics_simple.ps1`)

Runs both scripts sequentially with automatic monitoring:

```powershell
.\run_all_metrics_simple.ps1
```

**What it does:**
- Executes unitarias script → 1 minute pause → Executes funcionales script
- Validates script existence before execution
- Prompts for user confirmation before starting
- Measures timing for each phase
- Generates all unit_tests_metrics/ and functional_tests_metrics/ outputs

**Total estimated duration:** 7-8 hours

### Metrics Collected

The study measures four key metrics for each test type:

| Metric | Tool | Description | Unit |
|--------|------|-------------|------|
| **Instruction Coverage** | JaCoCo | % of bytecode instructions executed | % |
| **Branch Coverage** | JaCoCo | % of code branches executed | % |
| **Mutation Score** | PiTest | % of mutations killed by tests | % |
| **Execution Time** | Surefire | Time to run all tests | seconds |

### Data Analysis

Once test execution completes, analyze the collected CSV files:

```bash
# Navigate to analysis directory
cd analisis

# Run Python analysis script (if available)
python analyze_metrics.py
```

The analysis includes:

1. **Descriptive Statistics** (N=12 per iteration)
   - Mean, Median, Std. Dev for each metric
   - By test type and methodology (IA vs Manual)

2. **Assumption Testing**
   - Shapiro-Wilk test for normality (α=0.05)
   - Levene test for homogeneity of variances (α=0.05)

3. **Hypothesis Testing**
   - **Primary Analysis:** Mann-Whitney U test (N=2,480 raw data)
     - Non-parametric comparison (data not normally distributed)
     - Effect size r for practical significance
   
   - **Secondary Analysis:** t-Student/Welch test (N=12 aggregated)
     - Parametric comparison for reference
     - Cohen's d for effect size

4. **Conclusions**
   - Statistical significance of differences
   - Effect sizes and practical implications
   - Recommendations for IA test generation

### Summary Metrics per Test Class

Aggregated metrics (Mean / Median / Std. Dev.) per test class from the 2,480-iteration dataset (`analisis/numerical_data/2480_iterations.csv`). Consolidated CSV: `analisis/numerical_data/summary_metrics_per_class.csv`.

| Test Class | Tool | N | Instr. Mean | Instr. Med | Instr. Std | Branch Mean | Branch Med | Branch Std | Mut. Mean | Mut. Med | Mut. Std | Time Mean | Time Med | Time Std |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Manual** | | | | | | | | | | | | | | |
| OwnerAddPetUnitManualTest | Manual | 200 | 5.03 | 5.03 | 0.00 | 5.00 | 5.00 | 0.00 | 5.56 | 5.56 | 0.00 | 0.01 | 0.00 | 0.01 |
| OwnerGetPetUnitManualTest | Manual | 280 | 10.05 | 10.05 | 0.00 | 18.75 | 18.75 | 0.00 | 16.67 | 16.67 | 0.00 | 0.03 | 0.00 | 0.06 |
| PetValidatorUnitManualTest | Manual | 280 | 7.86 | 7.86 | 0.00 | 12.50 | 12.50 | 0.00 | 25.00 | 25.00 | 0.00 | 0.04 | 0.00 | 0.07 |
| ProcessCreationFormManualTest | Manual | 400 | 35.56 | 35.56 | 0.00 | 37.50 | 37.50 | 0.00 | 50.00 | 50.00 | 0.00 | 0.10 | 0.03 | 0.23 |
| ProcessNewVisitFormManualTest | Manual | 280 | 29.16 | 29.16 | 0.00 | 11.25 | 11.25 | 0.00 | 13.89 | 13.89 | 0.00 | 0.13 | 0.02 | 0.25 |
| ShowOwnerManualTest | Manual | 160 | 21.85 | 21.85 | 0.00 | 2.50 | 2.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.19 | 0.20 | 0.14 |
| **IA** | | | | | | | | | | | | | | |
| OwnerAddPetDiffblueTest | Diffblue Cover | 80 | 5.76 | 5.76 | 0.00 | 5.00 | 5.00 | 0.00 | 5.56 | 5.56 | 0.00 | 0.02 | 0.02 | 0.02 |
| OwnerGetPetDiffblueTest | Diffblue Cover | 400 | 10.69 | 10.69 | 0.00 | 16.25 | 16.25 | 0.00 | 19.44 | 19.44 | 0.00 | 0.01 | 0.00 | 0.01 |
| PetValidatorDiffblueTest | Diffblue Cover | 160 | 7.40 | 7.40 | 0.00 | 11.25 | 11.25 | 0.00 | 16.67 | 16.67 | 0.00 | 0.07 | 0.03 | 0.09 |
| OwnerControllerShowOwnerTestIA | ChatGPT | 80 | 21.57 | 21.57 | 0.00 | 2.50 | 2.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.22 | 0.20 | 0.21 |
| PetControllerProcessCreationFormTestIA | ChatGPT | 80 | 33.00 | 33.00 | 0.00 | 28.75 | 28.75 | 0.00 | 33.33 | 33.33 | 0.00 | 0.43 | 0.42 | 0.37 |
| VisitControllerProcessNewVisitFormTestIA | ChatGPT | 80 | 27.63 | 28.34 | 4.45 | 8.53 | 8.75 | 1.37 | 13.54 | 13.89 | 2.18 | 0.41 | 0.39 | 0.35 |

### Report Generation

The complete statistical report is available in PDF format:

```
analisis/reports/Comparative_Study_AI_vs_Manual_Tests.pdf
analisis/reports/Supplementary_Technical_Record.pdf
```

This report contains:
- Section 1: Introduction to the study and objectives
- Section 2: Methodology, including experimental design and metrics
- Section 3: Results with descriptive statistics, assumption testing, and hypothesis testing
- Section 4: Detailed discussion of results by metric
- Section 5: Study limitations and validity threats
- Section 6: Future work and research directions
- Section 7: General conclusions and practical recommendations
- Section 8: Directory structure explanation

**Figures included:**
- 4 Box plots (t-Student analysis) with English explanations
- 4 Violin plots (Mann-Whitney U analysis) with English explanations
- Execution time comparison graphs

### Study Validity

This study is scientifically valid for comparing IA vs Manual test generation because:

1. **Controlled Design:** 40 iterations with identical conditions across methodologies
2. **Dual Analysis Approach:** Both aggregated (N=12) and raw data (N=2,480) analyzed
3. **Appropriate Statistical Tests:** Mann-Whitney U used for non-normal data
4. **Code Coverage Measurement:** JaCoCo measures System Under Test (SUT), not test code
5. **Mutation Testing:** PiTest measures test effectiveness objectively
6. **Reproducible Environment:** Documented hardware, software, and execution conditions
7. **Isolated Execution:** No concurrent programs affecting measurements

## License

The Spring PetClinic sample application is released under version 2.0 of the [Apache License](https://www.apache.org/licenses/LICENSE-2.0).
