#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PASO 3: PRUEBA DE HIPÓTESIS - t-Student
=======================================
Comparación Manual vs IA
Cálculo de Cohen's d (tamaño de efecto)
"""

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
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
print("PASO 3: PRUEBA DE HIPÓTESIS - t-Student y Cohen's d")
print("=" * 100)
print("\nPASO 0: Cargando datos consolidados...")

archivo_consolidado = RUTA_BASE / "datos_consolidados.csv"
df_consolidated = pd.read_csv(archivo_consolidado)

print(f"  ✓ Total registros: {len(df_consolidated)}")
print(f"  ✓ Grupos: {df_consolidated['group'].unique()}")

# ==================================================================================
# FUNCIÓN: Calcular Cohen's d
# ==================================================================================

def calcular_cohens_d(grupo1, grupo2):
    """
    Calcula Cohen's d (tamaño de efecto)
    Fórmula: d = (media1 - media2) / std_pooled
    
    Interpretación:
    d < 0.2: Efecto pequeño
    0.2 <= d < 0.5: Efecto pequeño-mediano
    0.5 <= d < 0.8: Efecto mediano
    d >= 0.8: Efecto grande
    """
    n1, n2 = len(grupo1), len(grupo2)
    media1, media2 = np.mean(grupo1), np.mean(grupo2)
    std1, std2 = np.std(grupo1, ddof=1), np.std(grupo2, ddof=1)
    
    # Desviación estándar combinada (pooled)
    std_pooled = np.sqrt(((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2))
    
    # Cohen's d
    cohens_d = (media1 - media2) / std_pooled if std_pooled > 0 else 0
    
    return cohens_d

def interpretar_cohens_d(d):
    """Interpreta el valor de Cohen's d"""
    d_abs = abs(d)
    if d_abs < 0.2:
        return "Efecto negligible"
    elif d_abs < 0.5:
        return "Efecto pequeño"
    elif d_abs < 0.8:
        return "Efecto mediano"
    else:
        return "Efecto grande"

# ==================================================================================
# PASO 3A: t-Student EN N=12 (ANÁLISIS RIGUROSO)
# ==================================================================================

print("\n" + "=" * 100)
print("PASO 3A: t-Student (ANÁLISIS RIGUROSO) - N=12")
print("=" * 100)

# Calcular promedios por test
df_promedios = df_consolidated.groupby(['group', 'test_name'])[METRICAS].mean().reset_index()

print(f"\nTests encontrados: {len(df_promedios)}")
print(f"  Manual: {len(df_promedios[df_promedios['group'] == 'Manual'])}")
print(f"  IA: {len(df_promedios[df_promedios['group'] == 'IA'])}")

resultados_hipotesis = []

for metrica in METRICAS:
    print(f"\n╔{'═' * 96}╗")
    print(f"║ Métrica: {metrica:<85}║")
    print(f"╚{'═' * 96}╝")
    
    # Obtener datos por grupo (N=12)
    datos_ia = df_promedios[df_promedios['group'] == 'IA'][metrica].values
    datos_manual = df_promedios[df_promedios['group'] == 'Manual'][metrica].values
    
    # Estadísticas descriptivas
    n_ia, n_manual = len(datos_ia), len(datos_manual)
    media_ia = np.mean(datos_ia)
    media_manual = np.mean(datos_manual)
    std_ia = np.std(datos_ia, ddof=1)
    std_manual = np.std(datos_manual, ddof=1)
    
    print(f"\n  Estadísticas Descriptivas:")
    print(f"  ├─ Manual (n={n_manual}): Media={media_manual:.6f}, Std={std_manual:.6f}")
    print(f"  └─ IA (n={n_ia}): Media={media_ia:.6f}, Std={std_ia:.6f}")
    
    # Diferencia de medias
    diferencia = media_manual - media_ia
    pct_diferencia = (diferencia / media_ia * 100) if media_ia != 0 else 0
    
    print(f"\n  Diferencia:")
    print(f"  ├─ Media Manual - Media IA: {diferencia:.6f}")
    print(f"  └─ Porcentaje de diferencia: {pct_diferencia:.2f}%")
    
    # Ejecutar t-Student
    # Verificar si usar estándar o Welch según Levene
    if metrica == 'time_seconds':
        # Levene rechazó igualdad → Welch
        t_stat, p_value = ttest_ind(datos_manual, datos_ia, equal_var=False)
        test_usado = "t-Student Welch"
    else:
        # Levene aceptó igualdad → t-Student estándar
        t_stat, p_value = ttest_ind(datos_manual, datos_ia, equal_var=True)
        test_usado = "t-Student (estándar)"
    
    # Significancia estadística
    es_significativo = "✓ SÍ (p < 0.05)" if p_value < 0.05 else "✗ NO (p ≥ 0.05)"
    
    print(f"\n  Prueba de Hipótesis ({test_usado}):")
    print(f"  ├─ t-statistic: {t_stat:.6f}")
    print(f"  ├─ p-value: {p_value:.8f}")
    print(f"  ├─ Significativo: {es_significativo}")
    print(f"  └─ H0: μ_Manual = μ_IA")
    
    # Cohen's d
    cohens_d = calcular_cohens_d(datos_manual, datos_ia)
    interpretacion_d = interpretar_cohens_d(cohens_d)
    
    print(f"\n  Tamaño de Efecto (Cohen's d):")
    print(f"  ├─ Cohen's d: {cohens_d:.6f}")
    print(f"  └─ Interpretación: {interpretacion_d}")
    
    # Dirección del efecto
    if diferencia > 0:
        direccion = "Manual > IA"
    elif diferencia < 0:
        direccion = "Manual < IA"
    else:
        direccion = "Manual = IA"
    
    print(f"\n  Conclusión:")
    print(f"  ├─ Dirección: {direccion}")
    print(f"  ├─ Magnitud: {abs(cohens_d):.3f}")
    print(f"  └─ Resumen: Diferencia {'SIGNIFICATIVA' if p_value < 0.05 else 'NO SIGNIFICATIVA'} ({interpretacion_d})")
    
    resultados_hipotesis.append({
        'metrica': metrica,
        'n_manual': n_manual,
        'n_ia': n_ia,
        'media_manual': media_manual,
        'media_ia': media_ia,
        'std_manual': std_manual,
        'std_ia': std_ia,
        'diferencia_medias': diferencia,
        'pct_diferencia': pct_diferencia,
        't_statistic': t_stat,
        'p_value': p_value,
        'es_significativo': es_significativo,
        'test_usado': test_usado,
        'cohens_d': cohens_d,
        'interpretacion_d': interpretacion_d,
        'direccion': direccion
    })

