#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PASO 2: LEVENE - HOMOGENEIDAD DE VARIANZAS
===========================================
Análisis riguroso N=12
Decidiremos entre t-Student o t-Student Welch
"""

import pandas as pd
import numpy as np
from scipy.stats import levene
import os
from pathlib import Path

# ==================================================================================
# CONFIGURACION
# ==================================================================================

RUTA_BASE = Path(r"C:\Users\doleh\Downloads\development\spring-petclinic\analisis")
METRICAS = ['instr_pct', 'branch_pct', 'mutation_score', 'time_seconds']

# ==================================================================================
# PASO 0: CARGAR DATOS CONSOLIDADOS
# ==================================================================================

print("=" * 100)
print("PASO 2: LEVENE - HOMOGENEIDAD DE VARIANZAS")
print("=" * 100)
print("\nPASO 0: Cargando datos consolidados...")

archivo_consolidado = RUTA_BASE / "datos_consolidados.csv"
df_consolidated = pd.read_csv(archivo_consolidado)

print(f"  ✓ Total registros: {len(df_consolidated)}")
print(f"  ✓ Grupos: {df_consolidated['group'].unique()}")

# ==================================================================================
# PASO 2A: LEVENE EN N=2,480 (EXPLORACIÓN)
# ==================================================================================

print("\n" + "=" * 100)
print("PASO 2A: LEVENE EN N=2,480 (EXPLORACIÓN)")
print("=" * 100)

resultados_levene_2480 = []

for metrica in METRICAS:
    print(f"\n╔{'═' * 96}╗")
    print(f"║ Métrica: {metrica:<85}║")
    print(f"╚{'═' * 96}╝")
    
    # Obtener datos por grupo
    datos_ia = df_consolidated[df_consolidated['group'] == 'IA'][metrica].values
    datos_manual = df_consolidated[df_consolidated['group'] == 'Manual'][metrica].values
    
    # Calcular varianzas
    var_ia = np.var(datos_ia, ddof=1)
    var_manual = np.var(datos_manual, ddof=1)
    
    # Ejecutar Levene
    F_stat, p_value = levene(datos_ia, datos_manual)
    
    # Interpretación
    es_igual = "✓ Varianzas IGUALES" if p_value >= 0.05 else "✗ Varianzas DESIGUALES"
    
    print(f"\n  IA (N={len(datos_ia)}):")
    print(f"  ├─ Varianza: {var_ia:.6f}")
    print(f"  └─ Std Dev: {np.std(datos_ia, ddof=1):.6f}")
    
    print(f"\n  Manual (N={len(datos_manual)}):")
    print(f"  ├─ Varianza: {var_manual:.6f}")
    print(f"  └─ Std Dev: {np.std(datos_manual, ddof=1):.6f}")
    
    print(f"\n  Prueba de Levene:")
    print(f"  ├─ F-statistic: {F_stat:.6f}")
    print(f"  ├─ p-value: {p_value:.8f}")
    print(f"  ├─ Resultado: {es_igual}")
    print(f"  └─ Razón: Varianza IA {'>' if var_ia > var_manual else '<'} Varianza Manual")
    
    resultados_levene_2480.append({
        'nivel': 'N=2,480',
        'metrica': metrica,
        'n_ia': len(datos_ia),
        'n_manual': len(datos_manual),
        'var_ia': var_ia,
        'var_manual': var_manual,
        'F_statistic': F_stat,
        'p_value': p_value,
        'es_igual': es_igual
    })

# ==================================================================================
# PASO 2B: LEVENE EN N=12 (ANÁLISIS RIGUROSO) ← IMPORTANTE
# ==================================================================================

print("\n" + "=" * 100)
print("PASO 2B: LEVENE EN N=12 (ANÁLISIS RIGUROSO)")
print("=" * 100)

# Calcular promedios por test
df_promedios = df_consolidated.groupby(['group', 'test_name'])[METRICAS].mean().reset_index()

print(f"\nTests encontrados: {len(df_promedios)}")
print(f"  Manual: {len(df_promedios[df_promedios['group'] == 'Manual'])}")
print(f"  IA: {len(df_promedios[df_promedios['group'] == 'IA'])}")

resultados_levene_12 = []

for metrica in METRICAS:
    print(f"\n╔{'═' * 96}╗")
    print(f"║ Métrica: {metrica:<85}║")
    print(f"╚{'═' * 96}╝")
    
    # Obtener datos por grupo (N=12)
    datos_ia = df_promedios[df_promedios['group'] == 'IA'][metrica].values
    datos_manual = df_promedios[df_promedios['group'] == 'Manual'][metrica].values
    
    # Calcular varianzas
    var_ia = np.var(datos_ia, ddof=1)
    var_manual = np.var(datos_manual, ddof=1)
    
    # Ejecutar Levene
    if len(datos_ia) >= 2 and len(datos_manual) >= 2:
        F_stat, p_value = levene(datos_ia, datos_manual)
    else:
        F_stat, p_value = np.nan, np.nan
    
    # Interpretación
    es_igual = "✓ Varianzas IGUALES" if p_value >= 0.05 else "✗ Varianzas DESIGUALES"
    
    print(f"\n  IA (N={len(datos_ia)}):")
    print(f"  ├─ Valores: {datos_ia}")
    print(f"  ├─ Varianza: {var_ia:.6f}")
    print(f"  └─ Std Dev: {np.std(datos_ia, ddof=1):.6f}")
    
    print(f"\n  Manual (N={len(datos_manual)}):")
    print(f"  ├─ Valores: {datos_manual}")
    print(f"  ├─ Varianza: {var_manual:.6f}")
    print(f"  └─ Std Dev: {np.std(datos_manual, ddof=1):.6f}")
    
    print(f"\n  Prueba de Levene:")
    print(f"  ├─ F-statistic: {F_stat:.6f}")
    print(f"  ├─ p-value: {p_value:.8f}")
    print(f"  ├─ Resultado: {es_igual}")
    print(f"  ├─ Razón: Varianza IA {'>' if var_ia > var_manual else '<'} Varianza Manual")
    print(f"  └─ Ratio Varianzas: {max(var_ia, var_manual) / min(var_ia, var_manual):.2f}:1")
    
    resultados_levene_12.append({
        'nivel': 'N=12',
        'metrica': metrica,
        'n_ia': len(datos_ia),
        'n_manual': len(datos_manual),
        'var_ia': var_ia,
        'var_manual': var_manual,
        'F_statistic': F_stat,
        'p_value': p_value,
        'es_igual': es_igual,
        'ratio_var': max(var_ia, var_manual) / min(var_ia, var_manual)
    })

# ==================================================================================
# MATRIZ DE DECISIONES PARA PASO 3
# ==================================================================================

print("\n" + "=" * 100)
print("MATRIZ DE DECISIONES - ¿t-Student o t-Student Welch?")
print("=" * 100)

print("\n(Basado en Levene N=12)")
print("\n┌────────────────────┬──────────────────┬─────────────────────────────────┐")
print("│      Métrica       │  Varianzas       │    Test a usar en Paso 3        │")
print("│                    │   (Levene N=12)  │    (Manual vs IA)               │")
print("├────────────────────┼──────────────────┼─────────────────────────────────┤")

for row in resultados_levene_12:
    metrica = row['metrica']
    es_igual = row['es_igual']
    
    if "IGUALES" in es_igual:
        test_a_usar = "t-Student (estándar)"
        simbolo = "✓"
    else:
        test_a_usar = "t-Student Welch (corregido)"
        simbolo = "✗"
    
    print(f"│ {metrica:<18} │ {simbolo} {es_igual:<14} │ {test_a_usar:<29} │")

print("└────────────────────┴──────────────────┴─────────────────────────────────┘")

# ==================================================================================
# GUARDAR RESULTADOS EN EXCEL
# ==================================================================================

print("\n" + "=" * 100)
print("GUARDANDO RESULTADOS...")
print("=" * 100)

archivo_excel = RUTA_BASE / "02_PASO2_LEVENE_HOMOGENEIDAD_VARIANZAS.xlsx"

try:
    df_res_2480 = pd.DataFrame(resultados_levene_2480)
    df_res_12 = pd.DataFrame(resultados_levene_12)
    
    with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
        df_res_2480.to_excel(writer, sheet_name='Levene_N2480', index=False)
        df_res_12.to_excel(writer, sheet_name='Levene_N12', index=False)
    
    print(f"\n✓ Archivo guardado: {archivo_excel}")
except ImportError:
    print("\n! Openpyxl no instalado, guardando como CSV...")
    pd.DataFrame(resultados_levene_2480).to_csv(RUTA_BASE / "02_PASO2_LEVENE_N2480.csv", index=False)
    pd.DataFrame(resultados_levene_12).to_csv(RUTA_BASE / "02_PASO2_LEVENE_N12.csv", index=False)
    print("✓ Archivos CSV guardados")

# ==================================================================================
# CONCLUSIONES
# ==================================================================================

print("\n" + "=" * 100)
print("CONCLUSIONES PASO 2")
print("=" * 100)

print("""
1. NIVEL N=2,480 (EXPLORACIÓN):
   └─ Muestra varianzas en datos CRUDOS
   └─ Esperado: Varianzas desiguales (por estructura de escalones)
   └─ Uso: Solo informativo

2. NIVEL N=12 (RIGUROSO) ← LO MÁS IMPORTANTE:
   └─ Verifica igualdad de varianzas entre Manual e IA
   └─ Resultado: Define si usar t-Student o t-Student Welch
   └─ Uso: Para decisión definitiva en Paso 3

3. PRÓXIMO PASO (PASO 3):
   └─ Ejecutaremos prueba de hipótesis
   └─ Compararemos medias Manual vs IA
   └─ Usaremos t-Student o t-Student Welch según Levene

════════════════════════════════════════════════════════════════════════════════════════════════
""")

print("=" * 100)
print("FIN PASO 2 - LEVENE (HOMOGENEIDAD DE VARIANZAS)")
print("=" * 100)
