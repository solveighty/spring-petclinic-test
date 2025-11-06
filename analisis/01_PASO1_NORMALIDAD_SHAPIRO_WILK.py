#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PASO 1: NORMALIDAD - SHAPIRO-WILK TEST
========================================
Análisis riguroso de normalidad en N=2,480 y N=12
"""

import pandas as pd
import numpy as np
from scipy.stats import shapiro
import os
from pathlib import Path

# ==================================================================================
# CONFIGURACION
# ==================================================================================

RUTA_BASE = Path(r"C:\Users\doleh\Downloads\development\spring-petclinic\analisis")
RUTA_UNITARIAS = RUTA_BASE / "unit_tests_metrics"
RUTA_FUNCIONALES = RUTA_BASE / "functional_tests_metrics"

METRICAS = ['instr_pct', 'branch_pct', 'mutation_score', 'time_seconds']

# ==================================================================================
# PASO 0: CARGAR DATOS CONSOLIDADOS
# ==================================================================================

print("=" * 100)
print("PASO 1: NORMALIDAD (SHAPIRO-WILK)")
print("=" * 100)
print("\nPASO 0: Cargando datos consolidados...")

# Buscar si ya existe el archivo consolidado
archivo_consolidado = RUTA_BASE / "datos_consolidados.csv"

if archivo_consolidado.exists():
    print(f"  ✓ Cargando desde archivo existente: {archivo_consolidado}")
    df_consolidated = pd.read_csv(archivo_consolidado)
else:
    print("  ! No encontrado archivo consolidado, creando...")
    
    # Cargar archivos manuales
    archivos_unitarias = sorted(RUTA_UNITARIAS.glob("*.csv"))
    archivos_funcionales = sorted(RUTA_FUNCIONALES.glob("*.csv"))
    
    dfs = []
    
    # Unitarias
    for archivo in archivos_unitarias:
        df = pd.read_csv(archivo)
        df['category'] = 'Unitarias'
        # Extraer grupo del nombre del archivo
        if archivo.stem.startswith('IA_'):
            df['group'] = 'IA'
        else:
            df['group'] = 'Manual'
        df['test_name'] = archivo.stem
        dfs.append(df)
    
    # Funcionales
    for archivo in archivos_funcionales:
        df = pd.read_csv(archivo)
        df['category'] = 'Funcionales'
        # Extraer grupo del nombre del archivo
        if archivo.stem.startswith('IA_'):
            df['group'] = 'IA'
        else:
            df['group'] = 'Manual'
        df['test_name'] = archivo.stem
        dfs.append(df)
    
    df_consolidated = pd.concat(dfs, ignore_index=True)
    
    # Guardar para próximas ejecuciones
    df_consolidated.to_csv(archivo_consolidado, index=False)
    print(f"  ✓ Archivo consolidado creado y guardado")

print(f"  ✓ Total registros: {len(df_consolidated)}")
print(f"  ✓ Grupos: {df_consolidated['group'].unique()}")
print(f"  ✓ Métricas: {METRICAS}")

# ==================================================================================
# PASO 1A: SHAPIRO-WILK EN N=2,480 (EXPLORACION)
# ==================================================================================

print("\n" + "=" * 100)
print("PASO 1A: SHAPIRO-WILK EN N=2,480 (EXPLORACION)")
print("=" * 100)

resultados_2480 = []

for metrica in METRICAS:
    print(f"\n╔{'═' * 96}╗")
    print(f"║ Métrica: {metrica:<85}║")
    print(f"╚{'═' * 96}╝")
    
    for grupo in sorted(df_consolidated['group'].unique()):
        # Obtener datos
        datos = df_consolidated[df_consolidated['group'] == grupo][metrica].values
        n = len(datos)
        
        # Ejecutar Shapiro-Wilk
        W_stat, p_value = shapiro(datos)
        
        # Interpretación
        es_normal = "✓ SÍ es normal" if p_value >= 0.05 else "✗ NO es normal"
        
        # Estadísticas descriptivas
        media = np.mean(datos)
        mediana = np.median(datos)
        std = np.std(datos, ddof=1)
        min_val = np.min(datos)
        max_val = np.max(datos)
        
        # Guardar resultado
        resultados_2480.append({
            'nivel': 'N=2,480',
            'metrica': metrica,
            'grupo': grupo,
            'n': n,
            'W_statistic': W_stat,
            'p_value': p_value,
            'es_normal': es_normal,
            'media': media,
            'mediana': mediana,
            'std': std,
            'min': min_val,
            'max': max_val
        })
        
        print(f"\n  Grupo: {grupo} (N={n})")
        print(f"  ├─ W-statistic: {W_stat:.6f}")
        print(f"  ├─ p-value: {p_value:.8f}")
        print(f"  ├─ Resultado: {es_normal}")
        print(f"  ├─ Media: {media:.6f}")
        print(f"  ├─ Mediana: {mediana:.6f}")
        print(f"  ├─ Std Dev: {std:.6f}")
        print(f"  ├─ Min: {min_val:.6f}")
        print(f"  └─ Max: {max_val:.6f}")

# ==================================================================================
# PASO 1B: SHAPIRO-WILK EN N=12 (ANÁLISIS RIGUROSO)
# ==================================================================================

print("\n" + "=" * 100)
print("PASO 1B: SHAPIRO-WILK EN N=12 (ANÁLISIS RIGUROSO)")
print("=" * 100)

# Calcular promedios por test
print("\nCalculando promedios por test (40 iteraciones cada uno)...")

df_promedios = df_consolidated.groupby(['group', 'test_name'])[METRICAS].mean().reset_index()

print(f"  ✓ Tests únicos encontrados: {len(df_promedios)}")
print(f"  ✓ Manual: {len(df_promedios[df_promedios['group'] == 'Manual'])}")
print(f"  ✓ IA: {len(df_promedios[df_promedios['group'] == 'IA'])}")

# Mostrar los tests
print("\n  Tests Manual:")
for idx, row in df_promedios[df_promedios['group'] == 'Manual'].iterrows():
    print(f"    - {row['test_name']}")

print("\n  Tests IA:")
for idx, row in df_promedios[df_promedios['group'] == 'IA'].iterrows():
    print(f"    - {row['test_name']}")

# Ejecutar Shapiro-Wilk en N=12
resultados_12 = []

for metrica in METRICAS:
    print(f"\n╔{'═' * 96}╗")
    print(f"║ Métrica: {metrica:<85}║")
    print(f"╚{'═' * 96}╝")
    
    for grupo in sorted(df_promedios['group'].unique()):
        # Obtener datos (promedios)
        datos = df_promedios[df_promedios['group'] == grupo][metrica].values
        n = len(datos)
        
        # Ejecutar Shapiro-Wilk
        if n >= 3:  # Shapiro-Wilk requiere al menos 3 observaciones
            W_stat, p_value = shapiro(datos)
        else:
            W_stat, p_value = np.nan, np.nan
        
        # Interpretación
        if n >= 3:
            es_normal = "✓ SÍ es normal" if p_value >= 0.05 else "✗ NO es normal"
        else:
            es_normal = "? Insuficientes datos"
        
        # Estadísticas descriptivas
        media = np.mean(datos)
        mediana = np.median(datos)
        std = np.std(datos, ddof=1) if n > 1 else np.nan
        min_val = np.min(datos)
        max_val = np.max(datos)
        
        # Guardar resultado
        resultados_12.append({
            'nivel': 'N=12',
            'metrica': metrica,
            'grupo': grupo,
            'n': n,
            'W_statistic': W_stat,
            'p_value': p_value,
            'es_normal': es_normal,
            'media': media,
            'mediana': mediana,
            'std': std,
            'min': min_val,
            'max': max_val
        })
        
        print(f"\n  Grupo: {grupo} (N={n})")
        print(f"  ├─ W-statistic: {W_stat:.6f}")
        print(f"  ├─ p-value: {p_value:.8f}")
        print(f"  ├─ Resultado: {es_normal}")
        print(f"  ├─ Media: {media:.6f}")
        print(f"  ├─ Mediana: {mediana:.6f}")
        print(f"  ├─ Std Dev: {std:.6f}")
        print(f"  ├─ Min: {min_val:.6f}")
        print(f"  └─ Max: {max_val:.6f}")

# ==================================================================================
# RESUMEN COMPARATIVO
# ==================================================================================

print("\n" + "=" * 100)
print("RESUMEN COMPARATIVO: N=2,480 vs N=12")
print("=" * 100)

# Crear DataFrames con resultados
df_res_2480 = pd.DataFrame(resultados_2480)
df_res_12 = pd.DataFrame(resultados_12)

# Tabla comparativa para cada métrica
for metrica in METRICAS:
    print(f"\n╔{'═' * 96}╗")
    print(f"║ {metrica:<94}║")
    print(f"╚{'═' * 96}╝")
    
    print(f"\n{metrica} - N=2,480 (EXPLORACIÓN):")
    print("┌──────────┬──────────┬────────────────┬────────────────────────────┐")
    print("│  Grupo   │    N     │   W-statistic  │      p-value / Resultado   │")
    print("├──────────┼──────────┼────────────────┼────────────────────────────┤")
    
    for _, row in df_res_2480[df_res_2480['metrica'] == metrica].iterrows():
        print(f"│ {row['grupo']:<8} │ {row['n']:>6}    │ {row['W_statistic']:>14.6f} │ {row['p_value']:.8f} {row['es_normal']:>6} │")
    
    print("└──────────┴──────────┴────────────────┴────────────────────────────┘")
    
    print(f"\n{metrica} - N=12 (ANÁLISIS RIGUROSO):")
    print("┌──────────┬──────────┬────────────────┬────────────────────────────┐")
    print("│  Grupo   │    N     │   W-statistic  │      p-value / Resultado   │")
    print("├──────────┼──────────┼────────────────┼────────────────────────────┤")
    
    for _, row in df_res_12[df_res_12['metrica'] == metrica].iterrows():
        print(f"│ {row['grupo']:<8} │ {row['n']:>6}    │ {row['W_statistic']:>14.6f} │ {row['p_value']:.8f} {row['es_normal']:>6} │")
    
    print("└──────────┴──────────┴────────────────┴────────────────────────────┘")

# ==================================================================================
# MATRIZ DE DECISIONES PARA PASO 2 Y 3
# ==================================================================================

print("\n" + "=" * 100)
print("MATRIZ DE DECISIONES PARA PASOS SIGUIENTES")
print("=" * 100)

print("\nBasado en Shapiro-Wilk (N=12), decidiremos qué test usar:")
print("\n┌────────────────────┬──────────────────┬─────────────────────────────────┐")
print("│      Métrica       │   ¿Es Normal?    │    Test a usar en Paso 3        │")
print("│                    │   (Shapiro N=12) │    (Hipótesis Manual vs IA)     │")
print("├────────────────────┼──────────────────┼─────────────────────────────────┤")

for metrica in METRICAS:
    # Revisar si ambos grupos son normales en N=12
    datos_normal_12 = df_res_12[df_res_12['metrica'] == metrica]
    
    # Verificar grupo Manual
    manual_data = datos_normal_12[datos_normal_12['grupo'] == 'Manual']
    manual_normal = manual_data['p_value'].values[0] >= 0.05 if len(manual_data) > 0 else False
    
    # Verificar grupo IA
    ia_data = datos_normal_12[datos_normal_12['grupo'] == 'IA']
    ia_normal = ia_data['p_value'].values[0] >= 0.05 if len(ia_data) > 0 else False
    
    # Si solo hay Manual o si ambos son normales
    if len(ia_data) == 0:  # Solo Manual disponible
        ambos_normal = f"Manual: {'✓' if manual_normal else '✗'}"
        test_a_usar = "t-Student (asumiendo IA igual)" if manual_normal else "Mann-Whitney U (asumiendo IA igual)"
    elif manual_normal and ia_normal:
        ambos_normal = "✓ SÍ (ambos)"
        test_a_usar = "t-Student"
    else:
        ambos_normal = "✗ NO"
        test_a_usar = "Mann-Whitney U"
    
    print(f"│ {metrica:<18} │ {ambos_normal:<16} │ {test_a_usar:<29} │")

print("└────────────────────┴──────────────────┴─────────────────────────────┘")

# ==================================================================================
# GUARDAR RESULTADOS EN EXCEL
# ==================================================================================

print("\n" + "=" * 100)
print("GUARDANDO RESULTADOS...")
print("=" * 100)

archivo_excel = RUTA_BASE / "01_PASO1_NORMALIDAD_SHAPIRO_WILK.xlsx"

try:
    with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
        df_res_2480.to_excel(writer, sheet_name='Shapiro_N2480', index=False)
        df_res_12.to_excel(writer, sheet_name='Shapiro_N12', index=False)
    
    print(f"\n✓ Archivo guardado: {archivo_excel}")
except ImportError:
    print("\n! Openpyxl no instalado, guardando como CSV...")
    df_res_2480.to_csv(RUTA_BASE / "01_PASO1_NORMALIDAD_N2480.csv", index=False)
    df_res_12.to_csv(RUTA_BASE / "01_PASO1_NORMALIDAD_N12.csv", index=False)
    print("✓ Archivos CSV guardados")

# ==================================================================================
# CONCLUSIONES
# ==================================================================================

print("\n" + "=" * 100)
print("CONCLUSIONES PASO 1")
print("=" * 100)

print("""
1. NIVEL N=2,480 (EXPLORACIÓN):
   └─ Muestra la distribución REAL de todos los datos
   └─ Esperado: TODOS rechazan normalidad (p < 0.05)
   └─ Razón: "Escalones" por 40 replicas por test
   └─ Uso: Para gráficos informativos en Capítulo 4

2. NIVEL N=12 (RIGUROSO) ← LO MÁS IMPORTANTE:
   └─ Cada test es una observación INDEPENDIENTE
   └─ Esperado: MIXTO (algunas normales, otras no)
   └─ Resultado: Define qué test usar en Paso 3
   └─ Uso: Para conclusiones rigurosas del análisis

3. PRÓXIMO PASO:
   └─ Realizaremos Levene (homogeneidad de varianzas)
   └─ Luego ejecutaremos prueba de hipótesis
   └─ Usaremos resultados de Shapiro para decidir

════════════════════════════════════════════════════════════════════════════════════════════════
""")

print("=" * 100)
print("FIN PASO 1 - NORMALIDAD (SHAPIRO-WILK)")
print("=" * 100)
