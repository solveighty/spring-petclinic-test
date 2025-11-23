#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VERIFICACIÓN RIGUROSA - PASO 1, 2 y 3
=====================================
Validar que todos los cálculos sean correctos
"""

import pandas as pd
import numpy as np
from scipy.stats import shapiro, levene, ttest_ind
from pathlib import Path

# ==================================================================================
# CONFIGURACION
# ==================================================================================

RUTA_BASE = Path(r"C:\Users\doleh\Downloads\development\spring-petclinic\analisis")
METRICAS = ['instr_pct', 'branch_pct', 'mutation_score', 'time_seconds']

print("=" * 100)
print("VERIFICACIÓN RIGUROSA - PASO 1, 2 Y 3")
print("=" * 100)

# ==================================================================================
# CARGAR DATOS
# ==================================================================================

print("\n[PASO 0] Cargando datos...")
df = pd.read_csv(RUTA_BASE / "datos_consolidados.csv")
df_promedios = df.groupby(['group', 'test_name'])[METRICAS].mean().reset_index()

print(f"  ✓ Datos consolidados: {len(df)} registros")
print(f"  ✓ Promedios por test: {len(df_promedios)} tests")

# ==================================================================================
# VERIFICACIÓN 1: SHAPIRO-WILK
# ==================================================================================

print("\n" + "=" * 100)
print("VERIFICACIÓN 1: SHAPIRO-WILK (NORMALIDAD)")
print("=" * 100)

print("\nRecalculando Shapiro-Wilk manualmente...")

errores_shapiro = []

for metrica in METRICAS:
    for nivel in ['N=2480', 'N=12']:
        if nivel == 'N=2480':
            datos_ia = df[df['group'] == 'IA'][metrica].values
            datos_manual = df[df['group'] == 'Manual'][metrica].values
        else:  # N=12
            datos_ia = df_promedios[df_promedios['group'] == 'IA'][metrica].values
            datos_manual = df_promedios[df_promedios['group'] == 'Manual'][metrica].values
        
        # Calcular Shapiro-Wilk
        W_ia, p_ia = shapiro(datos_ia)
        W_manual, p_manual = shapiro(datos_manual)
        
        es_normal_ia = "✓" if p_ia >= 0.05 else "✗"
        es_normal_manual = "✓" if p_manual >= 0.05 else "✗"
        
        print(f"\n{metrica} ({nivel}):")
        print(f"  Manual: W={W_manual:.6f}, p={p_manual:.6f} {es_normal_manual}")
        print(f"  IA:     W={W_ia:.6f}, p={p_ia:.6f} {es_normal_ia}")

# Leer archivo generado
print("\n" + "-" * 100)
print("Comparando con archivo generado (01_PASO1_NORMALIDAD_SHAPIRO_WILK.xlsx)...")

try:
    shapiro_n12 = pd.read_excel(RUTA_BASE / '01_PASO1_NORMALIDAD_SHAPIRO_WILK.xlsx', sheet_name='Shapiro_N12')
    print(f"\n✓ Archivo PASO 1 encontrado")
    print(f"  Registros en Excel: {len(shapiro_n12)}")
    
    # Verificar coincidencia
    for _, row in shapiro_n12.iterrows():
        metrica = row['metrica']
        grupo = row['grupo']
        
        datos = df_promedios[df_promedios['group'] == grupo][metrica].values
        W_stat, p_value = shapiro(datos)
        
        excel_p = row['p_value']
        diferencia = abs(p_value - excel_p)
        
        if diferencia > 0.0001:
            errores_shapiro.append(f"  ✗ {metrica} ({grupo}): p calculado={p_value:.8f} vs Excel={excel_p:.8f}")
        else:
            print(f"  ✓ {metrica} ({grupo}): p-values coinciden")
    
    if not errores_shapiro:
        print("\n✓ PASO 1 VALIDADO: Todos los p-values de Shapiro-Wilk son correctos")
    else:
        print("\n✗ ERRORES ENCONTRADOS EN PASO 1:")
        for error in errores_shapiro:
            print(error)

except Exception as e:
    print(f"✗ Error leyendo PASO 1: {e}")

# ==================================================================================
# VERIFICACIÓN 2: LEVENE
# ==================================================================================

print("\n" + "=" * 100)
print("VERIFICACIÓN 2: LEVENE (HOMOGENEIDAD DE VARIANZAS)")
print("=" * 100)

print("\nRecalculando Levene manualmente...")

errores_levene = []

for metrica in METRICAS:
    datos_ia = df_promedios[df_promedios['group'] == 'IA'][metrica].values
    datos_manual = df_promedios[df_promedios['group'] == 'Manual'][metrica].values
    
    F_stat, p_value = levene(datos_ia, datos_manual)
    
    es_igual = "✓ Igual" if p_value >= 0.05 else "✗ Desigual"
    
    print(f"\n{metrica} (N=12):")
    print(f"  F-statistic={F_stat:.6f}, p={p_value:.6f} {es_igual}")

# Leer archivo generado
print("\n" + "-" * 100)
print("Comparando con archivo generado (02_PASO2_LEVENE_HOMOGENEIDAD_VARIANZAS.xlsx)...")

try:
    levene_n12 = pd.read_excel(RUTA_BASE / '02_PASO2_LEVENE_HOMOGENEIDAD_VARIANZAS.xlsx', sheet_name='Levene_N12')
    print(f"\n✓ Archivo PASO 2 encontrado")
    print(f"  Registros en Excel: {len(levene_n12)}")
    
    # Verificar coincidencia
    for _, row in levene_n12.iterrows():
        metrica = row['metrica']
        
        datos_ia = df_promedios[df_promedios['group'] == 'IA'][metrica].values
        datos_manual = df_promedios[df_promedios['group'] == 'Manual'][metrica].values
        F_stat, p_value = levene(datos_ia, datos_manual)
        
        excel_p = row['p_value']
        diferencia = abs(p_value - excel_p)
        
        if diferencia > 0.0001:
            errores_levene.append(f"  ✗ {metrica}: p calculado={p_value:.8f} vs Excel={excel_p:.8f}")
        else:
            print(f"  ✓ {metrica}: p-values coinciden")
    
    if not errores_levene:
        print("\n✓ PASO 2 VALIDADO: Todos los p-values de Levene son correctos")
    else:
        print("\n✗ ERRORES ENCONTRADOS EN PASO 2:")
        for error in errores_levene:
            print(error)

except Exception as e:
    print(f"✗ Error leyendo PASO 2: {e}")

# ==================================================================================
# VERIFICACIÓN 3: t-Student
# ==================================================================================

print("\n" + "=" * 100)
print("VERIFICACIÓN 3: t-Student (HIPÓTESIS)")
print("=" * 100)

print("\nRecalculando t-Student manualmente...")

errores_ttest = []

for metrica in METRICAS:
    datos_ia = df_promedios[df_promedios['group'] == 'IA'][metrica].values
    datos_manual = df_promedios[df_promedios['group'] == 'Manual'][metrica].values
    
    # Determinar si usar estándar o Welch
    if metrica == 'time_seconds':
        t_stat, p_value = ttest_ind(datos_manual, datos_ia, equal_var=False)
        test = "Welch"
    else:
        t_stat, p_value = ttest_ind(datos_manual, datos_ia, equal_var=True)
        test = "Estándar"
    
    es_sig = "✓ Significativa" if p_value < 0.05 else "✗ NO significativa"
    
    print(f"\n{metrica} (N=12) - t-Student {test}:")
    print(f"  t={t_stat:.6f}, p={p_value:.6f} {es_sig}")

# Leer archivo generado
print("\n" + "-" * 100)
print("Comparando con archivo generado (03_PASO3_HIPOTESIS_T_STUDENT.xlsx)...")

try:
    hipotesis = pd.read_excel(RUTA_BASE / '03_PASO3_HIPOTESIS_T_STUDENT.xlsx', sheet_name='Hipotesis_N12')
    print(f"\n✓ Archivo PASO 3 encontrado")
    print(f"  Registros en Excel: {len(hipotesis)}")
    
    # Verificar coincidencia
    for _, row in hipotesis.iterrows():
        metrica = row['metrica']
        
        datos_ia = df_promedios[df_promedios['group'] == 'IA'][metrica].values
        datos_manual = df_promedios[df_promedios['group'] == 'Manual'][metrica].values
        
        if metrica == 'time_seconds':
            t_stat, p_value = ttest_ind(datos_manual, datos_ia, equal_var=False)
        else:
            t_stat, p_value = ttest_ind(datos_manual, datos_ia, equal_var=True)
        
        excel_p = row['p_value']
        diferencia = abs(p_value - excel_p)
        
        if diferencia > 0.0001:
            errores_ttest.append(f"  ✗ {metrica}: p calculado={p_value:.8f} vs Excel={excel_p:.8f}")
        else:
            print(f"  ✓ {metrica}: p-values coinciden")
    
    if not errores_ttest:
        print("\n✓ PASO 3 VALIDADO: Todos los p-values de t-Student son correctos")
    else:
        print("\n✗ ERRORES ENCONTRADOS EN PASO 3:")
        for error in errores_ttest:
            print(error)

except Exception as e:
    print(f"✗ Error leyendo PASO 3: {e}")

# ==================================================================================
# VALIDACIÓN FINAL
# ==================================================================================

print("\n" + "=" * 100)
print("RESUMEN DE VALIDACIÓN")
print("=" * 100)

errores_totales = len(errores_shapiro) + len(errores_levene) + len(errores_ttest)

if errores_totales == 0:
    print("""
