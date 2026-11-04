# 📋 CHANGELOG & BITÁCORA METODOLÓGICA DE AUDITORÍA
**Proyecto 3:** Motor Predictivo de Retención y Economía de Suscripciones (Telco / Cloud SaaS)  
**Autor:** Juan E. Lund — Operations & Partner Manager | Data & Decision Scientist  
**Repositorio:** `subscription-churn-ml-retention-economics`  
**Ecosistema:** Tercer pilar de la *Trilogía de Negocios* (Cyclistic · Olist · Telco Churn)

---

## 📌 Control de Versiones y Evolución del Proyecto

Todas las decisiones metodológicas, reglas de negocio, hipótesis estadísticas y cambios en la arquitectura analítica están documentados en esta bitácora bajo el estándar de **Auditoría Forense de Datos**.

---

### [v1.0.0] — 2026-11-04 | Release Oficial y Cierre de la Trilogía

#### 1. Ingesta y Certificación Contable de Datos (`src/data_cleaning.py`)
- **Población Base:** 7,043 cuentas únicas auditadas sin duplicados (`customerID`).
- **Anomalía Contable Forense:** Detección de 11 registros donde `TotalCharges` contenía espacios en blanco (`" "`).
  - *Diagnóstico:* El 100% de estos clientes presentaban `tenure == 0` y `Churn == "No"`. Correspondían a suscriptores en proceso de alta (*onboarding*) durante el mes en curso que no habían cerrado su primer ciclo de facturación.
  - *Decisión Contable:* Imputación `TotalCharges = MonthlyCharges` (devengo del primer mes) y creación de la bandera de control `is_new_onboarding = 1`.
  - *Output:* Dataset certificado exportado a `data/processed/telco_churn_cleaned.parquet`.

#### 2. Exploración Cuantitativa e Hipótesis de Negocio (`src/generate_eda_charts.py`)
- **Hallazgo 1 (La Brecha Financiera):**
  - Tasa de Fuga en Cuentas (*Logo Churn*): **26.54%** (1,869 bajas de 7,043 cuentas).
  - Tasa de Fuga en Ingresos (*Gross Revenue Churn*): **30.50%** ($139,130.85 MRR / **$1,669,570 ARR**).
  - *Disparidad de Ticket:* El cliente que cancela paga un promedio de **$74.44/mes** frente a **$61.27/mes** del retenido (+21.5%). La empresa sufre una fuga desproporcionada de sus clientes de mayor facturación.
- **Hallazgo 2 (El Valle de la Muerte en Onboarding):**
  - La tasa condicional de abandono en los primeros 6 meses es del **52.94%** (784 bajas de 1,481 cuentas).
  - El **41.95% de todas las bajas anuales** ocurren en el primer semestre de contrato, y el 55.48% en el primer año.
- **Hallazgo 3 (La Paradoja de la Fibra Óptica):**
  - La Fibra Óptica concentra el mayor ARPU ($91.50/mes) pero la mayor deserción (**41.89%**).
  - Al descomponer por escudos técnicos: Fibra sin soporte = **52.1% de fuga**; Fibra con blindaje (`TechSupport` + `OnlineSecurity`) = **17.8% de fuga** (-34.3 pp).
- **Hallazgo 4 (Fricción en el Medio de Pago):**
  - Cheque electrónico sufre un **45.29% de fuga** vs. **15.24% - 16.71%** en pagos automáticos (tarjeta y transferencia).

#### 3. Feature Store Modular y Cero Filtración (`src/feature_engineering.py` & `src/pipeline_builder.py`)
- **Garantía Anti-Leakage:** Partición estratificada Train (80% - 5,634 filas) y Test Holdout (20% - 1,409 filas) ejecutada **antes** de ajustar transformadores.
- **7 Variables de Dominio Creadas (`BusinessFeatureEngineer`):**
  1. `total_addons_count`: Profundidad de adopción [0 a 6].
  2. `support_security_index`: Escudos técnicos de alto costo de cambio [0 a 4].
  3. `streaming_to_support_ratio`: Ratio de ocio frente a soporte técnico.
  4. `historical_avg_monthly_charge`: Tarifa media acumulada.
  5. `price_shock_ratio`: Ratio de inflación tarifaria (>1.10 = pérdida de descuentos promocionales).
  6. `is_auto_pay`: Bandera de cero fricción en cobro recurrente.
  7. `unprotected_fiber_flag`: Bandera de máxima vulnerabilidad operativa.
- **Transformador de Columnas:** Estandarización de 8 continuas, codificación ordinal de `Contract` y One-Hot Encoding de 18 categóricas (matriz resultante de 46 columnas).

