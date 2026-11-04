# 📡 Predictive Customer Retention & Subscription Economics
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-EB3C00?logo=xgboost&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-4.3+-0078D7?logo=microsoft&logoColor=white)
![SHAP](https://img.shields.io/badge/SHAP-XAI-brightgreen)
![Status](https://img.shields.io/badge/Status-Completed-success)

> **LTV Optimization, SHAP Explainability & EBITDA Maximization over a $5.47M ARR Portfolio**  
> **Author:** Juan E. Lund — Operations & Partner Manager | Data & Decision Scientist  
> **Language:** **English** | [Versión en Español](README.es.md)

---

## 1. Executive Summary (Answer-First)

To halt recurring revenue erosion and maximize the return on retention capital, the company must **abandon the default Machine Learning threshold ($\tau = 0.50$) and adopt an Expected Value decision framework with a calibrated threshold at $\tau^* = 0.44$, concentrating human commercial outreach on the 17.9% of subscribers driving 79.5% of total revenue loss**.

This project proves that subscription churn is not a homogenous volume problem (*Logo Churn* of 26.54%), but an **asymmetric revenue bleed (*Gross Revenue Churn* of 30.50% / $1,669,570 ARR)** caused by high-ARPU fiber optic accounts lacking technical support shields. The calibrated decision engine rescues **$47,505.55 in gross contribution margin in the test set (projecting $75,528 annualized net gain across the portfolio)** at a **46.6% campaign ROI**, while **prohibiting unnecessary retention discounts on 76.9% of healthy customers, ring-fencing $3.94M ARR at zero cost**.

### Financial and Operational Impact Summary

| Portfolio Metric | Baseline (Status Quo / No ML) | Default ML Cutoff ($\tau = 0.50$) | Calibrated Optimal Cutoff ($\tau^* = 0.44$) | Incremental Net Impact |
| :--- | :---: | :---: | :---: | :---: |
| **Total Audited Portfolio** | 7,043 accounts ($5,473,399 ARR) | 7,043 accounts | 7,043 accounts | — |
| **Gross Annual Revenue Bleed** | 1,869 accounts (**$1,669,570 ARR**) | — | — | **30.50% Gross Revenue Churn** |
| **True Churners Rescued (20% Test)** | 0 accounts (0.0%) | 179 accounts (47.9%) | **211 accounts (56.4%)** | **+32 churners rescued (+17.9%)** |
| **Campaign Spend ($C_{\text{int}} = \$100$)** | $0.00 | $26,500.00 | $32,400.00 | +$5,900.00 |
| **Rescued Gross Margin LTV (12m)** | $0.00 | $40,934.80 | **$47,505.55** | **+$6,570.75 in rescued margin** |
| **Incremental Net Profit (Lift)** | $0.00 | $14,434.80 | **$15,105.55** | **+$670.75 net lift (Test Set)** |
| **Campaign ROI** | 0.0% | 54.5% | **46.6%** | **Sustainable high-yield return** |
| **Subsidies on Loyal Accounts (Q3/Q4)**| High (Blanket promotions) | Moderate | **$0.00 (5,415 ring-fenced accounts)**| **$3.94M ARR protected at zero cost** |

---

## 2. Business Problem & Cost Asymmetry (Ask)

### 2.1 Logo Churn vs. Gross Revenue Churn Gap
* **Logo Churn (Account Volume):** **26.54%** (1,869 accounts out of 7,043).
* **Gross Revenue Churn (Dollar Bleed):** **30.50%** ($139,130.85/month of $456,116.60 total MRR).
* **The Asymmetry Gap (+3.96 pp):** Retained subscribers pay **$61.27/month** on average, while churning subscribers pay **$74.44/month (+21.5% premium)**. The business is disproportionately losing its highest-paying accounts.

![Revenue Churn Gap](./assets/01_logo_vs_revenue_churn_gap.png)

### 2.2 Why Optimizing for Accuracy Destroys Capital
On a 26.54% churn dataset, a naive majority-class classifier predicting *no one ever churns* scores a **73.46% Accuracy**. Yet its business value is zero: it detects zero cancellations and permits the full $1.67M ARR loss.

### 2.3 Mathematical Formulation: Asymmetric Cost-Benefit Matrix
* **Cost of False Negative ($FN$):** Loss of 12 months of salvageable contribution margin:
  $$\overline{V} = \text{MRR} \times m \times H = \$74.44 \times 0.70 \times 12 = \mathbf{\$625.30\text{ USD}}$$
* **Cost of False Positive ($FP$):** Operational contact cost + promotional discount granted unnecessarily:
  $$C_{\text{int}} = C_{\text{contact}} + C_{\text{offer}} = \$10 + \$90 = \mathbf{\$100.00\text{ USD}}$$
* **Save Rate ($\gamma$):** $\gamma = 0.35$ (35% campaign acceptance among true churners).
* **Loss Ratio:** Losing a premium customer is **6.25x more expensive** than giving an unneeded discount.
* **Bayesian Theoretical Optimal Threshold:**
  $$\tau^* = \frac{C_{\text{int}}}{\gamma \cdot V} = \frac{100}{0.35 \times 625.30} \approx \mathbf{0.457 \quad (45.7\%)}$$

---

## 3. Data Cleaning & Feature Engineering Pipeline (Prepare & Process)

### 3.1 Accounting Sanity Audit (`src/data_cleaning.py`)
* Audited 7,043 unique accounts in the IBM Watson Telco dataset.
* **Blank TotalCharges Anomaly:** 11 records had whitespace strings (`" "`).
* **Forensic Audit:** 100% of these cases had `tenure == 0` and `Churn == "No"` (first-month onboarding accounts awaiting first billing cycle).
* **Accounting Imputation Rule:** Imputed `TotalCharges = MonthlyCharges` and flagged `is_new_onboarding = 1`.

### 3.2 Feature Store & Pipeline Hygiene (`src/feature_engineering.py`)
To prevent data leakage, stratified splitting (80% Train / 20% Holdout Test) occurred strictly **before** fitting transformers. The custom scikit-learn transformer `BusinessFeatureEngineer` extracts 7 domain features:

| Derived Feature | Operational Definition | Business Rationale & Analytical Role |
| :--- | :--- | :--- |
| `total_addons_count` | Sum of active add-on services `[0 to 6]` | Measures digital ecosystem depth and customer engagement. |
| `support_security_index`| `TechSupport + OnlineSecurity + DeviceProtection + Backup` `[0 to 4]` | Isolates high-switching-cost technical shield services. |
| `streaming_to_support_ratio`| `(StreamingTV + StreamingMovies) / (support_security_index + 1)` | Identifies high-ARPU entertainment accounts lacking technical protection. |
| `historical_avg_monthly_charge`| `TotalCharges / max(tenure, 1)` | Tracks historical base pricing per account. |
| `price_shock_ratio` | `MonthlyCharges / historical_avg_monthly_charge` | Ratio > 1.10 flags promo roll-offs or recent price hikes. |
| `is_auto_pay` | Binary indicator if `PaymentMethod` is automated | Measures frictionless payment execution. |
| `unprotected_fiber_flag` | `Fiber optic` without `TechSupport` or `OnlineSecurity` | Flags the #1 margin risk combination in the catalog. |

---

## 4. Model Benchmark & Probability Calibration (Model & Validate)

Evaluated across **5-Fold Stratified Cross-Validation**:

```
                         Model  PR-AUC (Mean)  PR-AUC (Std)  ROC-AUC (Mean)  ROC-AUC (Std)  F2-Score (Mean)  Brier Score
                       XGBoost       0.659847      0.022174        0.846363       0.009823         0.709781       0.1564
Logistic Regression (Baseline)       0.656685      0.019781        0.845361       0.012503         0.723401       0.1655
                 Random Forest       0.655617      0.024372        0.844606       0.010357         0.701385       0.1533
                      LightGBM       0.652107      0.019425        0.841583       0.010559         0.695714       0.1558
```

### Platt Scaling Calibration (`CalibratedClassifierCV`)
To ensure predicted scores reflect true empirical event frequencies (a prerequisite for expected value optimization), the champion XGBoost model was calibrated via Platt Scaling (`method='sigmoid'`), reducing the **Brier Score to 0.1370 on the Holdout Test Set**, with **PR-AUC = 0.6572** and **ROC-AUC = 0.8451**.

---

## 5. Decision Threshold Optimization & SHAP Explainability (Explain & Optimize)

### 5.1 Empirical Sweep ($\tau^* = 0.44$)
Evaluating net profit curves across thresholds $\tau \in [0.05, 0.95]$ confirms that empirical optimization converges at $\tau^* = 0.44$, aligning with Bayesian theory:

![Threshold Optimization Dual Panel](./assets/03_expected_value_threshold_optimization.png)

### 5.2 Global Explainability via SHAP Beeswarm
SHAP game-theoretic attribution isolates the 4 primary macro drivers of churn across the company:
1. **Contract Structure:** Month-to-month contracts are the #1 individual risk driver (SHAP values $> +1.5$).
2. **Early Tenures:** 41.95% of all cancellations occur within the first 6 months (*Onboarding Valley of Death*).
3. **Unprotected Fiber Optic:** Fiber optic without technical support drives extreme dissatisfaction among high-spend users.
4. **Payment Method Friction:** Electronic checks triple cancellation propensity (45.3% vs. 15.2% for auto-pay).

![SHAP Global Beeswarm](./assets/04_shap_global_beeswarm.png)

### 5.3 Local CRM Explainability (3 Archetypes)

| Business Case | Local SHAP Diagnosis | Prescriptive Action |
| :--- | :--- | :--- |
| **Case A: At-Risk VIP**<br>($\hat{p}_i = 78.4\%$, MRR: $104.50) | High-ticket fiber optic and streaming, month-to-month, manual electronic check. | **Outbound CS Call:** Annual contract migration + waived TechSupport + $20/month discount for 6 months. |
| **Case B: Onboarding Drop-off**<br>($\hat{p}_i = 74.2\%$, Tenure: 2m) | Premature departure driven by lack of digital self-service adoption. | **Zero-Touch Digital Flow:** In-app setup guidance and guided configuration within first 30 days. |
| **Case C: Protected VIP**<br>($\hat{p}_i = 4.8\%$, MRR: $108.20) | 2-year contract, auto-pay, and 4 active technical protection services. | **No Discount Permitted:** Healthy loyal customer; standard organic engagement only. |

![Case A VIP Churner](./assets/05_shap_waterfall_case_a_vip_churner.png)

---

## 6. Prescriptive Retention Strategy: 2x2 Capital Allocation Matrix (Act)

All 7,043 accounts were segmented across a 2x2 matrix balancing **Calibrated Risk ($\tau^* = 0.44$)** and **Account Value ($\text{MRR} \ge \$70.00$)**:

![Strategic Retention Matrix](./assets/06_strategic_retention_matrix_2x2.png)

* **Q1 — Surgical VIP Rescue ($1,263$ accounts / $1.33M ARR / 72.6% Churn):** Dedicated human Customer Success outbound calls. Budget: $100/account ($126.3K). Migrates accounts to annual contracts with bundled technical support.
* **Q2 — Automated Digital Retention ($365$ accounts / $207K ARR / 72.3% Churn):** Zero-touch in-app automated sequences. Budget: $15/account ($5.5K). Incentivizes auto-pay enrollment.
* **Q3 & Q4 — Ring-Fenced Retention ($5,415$ accounts / $3.94M ARR / 10.7%–15.3% Churn):** **Cost: $0.00**. Explicitly prohibits retention discounts, protecting margin from commercial cannibalization.

### A/B Experimental Deployment Protocol
To certify incremental uplift before full rollout:
1. **Universal Holdout Group:** Randomly isolate 15% of Q1 and Q2 accounts with zero intervention.
2. **Treatment Group (85%):** Receive targeted prescriptive interventions.
3. **Certification Metric:** Measure 90-day and 180-day survival differential ($\text{Uplift} = \text{Retention}_{\text{Treatment}} - \text{Retention}_{\text{Control}}$).

---

## 7. Repository Structure

```text
subscription-churn-ml-retention-economics/
├── deliverables/
│   ├── Churn_Retention_Executive_Presentation.pptx    # 13-slide executive presentation (McKinsey/FT)
│   ├── Churn_Retention_Executive_Deck_Guide.md        # 13-slide speaker guide and objection handling
│   ├── CHANGELOG_Auditoria_Metodologica.md            # Comprehensive audit changelog
│   └── Fase_1_y_2_Resumen_Ejecutivo.md                # Phase 1 & 2 forensic audit log
├── data/
│   ├── processed/
│   │   ├── customer_risk_scoring_matrix.csv           # Final 7,043-account scoring matrix
│   │   ├── model_benchmark_results.csv                # 5-fold CV evaluation results
│   │   ├── telco_churn_cleaned.parquet                # Certified clean dataset
│   │   └── threshold_economics_simulation.csv         # Empirical threshold sweep table
│   └── raw/
│       └── WA_Fn-UseC_-Telco-Customer-Churn.csv       # Immutable IBM source dataset
├── src/
│   ├── business_strategy.py                           # 2x2 quadrant segmentation script
│   ├── config.py                                      # Global financial parameters
│   ├── data_cleaning.py                               # Accounting audit & certification
│   ├── data_ingestion.py                              # Reproducible raw download
│   ├── feature_engineering.py                         # Custom scikit-learn transformer
│   ├── generate_deck.py                               # 16:9 PowerPoint deck generator
│   ├── generate_eda_charts.py                         # Publication asset generator
│   ├── model_training.py                              # 5-fold CV & Platt scaling
│   ├── pipeline_builder.py                            # Leak-free ColumnTransformer pipeline
│   ├── retention_economics.py                         # Expected value optimization & dual panel
│   └── shap_explainer.py                              # Game-theoretic XAI generator
├── assets/                                            # High-resolution visual assets
├── README.es.md                                       # Spanish documentation
├── requirements.txt
└── README.md                                          # Primary English documentation
```

---

### Quick Reproduction Instructions

```bash
git clone https://github.com/JuanLund/subscription-churn-ml-retention-economics.git
cd subscription-churn-ml-retention-economics
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python src/data_ingestion.py
python src/data_cleaning.py
python src/model_training.py
python src/retention_economics.py
python src/shap_explainer.py
python src/business_strategy.py
```
