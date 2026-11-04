"""
SHAP Explainability Module (Global and Local XAI).
Generates publication-quality SHAP Beeswarm summary plots and Waterfall local case studies.
Saves visual assets in assets/ directory.
"""
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap
from lightgbm import LGBMClassifier

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline_builder import get_preprocessor, get_train_test_splits
from src.config import CONFIG

def run_shap_analysis():
    X_train, X_test, y_train, y_test = get_train_test_splits()
    
    preprocessor = get_preprocessor()
    
    # 1. Transform training and test data through pipeline
    print("Pre-transforming feature matrix for SHAP...")
    X_train_trans = preprocessor.fit_transform(X_train)
    X_test_trans = preprocessor.transform(X_test)
    
    # Get human-readable feature names from ColumnTransformer
    col_transformer = preprocessor.named_steps['col_transform']
    num_cols = [
        'tenure', 'MonthlyCharges', 'TotalCharges', 
        'total_addons_count', 'support_security_index',
        'streaming_to_support_ratio', 'historical_avg_monthly_charge', 
        'price_shock_ratio'
    ]
    ord_cols = ['Contract']
    cat_encoder = col_transformer.named_transformers_['cat'].named_steps['onehot']
    cat_cols_raw = [
        'gender', 'SeniorCitizen', 'Partner', 'Dependents',
        'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies',
        'PaperlessBilling', 'PaymentMethod',
        'is_new_onboarding', 'is_auto_pay', 'unprotected_fiber_flag'
    ]
    cat_cols_encoded = cat_encoder.get_feature_names_out(cat_cols_raw)
    feature_names = list(num_cols) + list(ord_cols) + list(cat_cols_encoded)
    
    # Dictionary mapping raw/encoded column names to clean executive business labels
    BUSINESS_FEATURE_LABELS = {
        'tenure': 'Antigüedad del Cliente (Meses)',
        'MonthlyCharges': 'Facturación Mensual (MRR $)',
        'TotalCharges': 'Facturación Histórica Acumulada ($)',
        'total_addons_count': 'Total de Servicios Digitales Activos',
        'support_security_index': 'Índice de Escudos Técnicos (Soporte + Seguridad)',
        'streaming_to_support_ratio': 'Ratio Ocio / Soporte Técnico',
        'historical_avg_monthly_charge': 'Tarifa Promedio Histórica ($)',
        'price_shock_ratio': 'Ratio de Inflación de Tarifa (Price Shock)',
        'Contract': 'Tipo de Contrato (Mes a mes -> 2 años)',
        'Contract_Month-to-month': 'Contrato: Mes a Mes',
        'Contract_One year': 'Contrato: Anual (1 Año)',
        'Contract_Two year': 'Contrato: Bianual (2 Años)',
        'PaymentMethod_Electronic check': 'Medio de Pago: Cheque Electrónico',
        'PaymentMethod_Mailed check': 'Medio de Pago: Cheque Postal',
        'PaymentMethod_Bank transfer (automatic)': 'Medio de Pago: Débito Automático',
        'PaymentMethod_Credit card (automatic)': 'Medio de Pago: Tarjeta Automática',
        'InternetService_Fiber optic': 'Conectividad: Fibra Óptica',
        'InternetService_DSL': 'Conectividad: DSL',
        'InternetService_No': 'Sin Servicio de Internet',
        'TechSupport_Yes': 'Tiene Soporte Técnico',
        'TechSupport_No': 'Sin Soporte Técnico',
        'OnlineSecurity_Yes': 'Tiene Seguridad Online',
        'OnlineSecurity_No': 'Sin Seguridad Online',
        'unprotected_fiber_flag': 'Vulnerabilidad: Fibra sin Soporte Técnico',
        'is_auto_pay': 'Adherido a Pago Automático',
        'is_new_onboarding': 'Suscriptor en Onboarding (<1 mes)',
        'PaperlessBilling_Yes': 'Facturación Electrónica',
        'SeniorCitizen_1': 'Cliente Adulto Mayor (Senior)',
        'Partner_Yes': 'Tiene Pareja',
        'Dependents_Yes': 'Tiene Personas a Cargo (Hijos)'
    }
    
    clean_feature_names = [BUSINESS_FEATURE_LABELS.get(col, col) for col in feature_names]
    
    # 2. Fit LightGBM directly on transformed data (standard Gradient Boosting)
    print("Fitting LightGBM model on preprocessed matrix for TreeExplainer...")
    lgb_model = LGBMClassifier(
        n_estimators=250, max_depth=5, num_leaves=31, learning_rate=0.05,
        class_weight='balanced', subsample=0.8, colsample_bytree=0.8,
        random_state=CONFIG.RANDOM_STATE, n_jobs=-1, verbose=-1
    )
    lgb_model.fit(X_train_trans, y_train)
    
    # Convert transformed test matrix to DataFrame with clean executive column names
    X_test_df = pd.DataFrame(X_test_trans, columns=clean_feature_names, index=X_test.index)
    
    # 3. Compute SHAP values using TreeExplainer
    print("Computing SHAP values on Holdout Test Set (1,409 accounts)...")
    explainer = shap.TreeExplainer(lgb_model)
    shap_values = explainer(X_test_df)
    
    # For binary classification, slice the positive class (churn=1) if dimension is 3D
    if len(shap_values.shape) == 3:
        shap_values_pos = shap_values[:, :, 1]
    else:
        shap_values_pos = shap_values
    
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # ==============================================================================
    # 4. GLOBAL SHAP BEESWARM PLOT
    # ==============================================================================
    print("Generating Global SHAP Beeswarm Plot...")
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    shap.plots.beeswarm(shap_values_pos, max_display=15, show=False)
    plt.title("SHAP Global Feature Attribution (Gradient Boosting)\nImpacto Direccional de cada Factor sobre la Decisión de Fuga", 
              fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    beeswarm_path = os.path.join(assets_dir, "04_shap_global_beeswarm.png")
    plt.savefig(beeswarm_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Global Beeswarm saved to {beeswarm_path}")
    
    # ==============================================================================
    # 5. LOCAL EXPLAINABILITY (3 REAL CUSTOMER ARCHETYPES)
    # ==============================================================================
    print("Identifying and generating 3 Local Customer Archetypes...")
    
    y_test_proba = lgb_model.predict_proba(X_test_trans)[:, 1]
    X_test_copy = X_test.copy()
    X_test_copy['proba'] = y_test_proba
    X_test_copy['actual_churn'] = y_test.values
    
    # Archetype A: The High-Value Silent Churner (High monthly charge, month-to-month, fiber)
    cand_a = X_test_copy[
        (X_test_copy['proba'] >= 0.70) & 
        (X_test_copy['MonthlyCharges'] >= 90) & 
        (X_test_copy['Contract'] == 'Month-to-month')
    ].index
    idx_a = cand_a[0] if len(cand_a) > 0 else X_test_copy['proba'].idxmax()
    pos_a = X_test.index.get_loc(idx_a)
    
    # Archetype B: The Early Onboarding Drop-off (tenure <= 3, month-to-month)
    cand_b = X_test_copy[
        (X_test_copy['proba'] >= 0.70) & 
        (X_test_copy['tenure'] <= 3) & 
        (X_test_copy['MonthlyCharges'] < 80)
    ].index
    idx_b = cand_b[0] if len(cand_b) > 0 else X_test_copy[X_test_copy['tenure'] <= 2].index[0]
    pos_b = X_test.index.get_loc(idx_b)
    
    # Archetype C: The High-Spend Loyal Account (MonthlyCharges > 85, Two year contract, proba < 0.10)
    cand_c = X_test_copy[
        (X_test_copy['proba'] < 0.10) & 
        (X_test_copy['MonthlyCharges'] >= 85) & 
        (X_test_copy['Contract'] == 'Two year')
    ].index
    idx_c = cand_c[0] if len(cand_c) > 0 else X_test_copy['proba'].idxmin()
    pos_c = X_test.index.get_loc(idx_c)
    
    archetypes = [
        (pos_a, idx_a, "Caso A: High-Value Silent Churner (MRR Alto en Riesgo)", "05_shap_waterfall_case_a_vip_churner.png"),
        (pos_b, idx_b, "Caso B: Early Onboarding Drop-off (Fuga Temprana <3m)", "05_shap_waterfall_case_b_onboarding.png"),
        (pos_c, idx_c, "Caso C: Loyal High-Spend Account (Cuenta Blindada de Alto LTV)", "05_shap_waterfall_case_c_loyal_vip.png")
    ]
    
    for pos, customer_id, label, filename in archetypes:
        fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
        shap.plots.waterfall(shap_values_pos[pos], max_display=10, show=False)
        plt.title(f"{label}\nCliente ID: {customer_id} | Probabilidad de Fuga: {y_test_proba[pos]:.1%}", 
                  fontsize=11, fontweight='bold', pad=15)
        plt.tight_layout()
        out_path = os.path.join(assets_dir, filename)
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Waterfall saved to {out_path}")
        
    print("\nSHAP Analysis completed successfully!")

if __name__ == "__main__":
    run_shap_analysis()
