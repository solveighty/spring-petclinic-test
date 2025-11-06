"""
Análisis Estadístico Descriptivo - 40 Iteraciones (SIN EMOJIS)
Cálculo de Media, Mediana, Desviación Estándar por métrica y grupo (Manual vs IA)
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE_PATH = Path("./unit_tests_metrics")
FUNCTIONAL_PATH = Path("./functional_tests_metrics")

print("=" * 80)
print("ESTADISTICA DESCRIPTIVA - 40 ITERACIONES")
print("=" * 80)

# Cargar todos los CSVs
dfs = []

unitarias_files = [
    "IA_OwnerAddPetDiffblueTest.csv",
    "IA_OwnerGetPetDiffblueTest.csv",
    "IA_PetValidatorDiffblueTest.csv",
    "Manual_OwnerAddPetUnitManualTest.csv",
    "Manual_OwnerGetPetUnitManualTest.csv",
    "Manual_PetValidatorUnitManualTest.csv",
]

funcionales_files = [
    "IA_OwnerControllerShowOwnerTestIA.csv",
    "IA_PetControllerProcessCreationFormTestIA.csv",
    "IA_VisitControllerProcessNewVisitFormTestIA.csv",
    "Manual_ShowOwnerManualTest.csv",
    "Manual_ProcessCreationFormManualTest.csv",
    "Manual_ProcessNewVisitFormManualTest.csv",
]

print("\nCargando archivos...")
for file in unitarias_files:
    filepath = BASE_PATH / file
    if filepath.exists():
        df = pd.read_csv(filepath)
        df['category'] = 'Unitarias'
        dfs.append(df)

for file in funcionales_files:
    filepath = FUNCTIONAL_PATH / file
    if filepath.exists():
        df = pd.read_csv(filepath)
        df['category'] = 'Funcionales'
        dfs.append(df)

df_consolidated = pd.concat(dfs, ignore_index=True)
print(f"Total: {len(df_consolidated)} registros cargados")

# Métricas
metricas = ['instr_pct', 'branch_pct', 'mutation_score', 'time_seconds']

# RESUMEN GLOBAL
print("\n" + "=" * 90)
print("RESUMEN GLOBAL - MANUAL vs IA")
print("=" * 90)

for metrica in metricas:
    print(f"\n{metrica.upper()}")
    print("-" * 90)
    print(f"{'Grupo':<10} {'n':>6} {'Media':>12} {'Mediana':>12} {'Desv.Est':>12} {'Min':>10} {'Max':>10}")
    print("-" * 90)
    
    for grupo in ['Manual', 'IA']:
        datos = df_consolidated[df_consolidated['group'] == grupo][metrica]
        print(f"{grupo:<10} {len(datos):>6.0f} {datos.mean():>12.4f} {datos.median():>12.4f} "
              f"{datos.std():>12.4f} {datos.min():>10.4f} {datos.max():>10.4f}")
    
    manual = df_consolidated[df_consolidated['group'] == 'Manual'][metrica]
    ia = df_consolidated[df_consolidated['group'] == 'IA'][metrica]
    diff = ia.mean() - manual.mean()
    pct = (diff / manual.mean() * 100) if manual.mean() != 0 else 0
    
    print(f"\nDiferencia IA - Manual: {diff:+.4f} ({pct:+.2f}%)\n")

# POR CATEGORÍA
print("\n" + "=" * 90)
print("POR CATEGORÍA")
print("=" * 90)

for categoria in ['Unitarias', 'Funcionales']:
    print(f"\n{'='*90}")
    print(f"CATEGORÍA: {categoria}")
    print(f"{'='*90}")
    
    df_cat = df_consolidated[df_consolidated['category'] == categoria]
    
    for metrica in metricas:
        print(f"\n{metrica.upper()}")
        print("-" * 90)
        print(f"{'Grupo':<10} {'n':>6} {'Media':>12} {'Mediana':>12} {'Desv.Est':>12} {'Min':>10} {'Max':>10}")
        print("-" * 90)
        
        for grupo in ['Manual', 'IA']:
            datos = df_cat[df_cat['group'] == grupo][metrica]
            if len(datos) > 0:
                print(f"{grupo:<10} {len(datos):>6.0f} {datos.mean():>12.4f} {datos.median():>12.4f} "
                      f"{datos.std():>12.4f} {datos.min():>10.4f} {datos.max():>10.4f}")

# EXPORTAR
print("\n" + "=" * 90)
print("EXPORTANDO...")
print("=" * 90)

df_consolidated.to_csv('datos_consolidados.csv', index=False)
print("Guardado: datos_consolidados.csv")

# Crear resumen en Excel
with pd.ExcelWriter('ESTADISTICA_DESCRIPTIVA.xlsx', engine='openpyxl') as writer:
    df_consolidated.to_excel(writer, sheet_name='Datos', index=False)
    
    for categoria in ['Unitarias', 'Funcionales']:
        df_cat = df_consolidated[df_consolidated['category'] == categoria]
        df_cat.to_excel(writer, sheet_name=categoria, index=False)

print("Guardado: ESTADISTICA_DESCRIPTIVA.xlsx")
print("\nCompleto.")
