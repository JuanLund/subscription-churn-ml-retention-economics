"""
Business Strategy and Retention Matrix Module.
Segments full portfolio into 4 operational quadrants based on calibrated risk (tau*) and MRR.
Generates customer_risk_scoring_matrix.csv and publication asset 06_strategic_retention_matrix_2x2.png.
"""
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline_builder import get_preprocessor, get_train_test_splits
from src.model_training import train_and_calibrate_champion
from src.config import CONFIG

def assign_quadrants(df_scores, tau_star=0.44, mrr_threshold=70.0):
    """
    Classifies accounts into 4 business quadrants:
    - Q1: High Risk / High Value -> Rescate Quirurgico VIP (Humano Outbound)
    - Q2: High Risk / Low Value  -> Retencion Digital Automatizada (Zero-Touch)
    - Q3: Low Risk / High Value  -> Blindaje & Expansion (Proteccion de Margen)
    - Q4: Low Risk / Low Value   -> Monitoreo Pasivo (Operacion Estandar)
    """
    conditions = [
        (df_scores['risk_score'] >= tau_star) & (df_scores['MonthlyCharges'] >= mrr_threshold),
        (df_scores['risk_score'] >= tau_star) & (df_scores['MonthlyCharges'] < mrr_threshold),
        (df_scores['risk_score'] < tau_star) & (df_scores['MonthlyCharges'] >= mrr_threshold),
        (df_scores['risk_score'] < tau_star) & (df_scores['MonthlyCharges'] < mrr_threshold)
    ]
    
    quadrant_names = [
        'Q1: Rescate Quirurgico VIP',
        'Q2: Retencion Digital Automatizada',
        'Q3: Blindaje & Expansion',
        'Q4: Monitoreo Pasivo'
    ]
    
    actions = [
        'CS Outbound Call + Descuento 20% x 6m + TechSupport Gratis + Auto-Pay',
        'Flujo Automatizado App/Email + Upgrade de Velocidad o Bono $15 Auto-Pay',
        'Prohibido Descuentos + Cross-sell de Servicios Digitales + Fidelizacion Organica',
        'Operacion Estandar + Monitoreo Mensual'
    ]
    
    costs = [100.0, 15.0, 0.0, 0.0]
    
    df_scores['Quadrant'] = np.select(conditions, quadrant_names, default='Q4: Monitoreo Pasivo')
    df_scores['Prescriptive_Action'] = np.select(conditions, actions, default='Operacion Estandar')
    df_scores['Budget_Allocated_USD'] = np.select(conditions, costs, default=0.0)
    
    return df_scores

