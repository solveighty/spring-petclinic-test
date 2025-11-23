#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
07_PLOT_Mann_Whitney_2x2.py
Genera gráfico 2x2 con violin plots para Mann-Whitney U (N=2,480)
Muestra medianas, p-values y tamaño de efecto r
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuración
ROOT = Path(__file__).resolve().parent
CSV = ROOT / 'datos_consolidados.csv'
EXCEL_RESULTADOS = ROOT / '03_PASO3B_MANN_WHITNEY_U_N2480.xlsx'
OUT_DIR = ROOT / 'figures'
OUT_DIR.mkdir(exist_ok=True)

METRICAS = ['instr_pct', 'branch_pct', 'mutation_score', 'time_seconds']
LABELS = ['Instruction Coverage (%)', 'Branch Coverage (%)', 
          'Mutation Score (%)', 'Time (seconds)']

DPI = 300
COLORBLIND_BLUE = '#87CEEB'  # Celeste para Manual
COLORBLIND_RED = '#FF8C00'   # Naranja para IA

print("="*80)
print("GENERANDO GRÁFICO 2×2: Mann-Whitney U (N=2,480) - Violin Plots")
print("="*80)

# Cargar datos
print("\n[1/3] Cargando datos...")
df = pd.read_csv(CSV)
print(f"  ✓ Datos: {len(df)} registros")

# Cargar resultados Mann-Whitney U
print("\n[2/3] Cargando resultados Mann-Whitney U...")
df_mw = pd.read_excel(EXCEL_RESULTADOS, sheet_name='Mann_Whitney_N2480')

# Crear mapping de resultados
mw_results = {}
for _, row in df_mw.iterrows():
    metrica = row['Metrica']
    mw_results[metrica] = {
        'p_value': row['p_value'],
        'r_effect_size': row['r_effect_size'],
        'U_statistic': row['U_statistic'],
        'Z_score': row['Z_score'],
        'mediana_manual': row['Mediana_Manual'],
        'mediana_ia': row['Mediana_IA'],
        'media_manual': row['Media_Manual'],
        'media_ia': row['Media_IA']
    }

print(f"  ✓ Resultados cargados para {len(mw_results)} métricas")

# Crear figura 2x2
print("\n[3/3] Generando gráfico 2×2...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Mann-Whitney U Analysis (N=2,480): Violin Plots with Statistical Results', 
             fontsize=16, fontweight='bold', y=0.995)

axes = axes.flatten()

for idx, (metrica, label) in enumerate(zip(METRICAS, LABELS)):
    ax = axes[idx]
    
    # Preparar datos para seaborn
    datos_manual = df[df['group'] == 'Manual'][metrica].values
    datos_ia = df[df['group'] == 'IA'][metrica].values
    
    plot_data = pd.concat([
        pd.DataFrame({'Valor': datos_manual, 'Grupo': 'Manual'}),
        pd.DataFrame({'Valor': datos_ia, 'Grupo': 'AI'})
    ])
    
    # Violin plot
    sns.violinplot(data=plot_data, x='Grupo', y='Valor', ax=ax, 
                   palette={'Manual': COLORBLIND_BLUE, 'AI': COLORBLIND_RED},
                   inner='box', linewidth=1.5)
    
    # Obtener resultados (buscar por label en mw_results)
    res = None
    for key in mw_results.keys():
        if label.split('(')[0].strip().lower() in key.lower():
            res = mw_results[key]
            break
    
    if res is None:
        print(f"  ! Advertencia: No se encontró resultado para {label}")
        continue
    
    p_val = res['p_value']
    r_effect = res['r_effect_size']
    u_stat = res['U_statistic']
    z_score = res['Z_score']
    
    # Significancia
    if p_val < 0.001:
        sig_stars = "***"
    elif p_val < 0.01:
        sig_stars = "**"
    elif p_val < 0.05:
        sig_stars = "*"
    else:
        sig_stars = "ns"
    
    # Formatear título con estadísticas (sin redondear como en Excel)
    titulo = f'{label}\n'
    titulo += f'U={u_stat:.0f}, Z={z_score:.6f}, p={p_val:.6e}, r={r_effect:.6f}'
    
    # Agregar texto con medianas y medias debajo del título
    stats_text = f'Manual: Mdn={res["mediana_manual"]:.6f}, μ={res["media_manual"]:.6f}  |  AI: Mdn={res["mediana_ia"]:.6f}, μ={res["media_ia"]:.6f}'
    titulo += f'\n{stats_text}'
    
    ax.set_title(titulo, fontsize=10, fontweight='bold')
    ax.set_ylabel('Value', fontsize=10)
    ax.set_xlabel('Group', fontsize=10)
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()

# Guardar figura
output_file = OUT_DIR / '07_Mann_Whitney_2x2.png'
plt.savefig(output_file, dpi=DPI, bbox_inches='tight')
print(f"\n✓ Figura guardada: {output_file}")

# También guardar PDF
output_pdf = OUT_DIR / '07_Mann_Whitney_2x2.pdf'
plt.savefig(output_pdf, bbox_inches='tight')
print(f"✓ Figura PDF guardada: {output_pdf}")

plt.close()

print("\n" + "="*80)
print("GRÁFICO 2×2 COMPLETADO")
print("="*80)
