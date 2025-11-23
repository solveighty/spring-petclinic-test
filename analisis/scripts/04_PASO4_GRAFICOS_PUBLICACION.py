#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASO 4: GENERACIÓN DE GRÁFICOS PARA PUBLICACIÓN
================================================

Script para generar 6 figuras de publicación-quality (300 DPI) para el Capítulo 4
- Figura 1: Histogramas (N=2,480)
- Figura 2: Box plots (N=2,480)
- Figura 3: Q-Q plots para normalidad (N=12)
- Figura 4: Levene p-values (N=12)
- Figura 6: Bar plots con IC 95% (N=12)
- Figura 7: Cohen's d (N=12)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, levene
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN GLOBAL
# ─────────────────────────────────────────────────────────────────────────────

DPI_OUTPUT = 300
COLORBLIND_BLUE = '#1f77b4'
COLORBLIND_RED = '#d62728'
COLORBLIND_GREEN = '#2ca02c'
COLORBLIND_GRAY = '#7f7f7f'
COLORBLIND_YELLOW = '#bcbd22'

sns.set_style("darkgrid")
METRICAS = ['instr_pct', 'branch_pct', 'mutation_score', 'time_seconds']
LABELS_METRICAS = ['Instruction Coverage (%)', 'Branch Coverage (%)', 
                   'Mutation Score', 'Time (seconds)']

print("=" * 100)
print("PASO 4: GENERACIÓN DE GRÁFICOS PARA PUBLICACIÓN")
print("=" * 100)

# ─────────────────────────────────────────────────────────────────────────────
# CARGAR DATOS
# ─────────────────────────────────────────────────────────────────────────────

print("\n[PASO 0] Cargando datos...")

df = pd.read_csv('datos_consolidados.csv')
print(f"  ✓ Datos consolidados: {len(df)} registros")

# Promedios por test (N=12)
df_promedios_raw = df.groupby('test_name')[METRICAS].mean().reset_index()
df_group = df.groupby('test_name')['group'].first().reset_index()
df_promedios = df_promedios_raw.merge(df_group, on='test_name')
print(f"  ✓ Promedios por test: {len(df_promedios)} tests")

datos_n12 = {
    'Manual': df_promedios[df_promedios['group'] == 'Manual'],
    'IA': df_promedios[df_promedios['group'] == 'IA']
}

# Cargar t-Student
excel_paso3 = pd.read_excel('03_PASO3_HIPOTESIS_T_STUDENT.xlsx', sheet_name=0)
t_student_dict = {}
for _, row in excel_paso3.iterrows():
    metrica = row['metrica']
    t_student_dict[metrica] = {
        't_stat': row['t_statistic'],
        'p_value': row['p_value'],
        'cohens_d': row['cohens_d']
    }
print(f"  ✓ Resultados t-Student cargados")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURA 1: HISTOGRAMAS (N=2,480)
# ─────────────────────────────────────────────────────────────────────────────

print("\n[FIGURA 1] Generando histogramas...")

fig1, axes1 = plt.subplots(2, 2, figsize=(14, 10))
fig1.suptitle('Figure 1: Distribution of Test Metrics (N=2,480)', 
              fontsize=16, fontweight='bold', y=0.995)

