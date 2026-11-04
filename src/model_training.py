"""
Model Benchmark and Probability Calibration Module.
Evaluates Logistic Regression, Random Forest, XGBoost, and LightGBM using 5-Fold Stratified CV.
Reports PR-AUC, ROC-AUC, F2-Score, Brier Score, and applies probability calibration.
"""
import sys
import os
import numpy as np
import pandas as pd
import logging
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import (
    average_precision_score, roc_auc_score, fbeta_score, 
    brier_score_loss, make_scorer, precision_score, recall_score
)
from sklearn.calibration import CalibratedClassifierCV, calibration_curve

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline_builder import get_preprocessor, get_train_test_splits
from src.config import CONFIG

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def get_candidate_models(pos_weight: float = 2.77):
    """
    Returns the dictionary of candidate models configured for benchmark.
    """
    models = {
        'Logistic Regression (Baseline)': LogisticRegression(
            penalty='l2', C=1.0, class_weight='balanced', 
            max_iter=1000, random_state=CONFIG.RANDOM_STATE
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=300, max_depth=8, min_samples_split=10, 
            class_weight='balanced_subsample', random_state=CONFIG.RANDOM_STATE, n_jobs=-1
        ),
        'XGBoost': XGBClassifier(
            n_estimators=250, max_depth=4, learning_rate=0.05, 
            scale_pos_weight=pos_weight, subsample=0.8, colsample_bytree=0.8,
            eval_metric='logloss', random_state=CONFIG.RANDOM_STATE, n_jobs=-1
        ),
        'LightGBM': LGBMClassifier(
            n_estimators=250, max_depth=5, num_leaves=31, learning_rate=0.05,
            class_weight='balanced', subsample=0.8, colsample_bytree=0.8,
            random_state=CONFIG.RANDOM_STATE, n_jobs=-1, verbose=-1
        )
    }
    return models

def evaluate_models_cross_validation(X_train, y_train):
    """
    Runs 5-Fold Stratified Cross-Validation on all candidate models.
    """
    preprocessor = get_preprocessor()
    pos_weight = (len(y_train) - y_train.sum()) / y_train.sum() # ~2.77
    models = get_candidate_models(pos_weight=pos_weight)
    
    cv = StratifiedKFold(n_splits=CONFIG.CV_FOLDS, shuffle=True, random_state=CONFIG.RANDOM_STATE)
    
    # Custom scorers
    f2_scorer = make_scorer(fbeta_score, beta=2)
    pr_auc_scorer = make_scorer(average_precision_score, response_method='predict_proba')
    roc_auc_scorer = make_scorer(roc_auc_score, response_method='predict_proba')
    brier_scorer = make_scorer(brier_score_loss, response_method='predict_proba', greater_is_better=False)
    
    scoring = {
        'pr_auc': pr_auc_scorer,
        'roc_auc': roc_auc_scorer,
        'f2': f2_scorer,
        'brier': brier_scorer
    }
    
    results = []
    
    logging.info(f"Starting 5-Fold Stratified CV across {len(models)} candidate models...")
    for name, model in models.items():
        logging.info(f"Evaluating {name}...")
        full_pipe = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])
        
        cv_res = cross_validate(full_pipe, X_train, y_train, cv=cv, scoring=scoring, n_jobs=1)
        
        results.append({
            'Model': name,
            'PR-AUC (Mean)': np.mean(cv_res['test_pr_auc']),
            'PR-AUC (Std)': np.std(cv_res['test_pr_auc']),
            'ROC-AUC (Mean)': np.mean(cv_res['test_roc_auc']),
            'ROC-AUC (Std)': np.std(cv_res['test_roc_auc']),
            'F2-Score (Mean)': np.mean(cv_res['test_f2']),
            'F2-Score (Std)': np.std(cv_res['test_f2']),
            'Brier Score (Mean)': -np.mean(cv_res['test_brier']), # convert back to positive loss
            'Brier Score (Std)': np.std(cv_res['test_brier'])
        })
        
    results_df = pd.DataFrame(results).sort_values(by='PR-AUC (Mean)', ascending=False)
    return results_df

def train_and_calibrate_champion(X_train, y_train, X_test, y_test):
    """
    Trains and calibrates the best-performing models on the full training set
    and validates them on the holdout test set.
    """
    preprocessor = get_preprocessor()
    pos_weight = (len(y_train) - y_train.sum()) / y_train.sum()
    
    # We will train and calibrate XGBoost (champion candidate) and Logistic Regression
    xgb_base = XGBClassifier(
        n_estimators=250, max_depth=4, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8, eval_metric='logloss',
        random_state=CONFIG.RANDOM_STATE, n_jobs=-1
    )
    
    xgb_pipe = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', xgb_base)
    ])
    
    # 5-fold internal calibration using isotonic/sigmoid
    calibrated_xgb = CalibratedClassifierCV(estimator=xgb_pipe, method='sigmoid', cv=5)
    
    logging.info("Fitting Calibrated XGBoost model on Train Set...")
    calibrated_xgb.fit(X_train, y_train)
    
    # Test set evaluation
    y_proba_raw = xgb_pipe.fit(X_train, y_train).predict_proba(X_test)[:, 1]
    y_proba_cal = calibrated_xgb.predict_proba(X_test)[:, 1]
    
    raw_brier = brier_score_loss(y_test, y_proba_raw)
    cal_brier = brier_score_loss(y_test, y_proba_cal)
    cal_prauc = average_precision_score(y_test, y_proba_cal)
    cal_rocauc = roc_auc_score(y_test, y_proba_cal)
    
    logging.info(f"Holdout Test Results for Calibrated XGBoost:")
    logging.info(f"  - PR-AUC: {cal_prauc:.4f}")
    logging.info(f"  - ROC-AUC: {cal_rocauc:.4f}")
    logging.info(f"  - Raw Brier Score: {raw_brier:.4f} --> Calibrated Brier Score: {cal_brier:.4f} (Lower is better)")
    
    return calibrated_xgb, xgb_pipe, y_proba_cal, y_proba_raw

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = get_train_test_splits()
    
    # 1. Cross Validation Benchmark
    benchmark_df = evaluate_models_cross_validation(X_train, y_train)
    print("\n" + "="*80)
    print("5-FOLD STRATIFIED CROSS-VALIDATION BENCHMARK RESULTS")
    print("="*80)
    print(benchmark_df.to_string(index=False))
    
    # Save benchmark table
    output_table_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "model_benchmark_results.csv")
    benchmark_df.to_csv(output_table_path, index=False)
    print(f"\nSaved benchmark table to {output_table_path}")
    
    # 2. Calibration
    cal_model, raw_model, y_proba_cal, y_proba_raw = train_and_calibrate_champion(X_train, y_train, X_test, y_test)