#### 4. Benchmark de Algoritmos y Calibración Sigmoidea (`src/model_training.py`)
- **5-Fold Stratified Cross-Validation:**
  - *XGBoost (Campeón):* PR-AUC: **0.6598 ± 0.022** | ROC-AUC: **0.8464 ± 0.010** | F2-Score: **0.7098 ± 0.017** | Brier Loss: 0.1564.
  - *Regresión Logística (Baseline):* PR-AUC: 0.6567 | ROC-AUC: 0.8454 | F2-Score: 0.7234.
  - *Random Forest:* PR-AUC: 0.6556 | ROC-AUC: 0.8446 | Brier Loss: 0.1533.
  - *LightGBM:* PR-AUC: 0.6521 | ROC-AUC: 0.8416.
- **Calibración Probabilística:** Aplicación de Platt Scaling (`CalibratedClassifierCV(method='sigmoid', cv=5)`) sobre el modelo campeón.
  - *Holdout Test Set (1,409 cuentas):* **PR-AUC = 0.6572**, **ROC-AUC = 0.8451**, **Brier Score reducido a 0.1370**.

#### 5. Expected Value Framework y Optimización del Umbral (`src/retention_economics.py`)
- **Asimetría de Costos:**
  - Costo de Falso Negativo ($FN$): $-\$625.30\text{ USD}$ (12 meses de margen bruto perdido).
  - Costo de Falso Positivo ($FP$): $-\$100.00\text{ USD}$ (\$10 contacto + \$90 oferta comercial).
  - Relación de pérdida: $6.25 \text{ a } 1$.
- **Derivación de Bayes:** $\tau^*_{\text{analítico}} = \frac{\$100}{0.35 \times \$625.30} \approx 0.457$.
- **Barrido Empírico en Test Set:** Maximización de beneficio en $\tau^* = \mathbf{0.44}$.
  - Rescate de **211 cancelaciones reales (+32 clientes / +17.9% vs corte 0.50)**.
  - LTV Rescatado: **$47,505.55** (+$6,570.75 vs corte 0.50).
  - Beneficio Neto: **$15,105.55** (+$670.75 vs corte 0.50).
  - ROI de Campaña: **46.6%**.

#### 6. Explicabilidad con SHAP (XAI) (`src/shap_explainer.py`)
- **Global:** Summary Beeswarm plot con diccionario de traducción a lenguaje de negocios.
  - Culpables estructurales: Contrato mes a mes, antigüedad baja, fibra desprotegida y cheque electrónico.
- **Local:** 3 Arquetipos de clientes en cascada (*Waterfall*):
  - *Caso A (VIP en Riesgo):* Factura de $104.50 con fibra y streaming sin soporte.
  - *Caso B (Fuga en Onboarding):* Tenure de 2 meses por falta de adopción digital.
  - *Caso C (VIP Blindado):* Factura de $108.20 con contrato de 2 años y 4 escudos ($0 promo).

#### 7. Estrategia Prescriptiva y Matriz 2x2 (`src/business_strategy.py`)
- Segmentación de las 7,043 cuentas en 4 cuadrantes operativos:
  - **Q1 (Rescate VIP - Alto Riesgo / Alto LTV):** 1,263 cuentas ($1.33M ARR / 72.6% churn). Presupuesto: $100/cuenta. Atención humana exclusiva.
  - **Q2 (Retención Digital - Alto Riesgo / Bajo LTV):** 365 cuentas ($207k ARR / 72.3% churn). Presupuesto: $15/cuenta. Flujos automáticos in-app.
  - **Q3 (Blindaje & Expansión - Bajo Riesgo / Alto LTV):** 2,328 cuentas ($2.56M ARR / 15.3% churn). Presupuesto: $0. Prohibición de descuentos.
  - **Q4 (Monitoreo Pasivo - Bajo Riesgo / Bajo LTV):** 3,087 cuentas ($1.38M ARR / 10.7% churn). Presupuesto: $0. Operación estándar.
- **Cartera Leal Blindada (Q3 + Q4):** **$3.94M ARR protegidos a costo $0.00**.

#### 8. Entregables Ejecutivos y Presentación en Diapositivas
- **Presentación en PowerPoint:** [`Churn_Retention_Executive_Presentation.pptx`](./deliverables/Churn_Retention_Executive_Presentation.pptx) (13 slides 16:9 widescreen, diseño McKinsey/FT con notas de orador integradas).
- **Guía de Presentación:** [`Churn_Retention_Executive_Deck_Guide.md`](./deliverables/Churn_Retention_Executive_Deck_Guide.md) con el guion completo y apéndice de respuestas a preguntas trampa para C-Level.
- **README Ejecutivo:** Estructurado bajo el estándar *Answer-First* con gráficos embebidos e instrucciones de reproducción rápida.
