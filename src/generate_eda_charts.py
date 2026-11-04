"""
Visual Assets Generator for Exploratory Data Analysis & Financial Drivers.
Generates publication-quality charts for README and Executive Deliverables.
"""
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set aesthetic theme
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "telco_churn_cleaned.parquet")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

df = pd.read_parquet(DATA_PATH)

# ==============================================================================
# CHART 1: The Revenue Churn Gap ($1.67M ARR Loss)
# ==============================================================================
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)

metrics = ['Logo Churn\n(Volumen de Clientes)', 'Gross Revenue Churn\n(Pérdida en MRR/ARR)']
rates = [26.54, 30.50]
colors = ['#4A90E2', '#D9381E']

bars = ax.bar(metrics, rates, color=colors, width=0.45, edgecolor='black', linewidth=0.5)

ax.set_ylim(0, 38)
ax.set_ylabel('Tasa de Fuga (%)', fontsize=11, fontweight='bold', color='#333333')
ax.set_title('La Brecha de Pérdida Financiera: Logo Churn vs. Revenue Churn\nCartera Total: $5.47M ARR | Pérdida Anual por Fuga: $1.67M ARR', 
             fontsize=12, fontweight='bold', pad=15, color='#1A1A1A')

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.8,
            f'{height:.2f}%',
            ha='center', va='bottom', fontsize=12, fontweight='bold', color='#1A1A1A')

ax.annotate('+3.96 pp de Sangría Financiera\nLos clientes que se van pagan +21.5% más\n($74.44/mes vs $61.27/mes)',
            xy=(1, 30.5), xytext=(0.5, 33),
            arrowprops=dict(arrowstyle="->", color='#D9381E', lw=1.5),
            ha='center', fontsize=10, fontweight='bold', color='#D9381E',
            bbox=dict(boxstyle="round,pad=0.4", fc="#FFF0ED", ec="#D9381E", lw=1))

plt.tight_layout()
chart1_path = os.path.join(ASSETS_DIR, "01_logo_vs_revenue_churn_gap.png")
fig.savefig(chart1_path, dpi=300)
plt.close(fig)
print(f"Chart 1 saved to {chart1_path}")

# ==============================================================================
# CHART 2: Tenure Hazard Curve (Valle de la Muerte en Onboarding)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

df['tenure_cohort'] = pd.cut(df['tenure'], bins=[-1, 6, 12, 24, 48, 72], 
                             labels=['0-6 meses', '7-12 meses', '13-24 meses', '25-48 meses', '49-72 meses'])
cohort_stats = df.groupby('tenure_cohort', observed=False).agg(
    churn_rate=('Churn_Binary', lambda x: x.mean() * 100),
    total_churn=('Churn_Binary', 'sum')
).reset_index()

x = range(len(cohort_stats))
ax.plot(x, cohort_stats['churn_rate'], marker='o', markersize=9, color='#D9381E', linewidth=2.5, label='Tasa de Fuga (%)')

for i, row in cohort_stats.iterrows():
    ax.annotate(f"{row['churn_rate']:.1f}%\n({int(row['total_churn'])} bajas)",
                (i, row['churn_rate']),
                textcoords="offset points", xytext=(0, 10), ha='center',
                fontsize=9.5, fontweight='bold', color='#1A1A1A')

ax.set_xticks(x)
ax.set_xticklabels(cohort_stats['tenure_cohort'], fontsize=10, fontweight='bold')
ax.set_ylabel('Tasa de Fuga Condicional (%)', fontsize=11, fontweight='bold', color='#333333')
ax.set_ylim(0, 65)
ax.set_title('Curva de Fuga por Ciclo de Vida: El "Valle de la Muerte" del Onboarding\nEl 55.5% de todas las bajas ocurren en los primeros 12 meses', 
             fontsize=12, fontweight='bold', pad=15, color='#1A1A1A')

ax.axvspan(-0.5, 0.5, color='#D9381E', alpha=0.10, label='Zona Crítica (0-6 meses): 52.9% de deserción')
ax.legend(loc='upper right', frameon=True)

plt.tight_layout()
chart2_path = os.path.join(ASSETS_DIR, "02_tenure_hazard_curve.png")
fig.savefig(chart2_path, dpi=300)
plt.close(fig)
print(f"Chart 2 saved to {chart2_path}")

# ==============================================================================
# CHART 3: The Fiber Optic & TechSupport Paradox
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

fiber_df = df[df['InternetService'] == 'Fiber optic'].copy()
fiber_df['Support_Bundle'] = np.where(
    (fiber_df['TechSupport'] == 'Yes') & (fiber_df['OnlineSecurity'] == 'Yes'),
    'Blindaje Completo\n(TechSupport + Security)',
    np.where(
        (fiber_df['TechSupport'] == 'Yes') | (fiber_df['OnlineSecurity'] == 'Yes'),
        'Blindaje Parcial\n(Uno de los dos)',
        'Sin Protección Técnica\n(Ninguno de los dos)'
    )
)

bundle_stats = fiber_df.groupby('Support_Bundle').agg(
    churn_rate=('Churn_Binary', lambda x: x.mean() * 100),
    accounts=('customerID', 'count')
).reindex([
    'Blindaje Completo\n(TechSupport + Security)',
    'Blindaje Parcial\n(Uno de los dos)',
    'Sin Protección Técnica\n(Ninguno de los dos)'
])

colors_bundle = ['#2E7D32', '#F9A825', '#C62828']
bars = ax.bar(bundle_stats.index, bundle_stats['churn_rate'], color=colors_bundle, width=0.45, edgecolor='black', linewidth=0.5)

ax.set_ylabel('Tasa de Fuga (%)', fontsize=11, fontweight='bold', color='#333333')
ax.set_ylim(0, 65)
ax.set_title('La Paradoja de la Fibra Óptica: El Impacto de los Escudos Técnicos\n(Base: 3,096 clientes de Fibra Óptica | ARPU promedio: $91.50/mes)', 
             fontsize=12, fontweight='bold', pad=15, color='#1A1A1A')

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1.0,
            f'{height:.1f}%',
            ha='center', va='bottom', fontsize=11, fontweight='bold', color='#1A1A1A')

ax.annotate('Fuga Masiva (+34.3 pp):\nFibra vendida sin soporte técnico\nes la combinación más tóxica del P&L',
            xy=(2, bundle_stats.loc['Sin Protección Técnica\n(Ninguno de los dos)', 'churn_rate']),
            xytext=(1.5, 54),
            arrowprops=dict(arrowstyle="->", color='#C62828', lw=1.5),
            ha='center', fontsize=9.5, fontweight='bold', color='#C62828',
            bbox=dict(boxstyle="round,pad=0.4", fc="#FFEBEE", ec="#C62828", lw=1))

plt.tight_layout()
chart3_path = os.path.join(ASSETS_DIR, "03_fiber_optic_support_paradox.png")
fig.savefig(chart3_path, dpi=300)
plt.close(fig)
print(f"Chart 3 saved to {chart3_path}")
