# Spring PetClinic Sample Application [![Build Status](https://github.com/spring-projects/spring-petclinic/actions/workflows/maven-build.yml/badge.svg)](https://github.com/spring-projects/spring-petclinic/actions/workflows/maven-build.yml)[![Build Status](https://github.com/spring-projects/spring-petclinic/actions/workflows/gradle-build.yml/badge.svg)](https://github.com/spring-projects/spring-petclinic/actions/workflows/gradle-build.yml)

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/spring-projects/spring-petclinic) [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=7517918)

## About This Fork: IA-Generated Tests vs Manual Tests Study

This is a research fork of Spring PetClinic used to conduct a **comparative study of IA-generated tests (DiffBlue, ChatGPT) vs manually written tests** in terms of code coverage, mutation testing effectiveness, and test execution performance.

**Study Objective:** Evaluate the effectiveness of IA tools in automatically generating test cases across unit tests (Unitarias) and functional tests (Funcionales) for a real-world Spring Boot application.

**Research Output:** Complete statistical analysis report available in `analisis/INFORME_COMPLETO_CAPITULO4.html`

### Understanding the Spring Petclinic application with a few diagrams

[See the presentation here](https://speakerdeck.com/michaelisvy/spring-petclinic-sample-application)

## Run Petclinic locally

Spring Petclinic is a [Spring Boot](https://spring.io/guides/gs/spring-boot) application built using [Maven](https://spring.io/guides/gs/maven/) or [Gradle](https://spring.io/guides/gs/gradle/). You can build a jar file and run it from the command line (it should work just as well with Java 17 or newer):

```bash
git clone https://github.com/spring-projects/spring-petclinic.git
cd spring-petclinic
./mvnw package
java -jar target/*.jar
```

(On Windows, or if your shell doesn't expand the glob, you might need to specify the JAR file name explicitly on the command line at the end there.)

You can then access the Petclinic at <http://localhost:8080/>.

<img width="1042" alt="petclinic-screenshot" src="https://cloud.githubusercontent.com/assets/838318/19727082/2aee6d6c-9b8e-11e6-81fe-e889a5ddfded.png">

Or you can run it from Maven directly using the Spring Boot Maven plugin. If you do this, it will pick up changes that you make in the project immediately (changes to Java source files require a compile as well - most people use an IDE for this):

```bash
./mvnw spring-boot:run
```

> NOTE: If you prefer to use Gradle, you can build the app using `./gradlew build` and look for the jar file in `build/libs`.

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

### Report Generation

The complete statistical report is available in HTML format:

```
analisis/INFORME_COMPLETO_CAPITULO4.html
```

This report contains:
- Section 4.0: Experimental Methodology (40 iterations, test structure)
- Section 4.1: Descriptive Statistics (28 statistical summaries)
- Section 4.2: Assumption Testing (Shapiro-Wilk, Levene results)
- Section 4.4: Hypothesis Testing (Mann-Whitney U, t-Student comparisons)
- Section 4.5: Conclusions and Interpretations with visualizations
- Section 4.5.8: Technical Specifications (reproducibility information)

**Figures included:**
- 4 Box plots (t-Student analysis) with Spanish explanations
- 4 Violin plots (Mann-Whitney U analysis) with Spanish explanations
- Execution time comparison graphs

### Directory Structure for Results and Tests

```
spring-petclinic/
├── analisis/
│   ├── INFORME_COMPLETO_CAPITULO4.html          # Main statistical report
│   ├── unit_tests_metrics/                       # Unit test CSV results
│   │   ├── DiffBlue_metrics_*.csv               # IA-generated tests metrics
│   │   └── Manual_metrics_*.csv                 # Manual tests metrics
│   └── functional_tests_metrics/                 # Functional test CSV results
│       ├── ChatGPT_metrics_*.csv                # IA-generated tests metrics
│       └── Manual_metrics_*.csv                 # Manual tests metrics
├── coverage_reports/                            # JaCoCo coverage reports (unitarias)
├── coverage_reports_functional/                 # JaCoCo coverage reports (funcionales)
├── src/test/java/org/springframework/samples/petclinic/experimental/
│   ├── ia/
│   │   ├── unitariasDIFFBLUECOVER/              # DiffBlue IA-generated unit tests
│   │   │   └── [Test classes covering business logic]
│   │   └── funcionalesCHATGPT/                  # ChatGPT IA-generated functional tests
│   │       └── [Integration and E2E test classes]
│   └── manual/
│       ├── unitarias/                           # Hand-written unit tests
│       │   └── [Test classes covering business logic]
│       └── funcionales/                         # Hand-written functional tests
│           └── [Integration and E2E test classes]
├── run_pitest_isolated_complete.ps1            # Unit tests execution script
├── run-test-metrics.ps1                        # Functional tests execution script
└── run_all_metrics_simple.ps1                  # Master orchestrator script
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

### Study Validity

This study is scientifically valid for comparing IA vs Manual test generation because:

1. **Controlled Design:** 40 iterations with identical conditions across methodologies
2. **Dual Analysis Approach:** Both aggregated (N=12) and raw data (N=2,480) analyzed
3. **Appropriate Statistical Tests:** Mann-Whitney U used for non-normal data
4. **Code Coverage Measurement:** JaCoCo measures System Under Test (SUT), not test code
5. **Mutation Testing:** PiTest measures test effectiveness objectively
6. **Reproducible Environment:** Documented hardware, software, and execution conditions
7. **Isolated Execution:** No concurrent programs affecting measurements

## Building a Container

There is no `Dockerfile` in this project. You can build a container image (if you have a docker daemon) using the Spring Boot build plugin:

```bash
./mvnw spring-boot:build-image
```

## In case you find a bug/suggested improvement for Spring Petclinic

Our issue tracker is available [here](https://github.com/spring-projects/spring-petclinic/issues).

## Database configuration

In its default configuration, Petclinic uses an in-memory database (H2) which
gets populated at startup with data. The h2 console is exposed at `http://localhost:8080/h2-console`,
and it is possible to inspect the content of the database using the `jdbc:h2:mem:<uuid>` URL. The UUID is printed at startup to the console.

A similar setup is provided for MySQL and PostgreSQL if a persistent database configuration is needed. Note that whenever the database type changes, the app needs to run with a different profile: `spring.profiles.active=mysql` for MySQL or `spring.profiles.active=postgres` for PostgreSQL. See the [Spring Boot documentation](https://docs.spring.io/spring-boot/how-to/properties-and-configuration.html#howto.properties-and-configuration.set-active-spring-profiles) for more detail on how to set the active profile.

You can start MySQL or PostgreSQL locally with whatever installer works for your OS or use docker:

```bash
docker run -e MYSQL_USER=petclinic -e MYSQL_PASSWORD=petclinic -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=petclinic -p 3306:3306 mysql:9.2
```

or

```bash
docker run -e POSTGRES_USER=petclinic -e POSTGRES_PASSWORD=petclinic -e POSTGRES_DB=petclinic -p 5432:5432 postgres:18.0
```

Further documentation is provided for [MySQL](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/resources/db/mysql/petclinic_db_setup_mysql.txt)
and [PostgreSQL](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/resources/db/postgres/petclinic_db_setup_postgres.txt).

Instead of vanilla `docker` you can also use the provided `docker-compose.yml` file to start the database containers. Each one has a service named after the Spring profile:

```bash
docker compose up mysql
```

or

```bash
docker compose up postgres
```

## Test Applications

At development time we recommend you use the test applications set up as `main()` methods in `PetClinicIntegrationTests` (using the default H2 database and also adding Spring Boot Devtools), `MySqlTestApplication` and `PostgresIntegrationTests`. These are set up so that you can run the apps in your IDE to get fast feedback and also run the same classes as integration tests against the respective database. The MySql integration tests use Testcontainers to start the database in a Docker container, and the Postgres tests use Docker Compose to do the same thing.

## Compiling the CSS

There is a `petclinic.css` in `src/main/resources/static/resources/css`. It was generated from the `petclinic.scss` source, combined with the [Bootstrap](https://getbootstrap.com/) library. If you make changes to the `scss`, or upgrade Bootstrap, you will need to re-compile the CSS resources using the Maven profile "css", i.e. `./mvnw package -P css`. There is no build profile for Gradle to compile the CSS.

## Working with Petclinic in your IDE

### Prerequisites

The following items should be installed in your system:

- Java 17 or newer (full JDK, not a JRE)
- [Git command line tool](https://help.github.com/articles/set-up-git)
- Your preferred IDE
  - Eclipse with the m2e plugin. Note: when m2e is available, there is an m2 icon in `Help -> About` dialog. If m2e is
  not there, follow the install process [here](https://www.eclipse.org/m2e/)
  - [Spring Tools Suite](https://spring.io/tools) (STS)
  - [IntelliJ IDEA](https://www.jetbrains.com/idea/)
  - [VS Code](https://code.visualstudio.com)

### Steps

1. On the command line run:

    ```bash
    git clone https://github.com/spring-projects/spring-petclinic.git
    ```

1. Inside Eclipse or STS:

    Open the project via `File -> Import -> Maven -> Existing Maven project`, then select the root directory of the cloned repo.

    Then either build on the command line `./mvnw generate-resources` or use the Eclipse launcher (right-click on project and `Run As -> Maven install`) to generate the CSS. Run the application's main method by right-clicking on it and choosing `Run As -> Java Application`.

1. Inside IntelliJ IDEA:

    In the main menu, choose `File -> Open` and select the Petclinic [pom.xml](pom.xml). Click on the `Open` button.

    - CSS files are generated from the Maven build. You can build them on the command line `./mvnw generate-resources` or right-click on the `spring-petclinic` project then `Maven -> Generates sources and Update Folders`.

    - A run configuration named `PetClinicApplication` should have been created for you if you're using a recent Ultimate version. Otherwise, run the application by right-clicking on the `PetClinicApplication` main class and choosing `Run 'PetClinicApplication'`.

1. Navigate to the Petclinic

    Visit [http://localhost:8080](http://localhost:8080) in your browser.

## Looking for something in particular?

|Spring Boot Configuration | Class or Java property files  |
|--------------------------|---|
|The Main Class | [PetClinicApplication](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/java/org/springframework/samples/petclinic/PetClinicApplication.java) |
|Properties Files | [application.properties](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/resources) |
|Caching | [CacheConfiguration](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/java/org/springframework/samples/petclinic/system/CacheConfiguration.java) |

## Interesting Spring Petclinic branches and forks

The Spring Petclinic "main" branch in the [spring-projects](https://github.com/spring-projects/spring-petclinic)
GitHub org is the "canonical" implementation based on Spring Boot and Thymeleaf. There are
[quite a few forks](https://spring-petclinic.github.io/docs/forks.html) in the GitHub org
[spring-petclinic](https://github.com/spring-petclinic). If you are interested in using a different technology stack to implement the Pet Clinic, please join the community there.

## Interaction with other open-source projects

One of the best parts about working on the Spring Petclinic application is that we have the opportunity to work in direct contact with many Open Source projects. We found bugs/suggested improvements on various topics such as Spring, Spring Data, Bean Validation and even Eclipse! In many cases, they've been fixed/implemented in just a few days.
Here is a list of them:

| Name | Issue |
|------|-------|
| Spring JDBC: simplify usage of NamedParameterJdbcTemplate | [SPR-10256](https://github.com/spring-projects/spring-framework/issues/14889) and [SPR-10257](https://github.com/spring-projects/spring-framework/issues/14890) |
| Bean Validation / Hibernate Validator: simplify Maven dependencies and backward compatibility |[HV-790](https://hibernate.atlassian.net/browse/HV-790) and [HV-792](https://hibernate.atlassian.net/browse/HV-792) |
| Spring Data: provide more flexibility when working with JPQL queries | [DATAJPA-292](https://github.com/spring-projects/spring-data-jpa/issues/704) |

## Contributing

The [issue tracker](https://github.com/spring-projects/spring-petclinic/issues) is the preferred channel for bug reports, feature requests and submitting pull requests.

For pull requests, editor preferences are available in the [editor config](.editorconfig) for easy use in common text editors. Read more and download plugins at <https://editorconfig.org>. All commits must include a __Signed-off-by__ trailer at the end of each commit message to indicate that the contributor agrees to the Developer Certificate of Origin.
For additional details, please refer to the blog post [Hello DCO, Goodbye CLA: Simplifying Contributions to Spring](https://spring.io/blog/2025/01/06/hello-dco-goodbye-cla-simplifying-contributions-to-spring).

## License

The Spring PetClinic sample application is released under version 2.0 of the [Apache License](https://www.apache.org/licenses/LICENSE-2.0).
