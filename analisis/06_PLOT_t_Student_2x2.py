#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
06_PLOT_t_Student_2x2.py
Genera gráfico 2x2 con box plots para t-Student (N=12)
Muestra medias, desviaciones estándar, p-values y Cohen's d
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuración
ROOT = Path(__file__).resolve().parent
CSV = ROOT / 'datos_consolidados.csv'
EXCEL_RESULTADOS = ROOT / '03_PASO3_HIPOTESIS_T_STUDENT.xlsx'
OUT_DIR = ROOT / 'figures'
OUT_DIR.mkdir(exist_ok=True)

METRICAS = ['instr_pct', 'branch_pct', 'mutation_score', 'time_seconds']
LABELS = ['Instruction Coverage (%)', 'Branch Coverage (%)', 
          'Mutation Score (%)', 'Time (seconds)']

DPI = 300
COLORBLIND_BLUE = '#87CEEB'  # Celeste para Manual
COLORBLIND_RED = '#FF8C00'   # Naranja para IA

print("="*80)
print("GENERANDO GRÁFICO 2×2: t-Student (N=12) - Box Plots")
print("="*80)

# Cargar datos
print("\n[1/3] Cargando datos...")
df = pd.read_csv(CSV)
df_promedios = df.groupby(['group', 'test_name'])[METRICAS].mean().reset_index()
print(f"  ✓ Datos: {len(df)} registros")
print(f"  ✓ Promedios: {len(df_promedios)} tests (N=12)")

# Cargar resultados t-Student
print("\n[2/3] Cargando resultados t-Student...")
df_t_student = pd.read_excel(EXCEL_RESULTADOS, sheet_name='Hipotesis_N12')

# Crear mapping de resultados
t_results = {}
for _, row in df_t_student.iterrows():
    metrica = row['Metrica']
    # Usar t_statistic_welch solo para Time, pero p_value_std para todos
    usar_t_welch = metrica == 'Time (seconds)'
    t_results[metrica] = {
        'p_value': row['p_value_std'],  # Siempre usar p_value_std
        'cohens_d': row['Cohens_d'],
        't_stat': row['t_statistic_welch'] if usar_t_welch else row['t_statistic_std'],
        'media_manual': row['Media_Manual'],
        'media_ia': row['Media_IA'],
        'std_manual': row['SD_Manual'],
        'std_ia': row['SD_IA']
    }

print(f"  ✓ Resultados cargados para {len(t_results)} métricas")

# Crear figura 2x2
print("\n[3/3] Generando gráfico 2×2...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('t-Student Analysis (N=12): Box Plots with Statistical Results', 
             fontsize=16, fontweight='bold', y=0.995)

axes = axes.flatten()

for idx, (metrica, label) in enumerate(zip(METRICAS, LABELS)):
    ax = axes[idx]
    
    # Preparar datos para seaborn
    datos_manual = df_promedios[df_promedios['group'] == 'Manual'][metrica].values
    datos_ia = df_promedios[df_promedios['group'] == 'IA'][metrica].values
    
    plot_data = pd.concat([
        pd.DataFrame({'Valor': datos_manual, 'Grupo': 'Manual'}),
        pd.DataFrame({'Valor': datos_ia, 'Grupo': 'IA'})
    ])
    
    # Box plot
    sns.boxplot(data=plot_data, x='Grupo', y='Valor', ax=ax, 
                palette={'Manual': COLORBLIND_BLUE, 'IA': COLORBLIND_RED},
                width=0.6)
    
    # Agregar puntos individuales (jitter)
    sns.stripplot(data=plot_data, x='Grupo', y='Valor', ax=ax, 
                  color='black', alpha=0.4, size=6, jitter=True)
    
    # Obtener resultados (buscar por label en t_results)
    res = None
    for key in t_results.keys():
        if label.split('(')[0].strip().lower() in key.lower():
            res = t_results[key]
            break
    
    if res is None:
        print(f"  ! Advertencia: No se encontró resultado para {label}")
        continue
    
    p_val = res['p_value']
    cohens_d = res['cohens_d']
    t_stat = res['t_stat']
    
    # Significancia
    sig_stars = "ns" if p_val >= 0.05 else "*" if p_val < 0.05 else "**" if p_val < 0.01 else "***"
    
    # Formatear título con estadísticas (sin redondear como en Excel)
    titulo = f'{label}\n'
    titulo += f't={t_stat:.6f}, p={p_val:.6f} ({sig_stars}), d={cohens_d:.6f}'
    
    # Agregar texto con medias y desviaciones debajo del título
    stats_text = f'Manual: μ={res["media_manual"]:.6f}±{res["std_manual"]:.6f}  |  AI: μ={res["media_ia"]:.6f}±{res["std_ia"]:.6f}'
    titulo += f'\n{stats_text}'
    
    ax.set_title(titulo, fontsize=10, fontweight='bold')
    ax.set_ylabel('Value', fontsize=10)
    ax.set_xlabel('Group', fontsize=10)
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()

# Guardar figura
output_file = OUT_DIR / '06_t_Student_2x2.png'
plt.savefig(output_file, dpi=DPI, bbox_inches='tight')
print(f"\n✓ Figura guardada: {output_file}")

# También guardar PDF
output_pdf = OUT_DIR / '06_t_Student_2x2.pdf'
plt.savefig(output_pdf, bbox_inches='tight')
print(f"✓ Figura PDF guardada: {output_pdf}")

plt.close()

print("\n" + "="*80)
print("GRÁFICO 2×2 COMPLETADO")
print("="*80)