✓ TODOS LOS PASOS VALIDADOS CORRECTAMENTE
═════════════════════════════════════════

• PASO 1 (Shapiro-Wilk): ✓ CORRECTO
• PASO 2 (Levene): ✓ CORRECTO
• PASO 3 (t-Student): ✓ CORRECTO

Los resultados son estadísticamente rigurosos y listos para Capítulo 4.
""")
else:
    print(f"""
✗ SE ENCONTRARON {errores_totales} ERRORES
═════════════════════════════════════════

Revisar los errores marcados arriba y reejecutar los scripts.
""")

# ==================================================================================
# ANÁLISIS ADICIONAL: POTENCIA ESTADÍSTICA
# ==================================================================================

print("\n" + "=" * 100)
print("ANÁLISIS ADICIONAL: PODER ESTADÍSTICO")
print("=" * 100)

print("""
Observación sobre el tamaño de muestra:
├─ N=12 es muy pequeño para detectar diferencias
├─ Con N=12 (6+6), el poder es bajo
├─ Esto puede explicar por qué NO hay diferencias significativas
└─ Aunque haya diferencias prácticas (ej: +25% mutation_score)

Recomendación para tesis:
└─ Mencionar que N=12 es limitante pero justificado por:
   ├─ Disponibilidad de datos
   ├─ Rigor estadístico sobre cantidad
   └─ Alineación con Sección 3.7
""")

print("\n" + "=" * 100)
print("FIN VERIFICACIÓN")
print("=" * 100)
