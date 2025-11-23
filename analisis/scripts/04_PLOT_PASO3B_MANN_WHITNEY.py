"""
04_PLOT_PASO3B_MANN_WHITNEY.py
Genera un gráfico 2x2 con boxplots y p-values de Mann-Whitney U
para las 4 métricas analizadas en PASO 3B. Guarda PNG y PDF en ./figures/

Uso: ejecutar desde la carpeta `analisis`:
    python 04_PLOT_PASO3B_MANN_WHITNEY.py

Requiere: pandas, scipy, matplotlib, seaborn
"""
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
import numpy as np

# Paths
ROOT = Path(__file__).resolve().parent
CSV = ROOT / 'datos_consolidados.csv'
OUT_DIR = ROOT / 'figures'
OUT_DIR.mkdir(exist_ok=True)

# Metrics to plot (column names expected in datos_consolidados.csv)
metrics = [
    ('instr_pct', 'Instruction Coverage (%)'),
    ('branch_pct', 'Branch Coverage (%)'),
    ('mutation_score', 'Mutation Score (%)'),
    ('time_seconds', 'Time (s)')
]

# Load data
if not CSV.exists():
    raise FileNotFoundError(f"No existe {CSV}. Ejecuta este script desde la carpeta 'analisis' donde está 'datos_consolidados.csv'.")

df = pd.read_csv(CSV)

# Basic validation of expected columns
for col, _ in metrics:
    if col not in df.columns:
        raise KeyError(f"Columna esperada '{col}' no encontrada en {CSV}. Columnas disponibles: {list(df.columns)}")

# Create 2x2 plot
sns.set(style='whitegrid', font_scale=1.0)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.ravel()

# Colors
palette = {'Manual': '#1f77b4', 'IA': '#ff7f0e', 'AI': '#ff7f0e'}

results = []

for ax, (col, title) in zip(axes, metrics):
    # Prepare data
    # Assume group column is named 'tool' or 'grupo' or 'tipo'; try common variants
    if 'tool' in df.columns:
        group_col = 'tool'
    elif 'grupo' in df.columns:
        group_col = 'grupo'
    elif 'group' in df.columns:
        group_col = 'group'
    elif 'source' in df.columns:
        group_col = 'source'
    else:
        # fallback: look for 'Manual'/'IA'/'AI' in a column
        possible = [c for c in df.columns if df[c].astype(str).isin(['Manual','IA','AI','IA']).any()]
        if possible:
            group_col = possible[0]
        else:
            raise KeyError("No se encontró columna de grupo (busqué 'tool','grupo','group','source').")

    # Normalize group labels: map spanish IA or AI to 'IA'/'Manual' as in dataset
    # We'll treat 'IA' and 'AI' as same if present
    df[group_col] = df[group_col].astype(str)

    g_manual = df[df[group_col].str.contains('Manual', case=False, na=False)][col].dropna()
    g_ai = df[df[group_col].str.contains('IA|AI|I.A.|IA_', case=False, na=False)][col].dropna()

    # If empty, try exact matches 'Manual' and 'IA'
    if g_manual.empty or g_ai.empty:
        # Try values 'Manual' and 'IA'
        g_manual = df[df[group_col] == 'Manual'][col].dropna()
        g_ai = df[df[group_col].isin(['IA','AI'])][col].dropna()

    # Combine for seaborn
    plot_df = pd.concat([
        pd.DataFrame({col: g_manual, 'Grupo': 'Manual'}),
        pd.DataFrame({col: g_ai, 'Grupo': 'IA'})
    ], ignore_index=True)

    # Compute Mann-Whitney U
    try:
        u_stat, p_val = mannwhitneyu(g_manual, g_ai, alternative='two-sided')
    except ValueError:
        # If one group is constant or too small
        u_stat, p_val = np.nan, np.nan

    results.append({'metric': col, 'u': float(u_stat) if not np.isnan(u_stat) else None, 'p': float(p_val) if not np.isnan(p_val) else None,
                    'median_manual': float(np.median(g_manual)) if len(g_manual)>0 else None,
                    'median_ai': float(np.median(g_ai)) if len(g_ai)>0 else None,
                    'n_manual': int(len(g_manual)), 'n_ai': int(len(g_ai))})

    # Plot: boxplot + a lightweight jittered stripplot (subsampled to avoid overplotting)
    sns.boxplot(x='Grupo', y=col, data=plot_df, ax=ax, palette=palette, showfliers=False)
    # For performance, overlay a subsampled stripplot (max 300 points per group)
    max_overlay = 300
    overlay_df = []
    for g in ['Manual', 'IA']:
        grp = plot_df[plot_df['Grupo'] == g]
        if len(grp) > max_overlay:
            grp = grp.sample(max_overlay, random_state=42)
        overlay_df.append(grp)
    overlay_df = pd.concat(overlay_df, ignore_index=True)
    sns.stripplot(x='Grupo', y=col, data=overlay_df, ax=ax, color='0.25', size=3, alpha=0.45, jitter=0.15, dodge=True)

    # Title with medians and p-value
    p_text = 'p = {:.2e}'.format(p_val) if (p_val is not None and not np.isnan(p_val)) else 'p = NA'
    med_text = f"medianas: Manual={results[-1]['median_manual']:.3f}, IA={results[-1]['median_ai']:.3f}" if results[-1]['median_manual'] is not None else ''
    ax.set_title(f"{title}\n{med_text} — {p_text}")
    ax.set_xlabel('')
    ax.set_ylabel(title)

plt.tight_layout()

# Save
png_out = OUT_DIR / 'paso3b_mannwhitney.png'
pdf_out = OUT_DIR / 'paso3b_mannwhitney.pdf'
fig.savefig(png_out, dpi=300)
fig.savefig(pdf_out, dpi=300)

# Also save a small CSV with results
res_df = pd.DataFrame(results)
res_df.to_csv(OUT_DIR / 'paso3b_mannwhitney_results.csv', index=False)

print(f"Gráficos guardados: {png_out} , {pdf_out}")
print(f"Resultados guardados: {OUT_DIR / 'paso3b_mannwhitney_results.csv'}")

# Close
plt.close(fig)
