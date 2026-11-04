# Fase 1 & 2: Auditoría Contable, EDA de Negocio y Feature Store

## 1. Resumen de Ejecución y Certificación de Datos
- **Población Total:** 7,043 cuentas únicas de suscriptores auditadas.
- **Anomalía Contable Detectada y Resuelta:**
  - Se identificaron exactamente **11 cuentas con `TotalCharges` en blanco (`' '`)**.
  - Auditoría forense: El 100% correspondía a cuentas con `tenure == 0` (primer mes de ciclo) y `Churn == 'No'`.
  - Solución contable: Se imputó `TotalCharges = MonthlyCharges` y se generó el indicador `is_new_onboarding = 1`.
  - Dataset certificado exportado a `data/processed/telco_churn_cleaned.parquet`.

## 2. Los 3 Hallazgos Financieros del EDA (Evidencia Cuantitativa)

### Hallazgo 1: La Brecha de Pérdida Financiera (Logo Churn vs. Revenue Churn)
- **Logo Churn (Tasa de Fuga en Cuentas):** **26.54%** (1,869 bajas de 7,043 clientes).
- **Cartera Total:** $456,116.60 MRR / **$5,473,399 ARR**.
- **Sangría Financiera:** $139,130.85 MRR / **$1,669,570 ARR**.
- **Gross Revenue Churn:** **30.50%** (**+3.96 pp por encima de la pérdida de cuentas**).
- **Causa Raíz:** El cliente que cancela paga un promedio de **$74.44/mes**, mientras que el retenido paga **$61.27/mes** (+21.5% de ticket). *Se están fugando preferentemente los clientes de mayor facturación.*

### Hallazgo 2: El "Valle de la Muerte" del Onboarding (Primeros 6 Meses)
- En el tramo de **0 a 6 meses de antigüedad**, la tasa condicional de fuga alcanza el **52.94%** (784 bajas de 1,481 cuentas).
- El **41.95% de todas las bajas de la compañía ocurren en los primeros 6 meses**, y el **55.48% en los primeros 12 meses**.
- **Implicancia Operativa:** La retención es un problema de adopción temprana y *onboarding*, no de desgaste tras años de servicio.

### Hallazgo 3: La Paradoja de la Fibra Óptica y el Blindaje Técnico
- **Clientes de Fibra Óptica:** 3,096 cuentas con el ARPU más alto ($91.50/mes) pero la mayor tasa de cancelación (**41.89%**).
- **El Impacto de TechSupport y OnlineSecurity:**
  - Fibra Óptica SIN soporte ni seguridad técnica: **52.1% de fuga**.
  - Fibra Óptica con blindaje técnico completo: **17.8% de fuga** (**-34.3 pp de reducción**).
- *Conclusión:* Vender fibra de alta velocidad sin soporte técnico es la combinación más destructiva de margen en el P&L.

## 3. Arquitectura del Pipeline y Feature Store (`scikit-learn`)
- **Partición Estratificada:** Train (5,634 filas, 26.54% churn) / Test Holdout (1,409 filas, 26.54% churn) — *Split ejecutado ANTES de cualquier ajuste de parámetros*.
- **Features de Negocio Creadas:**
  1. `total_addons_count` (0 a 6)
  2. `support_security_index` (0 a 4)
  3. `streaming_to_support_ratio`
  4. `historical_avg_monthly_charge`
  5. `price_shock_ratio`
  6. `is_auto_pay`
  7. `unprotected_fiber_flag`
- **Output del Preprocesador:** Matriz de 46 columnas limpias, estandarizadas y codificadas sin *data leakage*.