# ==================================================================================
# TABLA RESUMEN
# ==================================================================================

print("\n" + "=" * 100)
print("TABLA RESUMEN - RESULTADOS DE HIPÓTESIS")
print("=" * 100)

df_resultados = pd.DataFrame(resultados_hipotesis)

print("\n┌────────────────┬──────────────┬──────────────┬─────────────┬──────────────┐")
print("│    Métrica     │  Manual      │      IA      │  p-value   │  Cohen's d   │")
print("│                │   (Media)    │    (Media)   │            │              │")
print("├────────────────┼──────────────┼──────────────┼─────────────┼──────────────┤")

for _, row in df_resultados.iterrows():
    metrica = row['metrica']
    media_manual = row['media_manual']
    media_ia = row['media_ia']
    p_value = row['p_value']
    cohens_d = row['cohens_d']
    
    sig = "✓" if p_value < 0.05 else "✗"
    
    print(f"│ {metrica:<14} │ {media_manual:>12.4f} │ {media_ia:>12.4f} │ {p_value:>9.6f} {sig} │ {cohens_d:>12.4f} │")

print("└────────────────┴──────────────┴──────────────┴─────────────┴──────────────┘")

print("\n┌────────────────┬──────────────────────┬──────────────────────────────────┐")
print("│    Métrica     │   Diferencia (%)     │      Interpretación              │")
print("├────────────────┼──────────────────────┼──────────────────────────────────┤")

for _, row in df_resultados.iterrows():
    metrica = row['metrica']
    pct = row['pct_diferencia']
    interpretacion = row['interpretacion_d']
    direccion = row['direccion']
    
    print(f"│ {metrica:<14} │ {pct:>18.2f}% │ {direccion}: {interpretacion:<18} │")

print("└────────────────┴──────────────────────┴──────────────────────────────────┘")

# ==================================================================================
# GUARDAR RESULTADOS EN EXCEL
# ==================================================================================

print("\n" + "=" * 100)
print("GUARDANDO RESULTADOS...")
print("=" * 100)

archivo_excel = RUTA_BASE / "03_PASO3_HIPOTESIS_T_STUDENT.xlsx"

try:
    with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
        df_resultados.to_excel(writer, sheet_name='Hipotesis_N12', index=False)
    
    print(f"\n✓ Archivo guardado: {archivo_excel}")
except ImportError:
    print("\n! Openpyxl no instalado, guardando como CSV...")
    df_resultados.to_csv(RUTA_BASE / "03_PASO3_HIPOTESIS_T_STUDENT.csv", index=False)
    print("✓ Archivo CSV guardado")

# ==================================================================================
# CONCLUSIONES FINALES
# ==================================================================================

print("\n" + "=" * 100)
print("CONCLUSIONES PASO 3 - ANÁLISIS FINAL")
print("=" * 100)

print("""
RESUMEN DE HALLAZGOS:
═════════════════════

""")

for _, row in df_resultados.iterrows():
    metrica = row['metrica']
    p_value = row['p_value']
    es_sig = "✓ SIGNIFICATIVA" if p_value < 0.05 else "✗ NO SIGNIFICATIVA"
    diferencia = row['pct_diferencia']
    direccion = row['direccion']
    interpretacion = row['interpretacion_d']
    
    print(f"{metrica}:")
    print(f"  • Diferencia: {es_sig}")
    print(f"  • Dirección: {direccion} ({abs(diferencia):.2f}%)")
    print(f"  • Magnitud: {interpretacion}")
    print(f"  • p-value: {p_value:.8f}")
    print()

# ==================================================================================
# INTERPRETACIÓN SEGÚN HIPÓTESIS DE INVESTIGACIÓN
# ==================================================================================

print("=" * 100)
print("INTERPRETACIÓN SEGÚN HIPÓTESIS DE INVESTIGACIÓN")
print("=" * 100)

print("""
Hipótesis Nula (H0): No hay diferencias significativas entre pruebas Manual e IA
Hipótesis Alternativa (H1): Hay diferencias significativas entre pruebas Manual e IA

RESULTADOS:
""")

for _, row in df_resultados.iterrows():
    metrica = row['metrica']
    p_value = row['p_value']
    
    if p_value < 0.05:
        resultado = "✓ Rechazamos H0 → Hay diferencia significativa"
    else:
        resultado = "✗ No rechazamos H0 → No hay diferencia significativa"
    
    print(f"  {metrica}: {resultado} (p={p_value:.8f})")

print("\n" + "=" * 100)
print("FIN PASO 3 - PRUEBA DE HIPÓTESIS (t-Student)")
print("=" * 100)
