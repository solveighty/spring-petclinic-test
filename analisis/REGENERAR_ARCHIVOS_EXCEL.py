#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
REGENERAR TODOS LOS ARCHIVOS EXCEL CON DATOS VERIFICADOS
=========================================================
"""

import pandas as pd
import numpy as np
from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu
from pathlib import Path
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

RUTA_BASE = Path(r"C:\Users\doleh\Downloads\development\spring-petclinic\analisis")

# Cargar datos
print("Cargando datos consolidados...")
df = pd.read_csv(RUTA_BASE / "datos_consolidados.csv")
df_promedios = df.groupby(['group', 'test_name'])[['instr_pct', 'branch_pct', 'mutation_score', 'time_seconds']].mean().reset_index()

metricas = ['instr_pct', 'branch_pct', 'mutation_score', 'time_seconds']
labels = ['Instruction Coverage (%)', 'Branch Coverage (%)', 'Mutation Score (%)', 'Time (seconds)']

print(f"Total registros: {len(df)}")
print(f"Promedios agregados: {len(df_promedios)}")

# ============================================================================
# ESTADISTICA DESCRIPTIVA
# ============================================================================

print("\n[1/5] Generando ESTADISTICA_DESCRIPTIVA.xlsx...")

# Estadísticas N=2,480 (datos brutos)
desc_results_2480 = []
for metrica, label in zip(metricas, labels):
    for grupo in ['Manual', 'IA']:
        datos = df[df['group'] == grupo][metrica].dropna()
        desc_results_2480.append({
            'Metrica': label,
            'Grupo': grupo,
            'N': len(datos),
            'Media': datos.mean(),
            'Mediana': datos.median(),
            'Desv_Est': datos.std(),
            'Min': datos.min(),
            'Max': datos.max(),
            'Q1': datos.quantile(0.25),
            'Q3': datos.quantile(0.75)
        })

# Estadísticas N=12 (datos agregados)
desc_results_12 = []
for metrica, label in zip(metricas, labels):
    for grupo in ['Manual', 'IA']:
        datos = df_promedios[df_promedios['group'] == grupo][metrica].values
        desc_results_12.append({
            'Metrica': label,
            'Grupo': grupo,
            'N': len(datos),
            'Media': np.mean(datos),
            'Mediana': np.median(datos),
            'Desv_Est': np.std(datos, ddof=1),
            'Min': np.min(datos),
            'Max': np.max(datos),
            'Q1': np.percentile(datos, 25),
            'Q3': np.percentile(datos, 75)
        })

df_desc_2480 = pd.DataFrame(desc_results_2480)
df_desc_12 = pd.DataFrame(desc_results_12)

with pd.ExcelWriter(RUTA_BASE / "ESTADISTICA_DESCRIPTIVA.xlsx", engine='openpyxl') as writer:
    df_desc_2480.to_excel(writer, sheet_name='Descriptiva_N2480', index=False)
    df_desc_12.to_excel(writer, sheet_name='Descriptiva_N12', index=False)

print("  ✓ ESTADISTICA_DESCRIPTIVA.xlsx (2 hojas: N=2,480 + N=12)")

# ============================================================================
# PASO 1: SHAPIRO-WILK
# ============================================================================
# ============================================================================
# PASO 1: SHAPIRO-WILK
# ============================================================================

print("\n[2/5] Generando 01_PASO1_NORMALIDAD_SHAPIRO_WILK.xlsx...")

# Shapiro-Wilk N=2,480 (datos brutos)
shapiro_results_2480 = []
for metrica, label in zip(metricas, labels):
    for grupo in ['Manual', 'IA']:
        datos = df[df['group'] == grupo][metrica].dropna().values
        W, p = shapiro(datos)
        shapiro_results_2480.append({
            'Nivel': 'N=2,480',
            'Metrica': label,
            'Grupo': grupo,
            'N': len(datos),
            'W_statistic': W,
            'p_value': p,
            'Es_Normal': 'SI' if p >= 0.05 else 'NO',
            'Media': np.mean(datos),
            'Desv_Est': np.std(datos, ddof=1)
        })

# Shapiro-Wilk N=12 (datos agregados)
shapiro_results_12 = []
for metrica, label in zip(metricas, labels):
    for grupo in ['Manual', 'IA']:
        datos = df_promedios[df_promedios['group'] == grupo][metrica].values
        W, p = shapiro(datos)
        shapiro_results_12.append({
            'Nivel': 'N=12',
            'Metrica': label,
            'Grupo': grupo,
            'N': len(datos),
            'W_statistic': W,
            'p_value': p,
            'Es_Normal': 'SI' if p >= 0.05 else 'NO',
            'Media': np.mean(datos),
            'Desv_Est': np.std(datos, ddof=1)
        })

df_shapiro_2480 = pd.DataFrame(shapiro_results_2480)
df_shapiro_12 = pd.DataFrame(shapiro_results_12)

with pd.ExcelWriter(RUTA_BASE / "01_PASO1_NORMALIDAD_SHAPIRO_WILK.xlsx", engine='openpyxl') as writer:
    df_shapiro_2480.to_excel(writer, sheet_name='Shapiro_N2480', index=False)
    df_shapiro_12.to_excel(writer, sheet_name='Shapiro_N12', index=False)

print("  ✓ 01_PASO1_NORMALIDAD_SHAPIRO_WILK.xlsx (2 hojas: N=2,480 + N=12)")

# ============================================================================
# PASO 2: LEVENE
# ============================================================================

print("\n[3/5] Generando 02_PASO2_LEVENE_HOMOGENEIDAD_VARIANZAS.xlsx...")

levene_results = []
for metrica, label in zip(metricas, labels):
    dm = df_promedios[df_promedios['group'] == 'Manual'][metrica].values
    di = df_promedios[df_promedios['group'] == 'IA'][metrica].values
    
    F, p = levene(dm, di)
    var_m = np.var(dm, ddof=1)
    var_i = np.var(di, ddof=1)
    
    levene_results.append({
        'Nivel': 'N=12',
        'Metrica': label,
        'N_Manual': len(dm),
        'N_IA': len(di),
        'Var_Manual': var_m,
        'Var_IA': var_i,
        'F_statistic': F,
        'p_value': p,
        'Var_Iguales': 'SI' if p >= 0.05 else 'NO',
        'Test_Usar': 't-Student' if p >= 0.05 else 't-Student Welch'
    })

df_levene = pd.DataFrame(levene_results)
with pd.ExcelWriter(RUTA_BASE / "02_PASO2_LEVENE_HOMOGENEIDAD_VARIANZAS.xlsx", engine='openpyxl') as writer:
    df_levene.to_excel(writer, sheet_name='Levene_N12', index=False)

print("  ✓ 02_PASO2_LEVENE_HOMOGENEIDAD_VARIANZAS.xlsx")

# ============================================================================
# PASO 3A: t-STUDENT
# ============================================================================

print("\n[4/5] Generando 03_PASO3_HIPOTESIS_T_STUDENT.xlsx...")

tstudent_results = []
for metrica, label in zip(metricas, labels):
    dm = df_promedios[df_promedios['group'] == 'Manual'][metrica].values
    di = df_promedios[df_promedios['group'] == 'IA'][metrica].values
    
    # Estadisticas
    mean_m, mean_i = np.mean(dm), np.mean(di)
    std_m, std_i = np.std(dm, ddof=1), np.std(di, ddof=1)
    
    # t-Student
    t_std, p_std = ttest_ind(dm, di, equal_var=True)
    t_welch, p_welch = ttest_ind(dm, di, equal_var=False)
    
    # Cohen's d
    n1, n2 = len(dm), len(di)
    pooled_std = np.sqrt(((n1-1)*std_m**2 + (n2-1)*std_i**2) / (n1+n2-2))
    cohens_d = (mean_m - mean_i) / pooled_std if pooled_std > 0 else 0
    
    # Interpretacion
    if abs(cohens_d) < 0.2:
        interp = 'Negligible'
    elif abs(cohens_d) < 0.5:
        interp = 'Pequeño'
    elif abs(cohens_d) < 0.8:
        interp = 'Mediano'
    else:
        interp = 'Grande'
    
    tstudent_results.append({
        'Metrica': label,
        'N_Manual': n1,
        'N_IA': n2,
        'Media_Manual': mean_m,
        'Media_IA': mean_i,
        'SD_Manual': std_m,
        'SD_IA': std_i,
        'Diferencia': mean_m - mean_i,
        't_statistic_std': t_std,
        'p_value_std': p_std,
        't_statistic_welch': t_welch,
        'p_value_welch': p_welch,
        'Cohens_d': cohens_d,
        'Interpretacion': interp,
        'Significativo': 'SI' if p_welch < 0.05 else 'NO'
    })

df_tstudent = pd.DataFrame(tstudent_results)
with pd.ExcelWriter(RUTA_BASE / "03_PASO3_HIPOTESIS_T_STUDENT.xlsx", engine='openpyxl') as writer:
    df_tstudent.to_excel(writer, sheet_name='Hipotesis_N12', index=False)

print("  ✓ 03_PASO3_HIPOTESIS_T_STUDENT.xlsx")

# ============================================================================
# PASO 3B: MANN-WHITNEY U
# ============================================================================

print("\n[5/5] Generando 03_PASO3B_MANN_WHITNEY_U_N2480.xlsx...")

mw_results = []
for metrica, label in zip(metricas, labels):
    dm = df[df['group'] == 'Manual'][metrica].dropna().values
    di = df[df['group'] == 'IA'][metrica].dropna().values
    
    # Mann-Whitney U
    U, p = mannwhitneyu(dm, di, alternative='two-sided')
    
    # Estadisticas
    n1, n2 = len(dm), len(di)
    median_m, median_i = np.median(dm), np.median(di)
    mean_m, mean_i = np.mean(dm), np.mean(di)
    
    # Z-score y effect size r
    E_U = (n1 * n2) / 2
    Var_U = (n1 * n2 * (n1 + n2 + 1)) / 12
    Z = (U - E_U) / np.sqrt(Var_U)
    r = abs(Z) / np.sqrt(n1 + n2)
    
    # Interpretacion r
    if abs(r) < 0.1:
        interp = 'Negligible'
    elif abs(r) < 0.3:
        interp = 'Pequeño'
    elif abs(r) < 0.5:
        interp = 'Mediano'
    else:
        interp = 'Grande'
    
    mw_results.append({
        'Metrica': label,
        'N_Manual': n1,
        'N_IA': n2,
        'Mediana_Manual': median_m,
        'Mediana_IA': median_i,
        'Media_Manual': mean_m,
        'Media_IA': mean_i,
        'Diferencia_Mediana': median_m - median_i,
        'U_statistic': U,
        'Z_score': Z,
        'p_value': p,
        'r_effect_size': r,
        'Interpretacion': interp,
        'Significativo': 'SI' if p < 0.05 else 'NO'
    })

df_mw = pd.DataFrame(mw_results)
with pd.ExcelWriter(RUTA_BASE / "03_PASO3B_MANN_WHITNEY_U_N2480.xlsx", engine='openpyxl') as writer:
    df_mw.to_excel(writer, sheet_name='Mann_Whitney_N2480', index=False)

print("  ✓ 03_PASO3B_MANN_WHITNEY_U_N2480.xlsx")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n" + "="*80)
print("RESUMEN DE ARCHIVOS GENERADOS")
print("="*80)
print("\n✓ Todos los archivos Excel han sido regenerados con datos verificados")
print("\nArchivos creados:")
print("  1. ESTADISTICA_DESCRIPTIVA.xlsx")
print("  2. 01_PASO1_NORMALIDAD_SHAPIRO_WILK.xlsx")
print("  3. 02_PASO2_LEVENE_HOMOGENEIDAD_VARIANZAS.xlsx")
print("  4. 03_PASO3_HIPOTESIS_T_STUDENT.xlsx")
print("  5. 03_PASO3B_MANN_WHITNEY_U_N2480.xlsx")

print("\n" + "="*80)
print("PROCESO COMPLETADO")
print("="*80)