def plot_retention_matrix(df_scores, tau_star, mrr_threshold, assets_dir):
    """
    Generates a publication-grade scatter/quadrant plot.
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    
    # Color map for quadrants
    colors = {
        'Q1: Rescate Quirurgico VIP': '#C62828',         # Dark red
        'Q2: Retencion Digital Automatizada': '#E65100',  # Orange
        'Q3: Blindaje & Expansion': '#1565C0',            # Blue
        'Q4: Monitoreo Pasivo': '#757575'                 # Gray
    }
    
    for quad, color in colors.items():
        subset = df_scores[df_scores['Quadrant'] == quad]
        ax.scatter(subset['risk_score'], subset['MonthlyCharges'], 
                   c=color, label=f"{quad} (n={len(subset):,})", 
                   alpha=0.45, s=22, edgecolors='none')
        
    # Dividing decision lines
    ax.axvline(tau_star, color='black', linestyle='--', linewidth=1.5, label=f'Umbral Optimo (tau* = {tau_star})')
    ax.axhline(mrr_threshold, color='black', linestyle=':', linewidth=1.5, label=f'Corte de Alto LTV (${mrr_threshold}/mes)')
    
    # Quadrant annotations
    ax.text(0.72, 115, "Q1: RESCATE VIP\nAgente Humano ($100)", fontsize=11, fontweight='bold', 
            ha='center', va='center', bbox=dict(boxstyle="round,pad=0.4", fc="#FFEBEE", ec="#C62828", lw=1.2))
    
    ax.text(0.72, 30, "Q2: RETENCION DIGITAL\nZero-Touch ($15)", fontsize=11, fontweight='bold', 
            ha='center', va='center', bbox=dict(boxstyle="round,pad=0.4", fc="#FFF3E0", ec="#E65100", lw=1.2))
    
    ax.text(0.20, 115, "Q3: BLINDAJE & EXPANSION\nProhibido Descuentos ($0)", fontsize=11, fontweight='bold', 
            ha='center', va='center', bbox=dict(boxstyle="round,pad=0.4", fc="#E3F2FD", ec="#1565C0", lw=1.2))
    
    ax.text(0.20, 30, "Q4: MONITOREO PASIVO\nSin Accion ($0)", fontsize=11, fontweight='bold', 
            ha='center', va='center', bbox=dict(boxstyle="round,pad=0.4", fc="#F5F5F5", ec="#757575", lw=1.2))
    
    ax.set_xlabel('Probabilidad Calibrada de Fuga ($\hat{p}_i$)', fontsize=11, fontweight='bold', color='#333333')
    ax.set_ylabel('Facturacion Mensual Recurrente - MRR ($/mes)', fontsize=11, fontweight='bold', color='#333333')
    ax.set_title('Matriz de Retencion Estrategica 2x2: Asignacion de Recursos segun Riesgo y LTV\n'
                 'Segmentacion Prescriptiva de la Cartera Total (7,043 Clientes | $5.47M ARR)', 
                 fontsize=12, fontweight='bold', pad=15)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(15, 125)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.22), ncol=3, frameon=True, fontsize=9)
    
    plt.tight_layout()
    chart_path = os.path.join(assets_dir, "06_strategic_retention_matrix_2x2.png")
    fig.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Strategic retention matrix chart saved to {chart_path}")

def generate_full_scoring_matrix():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "telco_churn_cleaned.parquet")
    df = pd.read_parquet(data_path)
    
    X_train, X_test, y_train, y_test = get_train_test_splits()
    
    # Train calibrated model
    cal_xgb, raw_xgb, y_proba_cal, y_proba_raw = train_and_calibrate_champion(X_train, y_train, X_test, y_test)
    
    # Generate predictions across ALL 7,043 accounts for operations
    X_all = df.drop(columns=['Churn', 'Churn_Binary'])
    all_proba = cal_xgb.predict_proba(X_all)[:, 1]
    
    df_scores = df[['customerID', 'Contract', 'tenure', 'MonthlyCharges', 'TotalCharges', 'InternetService', 'PaymentMethod', 'Churn']].copy()
    df_scores['risk_score'] = np.round(all_proba, 4)
    df_scores['annual_mrr_usd'] = df_scores['MonthlyCharges'] * 12
    df_scores['ltv_in_risk_usd'] = np.round(df_scores['MonthlyCharges'] * CONFIG.GROSS_MARGIN * CONFIG.LTV_HORIZON_MONTHS, 2)
    
    # Optimal threshold from Phase 4
    TAU_STAR = 0.44
    MRR_CUT = 70.0
    
    df_scores = assign_quadrants(df_scores, tau_star=TAU_STAR, mrr_threshold=MRR_CUT)
    
    # Save processed matrix
    out_csv = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "customer_risk_scoring_matrix.csv")
    df_scores.to_csv(out_csv, index=False)
    print(f"Scoring matrix saved to {out_csv} ({len(df_scores)} rows)")
    
    # Generate visual asset
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    plot_retention_matrix(df_scores, TAU_STAR, MRR_CUT, assets_dir)
    
    # Portfolio breakdown summary
    summary = df_scores.groupby('Quadrant').agg(
        accounts=('customerID', 'count'),
        pct_portfolio=('customerID', lambda x: len(x) / len(df_scores) * 100),
        total_mrr=('MonthlyCharges', 'sum'),
        total_arr=('annual_mrr_usd', 'sum'),
        budget_needed=('Budget_Allocated_USD', 'sum'),
        actual_churn_rate=('Churn', lambda x: (x == 'Yes').mean() * 100)
    ).round(2)
    
    return summary

if __name__ == "__main__":
    summary = generate_full_scoring_matrix()
    print("\n" + "="*80)
    print("PORTFOLIO SEGMENTATION SUMMARY BY RETENTION QUADRANT")
    print("="*80)
    print(summary.to_string())
