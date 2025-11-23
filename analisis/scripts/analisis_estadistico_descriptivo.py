"""
Análisis Estadístico Descriptivo - 40 Iteraciones
Cálculo de Media, Mediana, Desviación Estándar por métrica y grupo (Manual vs IA)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os

# Configurar ruta
BASE_PATH = Path("./unit_tests_metrics")
FUNCTIONAL_PATH = Path("./functional_tests_metrics")

# ============================================================================
# 1. CARGAR TODOS LOS ARCHIVOS CSV
# ============================================================================

print("=" * 80)
print("ANÁLISIS ESTADÍSTICO DESCRIPTIVO - 40 ITERACIONES")
print("=" * 80)
print("\nCargando datos...")

# Cargar todos los CSVs
dfs = []

# Unitarias
unitarias_files = [
    "IA_OwnerAddPetDiffblueTest.csv",
    "IA_OwnerGetPetDiffblueTest.csv",
    "IA_PetValidatorDiffblueTest.csv",
    "Manual_OwnerAddPetUnitManualTest.csv",
    "Manual_OwnerGetPetUnitManualTest.csv",
    "Manual_PetValidatorUnitManualTest.csv",
]

for file in unitarias_files:
    filepath = BASE_PATH / file
    if filepath.exists():
        df = pd.read_csv(filepath)
        df['category'] = 'Unitarias'
        dfs.append(df)
        print(f"[OK] {file} ({len(df)-1} registros)")
    else:
        print(f"[ERROR] {file} NO ENCONTRADO")

# Funcionales
funcionales_files = [
    "IA_OwnerControllerShowOwnerTestIA.csv",
    "IA_PetControllerProcessCreationFormTestIA.csv",
    "IA_VisitControllerProcessNewVisitFormTestIA.csv",
    "Manual_ShowOwnerManualTest.csv",
    "Manual_ProcessCreationFormManualTest.csv",
    "Manual_ProcessNewVisitFormManualTest.csv",
]

for file in funcionales_files:
    filepath = FUNCTIONAL_PATH / file
    if filepath.exists():
        df = pd.read_csv(filepath)
        df['category'] = 'Funcionales'
        dfs.append(df)
        print(f"[OK] {file} ({len(df)-1} registros)")
    else:
        print(f"[ERROR] {file} NO ENCONTRADO")

# Consolidar
df_consolidated = pd.concat(dfs, ignore_index=True)
print(f"\n[OK] Total de registros consolidados: {len(df_consolidated)}")
print(f"[OK] Grupos: {df_consolidated['group'].unique()}")
print(f"[OK] Categorías: {df_consolidated['category'].unique()}")

# ============================================================================
# 2. ESTADÍSTICA DESCRIPTIVA GLOBAL (Manual vs IA)
# ============================================================================

print("\n" + "=" * 80)
print("ESTADÍSTICA DESCRIPTIVA GLOBAL - MANUAL vs IA")
print("=" * 80)

# Métricas a analizar
metricas = ['instr_pct', 'branch_pct', 'mutation_score', 'time_seconds']

# Crear tabla de resumen
resumen_stats = []

for metrica in metricas:
    for grupo in ['Manual', 'IA']:
        datos = df_consolidated[df_consolidated['group'] == grupo][metrica]
        
        stats_row = {
            'Métrica': metrica,
            'Grupo': grupo,
            'n': len(datos),
            'Media': datos.mean(),
            'Mediana': datos.median(),
            'Desv.Est': datos.std(),
            'Min': datos.min(),
            'Max': datos.max(),
            'Q1': datos.quantile(0.25),
            'Q3': datos.quantile(0.75),
            'IQR': datos.quantile(0.75) - datos.quantile(0.25),
        }
        resumen_stats.append(stats_row)

df_stats = pd.DataFrame(resumen_stats)

# Mostrar por métrica
for metrica in metricas:
    print(f"\nMETRICA: {metrica}")
    print("-" * 80)
    
    df_metrica = df_stats[df_stats['Métrica'] == metrica].copy()
    
    # Mostrar tabla
    print(f"\n{'Grupo':<10} {'n':>5} {'Media':>10} {'Mediana':>10} {'Desv.Est':>10} {'Min':>8} {'Max':>8}")
    print("-" * 80)
    
    for _, row in df_metrica.iterrows():
        print(f"{row['Grupo']:<10} {row['n']:>5.0f} {row['Media']:>10.4f} {row['Mediana']:>10.4f} "
              f"{row['Desv.Est']:>10.4f} {row['Min']:>8.4f} {row['Max']:>8.4f}")
    
    # Calcular diferencia
    manual_row = df_metrica[df_metrica['Grupo'] == 'Manual'].iloc[0]
    ia_row = df_metrica[df_metrica['Grupo'] == 'IA'].iloc[0]
    
    diff_media = ia_row['Media'] - manual_row['Media']
    diff_mediana = ia_row['Mediana'] - manual_row['Mediana']
    
    print(f"\n  Diferencia (IA - Manual):")
    print(f"    Media: {diff_media:+.4f} ({(diff_media/manual_row['Media']*100):+.2f}%)")
    print(f"    Mediana: {diff_mediana:+.4f} ({(diff_mediana/manual_row['Mediana']*100):+.2f}%)")

# ============================================================================
# 3. ESTADÍSTICA DESCRIPTIVA POR CATEGORÍA
# ============================================================================

print("\n\n" + "=" * 80)
print("ESTADÍSTICA DESCRIPTIVA POR CATEGORÍA (Unitarias vs Funcionales)")
print("=" * 80)

for categoria in ['Unitarias', 'Funcionales']:
    print(f"\n\n{'='*80}")
    print(f"CATEGORÍA: {categoria}")
    print(f"{'='*80}")
    
    df_cat = df_consolidated[df_consolidated['category'] == categoria]
    
    for metrica in metricas:
        print(f"\n📊 MÉTRICA: {metrica}")
        print("-" * 80)
        print(f"{'Grupo':<10} {'n':>5} {'Media':>10} {'Mediana':>10} {'Desv.Est':>10} {'Min':>8} {'Max':>8}")
        print("-" * 80)
        
        for grupo in ['Manual', 'IA']:
            datos = df_cat[df_cat['group'] == grupo][metrica]
            if len(datos) > 0:
                print(f"{grupo:<10} {len(datos):>5.0f} {datos.mean():>10.4f} {datos.median():>10.4f} "
                      f"{datos.std():>10.4f} {datos.min():>8.4f} {datos.max():>8.4f}")

# ============================================================================
# 4. ESTADÍSTICA DESCRIPTIVA POR CLASE DE TEST
# ============================================================================

print("\n\n" + "=" * 80)
print("ESTADÍSTICA DESCRIPTIVA POR CLASE DE TEST")
print("=" * 80)

test_classes = df_consolidated['test_class'].unique()

for test_class in sorted(test_classes):
    df_test = df_consolidated[df_consolidated['test_class'] == test_class]
    
    print(f"\n\n{'='*80}")
    print(f"CLASE: {test_class}")
    print(f"{'='*80}")
    
    for metrica in metricas:
        print(f"\n📊 MÉTRICA: {metrica}")
        print("-" * 80)
        print(f"{'Grupo':<10} {'n':>5} {'Media':>10} {'Mediana':>10} {'Desv.Est':>10} {'Min':>8} {'Max':>8}")
        print("-" * 80)
        
        for grupo in ['Manual', 'IA']:
            datos = df_test[df_test['group'] == grupo][metrica]
            if len(datos) > 0:
                print(f"{grupo:<10} {len(datos):>5.0f} {datos.mean():>10.4f} {datos.median():>10.4f} "
                      f"{datos.std():>10.4f} {datos.min():>8.4f} {datos.max():>8.4f}")

# ============================================================================
# 5. EXPORTAR A EXCEL PARA ANÁLISIS POSTERIOR
# ============================================================================

print("\n\n" + "=" * 80)
print("EXPORTANDO RESULTADOS")
print("=" * 80)

# Guardar la tabla de estadística global
df_stats_formatted = df_stats.round(4)
df_stats_formatted.to_csv('estadistica_descriptiva_global.csv', index=False)
print("\n✅ CSV guardado: estadistica_descriptiva_global.csv")

# Guardar datos consolidados
df_consolidated.to_csv('datos_consolidados_40_iteraciones.csv', index=False)
print("✅ CSV guardado: datos_consolidados_40_iteraciones.csv")

# Crear Excel con múltiples sheets
with pd.ExcelWriter('ANALISIS_ESTADISTICO_DESCRIPTIVO.xlsx', engine='openpyxl') as writer:
    df_stats_formatted.to_excel(writer, sheet_name='Resumen Global', index=False)
    df_consolidated.to_excel(writer, sheet_name='Datos Consolidados', index=False)
    
    # Tablas por categoría
    for categoria in ['Unitarias', 'Funcionales']:
        df_cat = df_consolidated[df_consolidated['category'] == categoria]
        df_cat.to_excel(writer, sheet_name=f'{categoria}', index=False)

print("✅ Excel guardado: ANALISIS_ESTADISTICO_DESCRIPTIVO.xlsx")

print("\n" + "=" * 80)
print("✅ ANÁLISIS COMPLETO")
print("=" * 80)
print("\n📁 Archivos generados:")
print("   1. estadistica_descriptiva_global.csv")
print("   2. datos_consolidados_40_iteraciones.csv")
print("   3. ANALISIS_ESTADISTICO_DESCRIPTIVO.xlsx")
print("\nPróximo paso: Pruebas de normalidad (Shapiro-Wilk)")