for idx, metrica in enumerate(METRICAS):
    ax = axes1[idx // 2, idx % 2]
    
    datos_manual = df[df['group'] == 'Manual'][metrica]
    datos_ia = df[df['group'] == 'IA'][metrica]
    
    ax.hist(datos_manual, bins=30, alpha=0.6, label='Manual', 
            color=COLORBLIND_BLUE, edgecolor='black', linewidth=0.5)
    ax.hist(datos_ia, bins=30, alpha=0.6, label='AI', 
            color=COLORBLIND_RED, edgecolor='black', linewidth=0.5)
    
    media_manual = datos_manual.mean()
    media_ia = datos_ia.mean()
    
    ax.axvline(media_manual, color=COLORBLIND_BLUE, linestyle='--', linewidth=2, 
               label=f'Manual μ={media_manual:.2f}')
    ax.axvline(media_ia, color=COLORBLIND_RED, linestyle='--', linewidth=2, 
               label=f'AI μ={media_ia:.2f}')
    
    ax.set_xlabel(LABELS_METRICAS[idx], fontsize=11, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9, loc='best')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Figura_1_Histogramas.png', dpi=DPI_OUTPUT, bbox_inches='tight')
plt.savefig('Figura_1_Histogramas.pdf', bbox_inches='tight')
print("  ✓ Figura 1 guardada")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# FIGURA 2: BOX PLOTS (N=2,480)
# ─────────────────────────────────────────────────────────────────────────────

print("\n[FIGURA 2] Generando box plots...")

fig2, axes2 = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle('Figure 2: Box Plots Comparing Manual vs AI (N=2,480)', 
              fontsize=16, fontweight='bold', y=0.995)

for idx, metrica in enumerate(METRICAS):
    ax = axes2[idx // 2, idx % 2]
    
    data_to_plot = [df[df['group'] == 'Manual'][metrica],
                     df[df['group'] == 'IA'][metrica]]
    
    bp = ax.boxplot(data_to_plot, labels=['Manual', 'AI'], patch_artist=True,
                    widths=0.6, showmeans=True,
                    meanprops=dict(marker='D', markerfacecolor='red', markeredgecolor='red', markersize=8))
    
    colors = [COLORBLIND_BLUE, COLORBLIND_RED]
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_ylabel(LABELS_METRICAS[idx], fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('Figura_2_BoxPlots.png', dpi=DPI_OUTPUT, bbox_inches='tight')
plt.savefig('Figura_2_BoxPlots.pdf', bbox_inches='tight')
print("  ✓ Figura 2 guardada")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# FIGURA 3: Q-Q PLOTS (N=12)
# ─────────────────────────────────────────────────────────────────────────────

print("\n[FIGURA 3] Generando Q-Q plots...")

fig3, axes3 = plt.subplots(2, 4, figsize=(16, 10))
fig3.suptitle('Figure 3: Q-Q Plots for Normality Validation (N=12)', 
              fontsize=16, fontweight='bold', y=0.995)

for idx, metrica in enumerate(METRICAS):
    # Manual
    ax_m = axes3[0, idx]
    datos_manual = datos_n12['Manual'][metrica].values
    stats.probplot(datos_manual, dist="norm", plot=ax_m)
    
    w_m, p_m = shapiro(datos_manual)
    ax_m.set_title(f'Manual - {LABELS_METRICAS[idx]}\nShapiro-Wilk: p={p_m:.4f}', 
                   fontsize=10, fontweight='bold')
    ax_m.grid(True, alpha=0.3)
    
    # IA
    ax_i = axes3[1, idx]
    datos_ia = datos_n12['IA'][metrica].values
    stats.probplot(datos_ia, dist="norm", plot=ax_i)
    
    w_i, p_i = shapiro(datos_ia)
    ax_i.set_title(f'AI - {LABELS_METRICAS[idx]}\nShapiro-Wilk: p={p_i:.4f}', 
                   fontsize=10, fontweight='bold')
    ax_i.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Figura_3_QQPlots.png', dpi=DPI_OUTPUT, bbox_inches='tight')
plt.savefig('Figura_3_QQPlots.pdf', bbox_inches='tight')
print("  ✓ Figura 3 guardada")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# FIGURA 4: LEVENE TEST (N=12)
# ─────────────────────────────────────────────────────────────────────────────

print("\n[FIGURA 4] Generando gráfico Levene...")

fig4, ax4 = plt.subplots(figsize=(12, 6))

levene_pvalues = []
levene_labels = []

for metrica in METRICAS:
    stat, pval = levene(datos_n12['Manual'][metrica],
                        datos_n12['IA'][metrica])
    levene_pvalues.append(pval)
    levene_labels.append(metrica.replace('_', ' ').title())

colors_levene = [COLORBLIND_BLUE if p >= 0.05 else COLORBLIND_RED 
                 for p in levene_pvalues]
bars = ax4.bar(range(len(METRICAS)), levene_pvalues, color=colors_levene, 
               edgecolor='black', linewidth=1.5, alpha=0.8)

ax4.axhline(y=0.05, color='red', linestyle='--', linewidth=2, label='α = 0.05')

ax4.set_xticks(range(len(METRICAS)))
ax4.set_xticklabels(levene_labels, fontsize=11, fontweight='bold')
ax4.set_ylabel('p-value', fontsize=12, fontweight='bold')
ax4.set_title('Figure 4: Levene Test for Homogeneity of Variances (N=12)', 
              fontsize=14, fontweight='bold', pad=20)
ax4.set_ylim(0, 1.0)
ax4.grid(True, alpha=0.3, axis='y')
ax4.legend(fontsize=11)

for i, (bar, pval) in enumerate(zip(bars, levene_pvalues)):
    height = bar.get_height()
    status = "Equal" if pval >= 0.05 else "Unequal"
    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.03,
             f'p={pval:.4f}\n{status}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('Figura_4_Levene.png', dpi=DPI_OUTPUT, bbox_inches='tight')
plt.savefig('Figura_4_Levene.pdf', bbox_inches='tight')
print("  ✓ Figura 4 guardada")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# FIGURA 6: BAR PLOTS CON IC 95% (N=12)
# ─────────────────────────────────────────────────────────────────────────────

print("\n[FIGURA 6] Generando bar plots con IC 95%...")

fig6, axes6 = plt.subplots(2, 2, figsize=(14, 11))
fig6.suptitle('Figure 6: Means with 95% Confidence Intervals (N=12)', 
              fontsize=16, fontweight='bold', y=0.995)

for idx, metrica in enumerate(METRICAS):
    ax = axes6[idx // 2, idx % 2]
    
    manual_data = datos_n12['Manual'][metrica].values
    ia_data = datos_n12['IA'][metrica].values
    
    n_manual = len(manual_data)
    n_ia = len(ia_data)
    
    mean_manual = manual_data.mean()
    se_manual = manual_data.std() / np.sqrt(n_manual)
    ci_manual = 1.96 * se_manual
    
    mean_ia = ia_data.mean()
    se_ia = ia_data.std() / np.sqrt(n_ia)
    ci_ia = 1.96 * se_ia
    
    x_pos = np.arange(2)
    means = [mean_manual, mean_ia]
    errors = [ci_manual, ci_ia]
    
    bars = ax.bar(x_pos, means, yerr=errors, capsize=10, 
                  color=[COLORBLIND_BLUE, COLORBLIND_RED],
                  edgecolor='black', linewidth=1.5, alpha=0.8,
                  error_kw={'linewidth': 2, 'ecolor': 'black'})
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(['Manual', 'AI'], fontsize=11, fontweight='bold')
    ax.set_ylabel(LABELS_METRICAS[idx], fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    t_data = t_student_dict.get(metrica, {})
    title_text = f'{LABELS_METRICAS[idx]}\nt={t_data.get("t_stat", 0):.3f}, p={t_data.get("p_value", 0):.4f}, d={t_data.get("cohens_d", 0):.3f}'
    ax.set_title(title_text, fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('Figura_6_BarplotsIC95.png', dpi=DPI_OUTPUT, bbox_inches='tight')
plt.savefig('Figura_6_BarplotsIC95.pdf', bbox_inches='tight')
print("  ✓ Figura 6 guardada")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# FIGURA 7: COHEN'S D (N=12)
# ─────────────────────────────────────────────────────────────────────────────

print("\n[FIGURA 7] Generando gráfico Cohen's d...")

fig7, ax7 = plt.subplots(figsize=(11, 7))

cohens_d_values = []
for metrica in METRICAS:
    d_value = t_student_dict.get(metrica, {}).get('cohens_d', 0)
    cohens_d_values.append(d_value)

def get_color_cohens_d(d):
    abs_d = abs(d)
    if abs_d < 0.2:
        return COLORBLIND_GRAY
    elif abs_d < 0.5:
        return COLORBLIND_GREEN
    elif abs_d < 0.8:
        return COLORBLIND_YELLOW
    else:
        return COLORBLIND_RED

colors_d = [get_color_cohens_d(d) for d in cohens_d_values]

y_pos = np.arange(len(METRICAS))
levene_labels_short = [m.replace('_', ' ').title() for m in METRICAS]
bars = ax7.barh(y_pos, cohens_d_values, color=colors_d, edgecolor='black', 
                linewidth=1.5, alpha=0.8)

ax7.axvline(x=0.2, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax7.axvline(x=-0.2, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax7.axvline(x=0.5, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax7.axvline(x=-0.5, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax7.axvline(x=0.8, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax7.axvline(x=-0.8, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax7.axvline(x=0, color='black', linewidth=2)

ax7.set_yticks(y_pos)
ax7.set_yticklabels(levene_labels_short, fontsize=11, fontweight='bold')
ax7.set_xlabel("Cohen's d (Effect Size)", fontsize=12, fontweight='bold')
ax7.set_title("Figure 7: Effect Sizes - Cohen's d (N=12)", fontsize=14, fontweight='bold', pad=20)
ax7.set_xlim(-1.2, 1.2)
ax7.grid(True, alpha=0.3, axis='x')

for i, (bar, d_val) in enumerate(zip(bars, cohens_d_values)):
    width = bar.get_width()
    abs_d = abs(d_val)
    if abs_d < 0.2:
        effect = "Negligible"
    elif abs_d < 0.5:
        effect = "Small"
    elif abs_d < 0.8:
        effect = "Medium"
    else:
        effect = "Large"
    
    x_text = width + (0.05 if width > 0 else -0.05)
    ha_text = 'left' if width > 0 else 'right'
    
    ax7.text(x_text, bar.get_y() + bar.get_height()/2.,
             f' {d_val:.3f}\n{effect}',
             ha=ha_text, va='center', fontsize=10, fontweight='bold')

legend_elements = [
    plt.Rectangle((0, 0), 1, 1, fc=COLORBLIND_GRAY, ec='black', label='|d| < 0.2 (Negligible)'),
    plt.Rectangle((0, 0), 1, 1, fc=COLORBLIND_GREEN, ec='black', label='0.2 ≤ |d| < 0.5 (Small)'),
    plt.Rectangle((0, 0), 1, 1, fc=COLORBLIND_YELLOW, ec='black', label='0.5 ≤ |d| < 0.8 (Medium)'),
    plt.Rectangle((0, 0), 1, 1, fc=COLORBLIND_RED, ec='black', label='|d| ≥ 0.8 (Large)')
]
ax7.legend(handles=legend_elements, loc='lower right', fontsize=10)

plt.tight_layout()
plt.savefig('Figura_7_CohenD.png', dpi=DPI_OUTPUT, bbox_inches='tight')
plt.savefig('Figura_7_CohenD.pdf', bbox_inches='tight')
print("  ✓ Figura 7 guardada")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# RESUMEN FINAL
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 100)
print("✓ TODAS LAS FIGURAS GENERADAS EXITOSAMENTE")
print("=" * 100)
print("""
Figuras generadas (PNG + PDF a 300 DPI):
  ✓ Figura_1_Histogramas - Distribuciones (N=2,480)
  ✓ Figura_2_BoxPlots - Box plots (N=2,480)
  ✓ Figura_3_QQPlots - Q-Q plots (N=12)
  ✓ Figura_4_Levene - Levene p-values (N=12)
  ✓ Figura_6_BarplotsIC95 - Medias con IC 95% (N=12)
  ✓ Figura_7_CohenD - Effect sizes (N=12)

SIGUIENTES PASOS:
  - PASO 5: Crear consolidado Excel con todas las tablas
  - PASO 6: Redactar Capítulo 4
""")

print("=" * 100)
