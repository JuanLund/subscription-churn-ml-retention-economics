# Guía Maestra para el Deck Ejecutivo: Retención Predictiva y Economía de Suscripciones
**Documento para el Comité Directivo (CEO, CFO, VP of Customer Success)**  
**Autor:** Juan E. Lund — Operations & Partner Manager | Data & Decision Scientist  
**Formato:** Estructura recomendada de 13 Diapositivas con Notas del Orador (*Answer-First Methodology*).

---

## Slide 1: Portada y Declaración de Impacto
* **Título Principal:** *Protección de Ingresos Recurrentes: De la Predicción de Churn a la Maximización de EBITDA*
* **Subtítulo:** *Optimización de Retención sobre una Cartera de $5.47M en ARR mediante Machine Learning y Valor Esperado*
* **Presentador:** Juan E. Lund (Operations & Partner Manager)
* **Nota del Orador:** *"Hoy no venimos a presentar un modelo de inteligencia artificial como un ejercicio académico, sino a presentar una propuesta de asignación de capital: cómo recuperar más de $47k en margen bruto en un grupo de prueba de solo 1,400 clientes y cómo proteger más de $1.3M de ARR que hoy se están fugando silenciosamente."*

---

## Slide 2: Resumen Ejecutivo (Answer-First)
* **Mensaje Clave:** Para frenar la pérdida de ingresos sin regalar margen, la empresa debe sustituir el enfoque reactivo tradicional por una intervención prescriptiva basada en un **umbral calibrado en 44%**.
* **3 Cifras Clave:**
  1. **$1.67M ARR en Riesgo:** La fuga real no es del 26.5% de cuentas, sino del 30.5% de la facturación.
  2. **1,263 Cuentas VIP:** El 79.5% de la sangría se concentra en menos del 18% de los clientes.
  3. **46.6% ROI:** Cada dólar invertido en el rescate de cuentas VIP genera $1.47 en margen de vida útil.

---

## Slide 3: El Diagnóstico Financiero (Logo Churn vs. Revenue Churn)
* **Visual:** Gráfico de barras de la brecha financiera (`01_logo_vs_revenue_churn_gap.png`).
* **Mensaje:** La compañía sufre una fuga desproporcionada de sus clientes más valiosos:
  * El cliente que permanece paga un promedio de **$61.27/mes**.
  * El cliente que cancela paga un promedio de **$74.44/mes (+21.5%)**.
* **Nota del Orador:** *"El equipo de marketing reportaba que perdíamos 1 de cada 4 clientes. La realidad financiera que descubrimos en los datos es que estamos perdiendo casi 1 de cada 3 dólares de facturación recurrente."*

---

## Slide 4: El "Valle de la Muerte" del Onboarding (Primeros 6 Meses)
* **Visual:** Curva de supervivencia y riesgo acumulado (`02_tenure_hazard_curve.png`).
* **Hallazgo:**
  * En los primeros 6 meses de contrato, la tasa condicional de abandono es del **52.9%**.
  * El **41.9% de todas las bajas de la compañía ocurren en este primer semestre**, y el 55.5% en el primer año.
* **Mensaje:** El abandono no es un problema de desgaste tras 3 o 4 años; es una falla de adopción, configuración temprana y bienvenida en el mes 1.

---

## Slide 5: La Paradoja de la Fibra Óptica Desprotegida
* **Visual:** Gráfico comparativo de paquetes de soporte en fibra (`03_fiber_optic_support_paradox.png`).
* **Hallazgo:** La Fibra Óptica tiene el ARPU más alto ($91.50/mes) pero la mayor tasa de cancelación (41.9%).
  * Fibra Óptica SIN soporte técnico: **52.1% de deserción**.
  * Fibra Óptica CON soporte y seguridad: **17.8% de deserción (-34.3 pp)**.
* **Nota del Orador:** *"Vender nuestra conexión más rápida sin soporte técnico es el error más costoso del catálogo. Al primer corte de internet o problema de WiFi, el cliente no tiene a quién recurrir y se va con la competencia."*

---

## Slide 6: Fricción en el Cobro: El Desastre del Cheque Electrónico
* **Hallazgo:** Los clientes que pagan con `Electronic check` sufren una tasa de cancelación del **45.3%**, frente al **15.2% - 16.7%** de los clientes adheridos a débito automático o tarjeta de crédito.
* **Mensaje:** El pago manual obliga al suscriptor a reevaluar su gasto mes a mes. La digitalización del cobro es la palanca de retención más barata de la compañía.

---

## Slide 7: Por Qué las Reglas Tradicionales de IA Destruyen Valor
* **Explicación del Error:** El umbral por defecto de los modelos (50%) asume que perder un cliente cuesta lo mismo que mandarle una oferta.
* **La Asimetría Financiera:**
  * Perder un cliente (Falso Negativo) cuesta **-$625.30** de margen bruto de 1 año.
  * Dar un descuento innecesario (Falso Positivo) cuesta **-$100.00**.
* **Mensaje:** Es 6 veces más caro dejar ir a un cliente que darle una oferta. El modelo tiene que ser más audaz y anticipatorio.

---

## Slide 8: La Solución Matemática: Umbral Óptimo de Decisión ($\tau^* = 0.44$)
* **Visual:** Curva de Beneficio Neto vs. Umbral de Decisión (`03_expected_value_threshold_optimization.png`).
* **Comparativa:**
  * Con corte 0.50: Se rescatan $40.9k con $14.4k de beneficio neto.
  * Con corte óptimo 0.44: Se capturan **+32 fugas adicionales**, alcanzando **$47.5k de LTV rescatado y $15.1k de beneficio neto** (+4.6% neto adicional).

---

## Slide 9: Benchmark de Modelos y Rigor Metodológico
* **Resumen Técnico:** Comparación mediante 5-Fold Stratified Cross-Validation entre Regresión Logística, Random Forest, XGBoost y LightGBM.
* **Modelo Ganador:** **XGBoost Calibrado** (PR-AUC: 0.6598, ROC-AUC: 0.8464, Brier Score: 0.1370).
* **Mensaje:** Garantía de reproducibilidad y cero filtración de datos (*Zero Data Leakage*).

---

## Slide 10: Explicabilidad con SHAP: Abriendo la Caja Negra
* **Visual:** SHAP Beeswarm Plot global (`04_shap_global_beeswarm.png`).
* **Mensaje:** Demostración con Teoría de Juegos Cooperativos de que el modelo no opera por intuición: prioriza contratos mes a mes, antigüedad temprana, tarifas desprotegidas y métodos de pago de alta fricción.

---

## Slide 11: Del Diagnóstico a la Acción: 3 Casos Reales en el CRM
* **Visual:** Casos Waterfall locales (`05_shap_waterfall_case_a_vip_churner.png`).
* **Mensaje:** El agente de Customer Success sabe exactamente por qué llama a cada cliente:
  * Al cliente VIP se le ofrece migración contractual con soporte técnico.
  * Al cliente en onboarding se le asiste en la configuración digital.
  * Al cliente leal se le protege de recibir promociones que canibalicen margen.

---

## Slide 12: La Matriz Prescriptiva de Retención $2 \times 2$
* **Visual:** Gráfico de dispersión de 4 cuadrantes (`06_strategic_retention_matrix_2x2.png`).
* **Estrategia:**
  * **Q1 (Rescate VIP):** 1,263 cuentas ($1.33M ARR) atendidas por agentes humanos ($100/cuenta).
  * **Q2 (Retención Digital):** 365 cuentas ($207k ARR) atendidas por flujos automáticos in-app ($15/cuenta).
  * **Q3 y Q4 (Blindaje y Monitoreo):** 5,415 cuentas leales con **costo $0**.

---

## Slide 13: Plan de Implementación y Protocolo Experimental A/B
* **Hoja de Ruta (Sprints de 8 Semanas):**
  1. **Semana 1-2:** Integración del scoring semanal en el CRM (Salesforce / HubSpot).
  2. **Semana 3-4:** Capacitación del equipo de Customer Success en la oferta del cuadrante Q1.
  3. **Semana 5-8:** Despliegue de la prueba A/B con **15% de Grupo de Control (Holdout)** para certificar el *Incremental Uplift* ante Finanzas.
* **Llamado a la Acción (Ask al Directorio):** Aprobación del presupuesto piloto de retención de **$32,400** con meta de capturar **$47,500 en margen bruto rescatado**.

---

## 💡 Apéndice: Guía de Defensa ante "Preguntas Trampa" en Entrevistas de Alto Nivel

### Trampa 1 (Pregunta del Lead ML Engineer / Head of Data):
> *"¿Por qué usaste XGBoost y CalibratedClassifierCV en lugar de un modelo más complejo o redes neuronales TabNet?"*
* **Tu Respuesta Ganadora:**  
  *"En datos tabulares de comportamiento de clientes, Gradient Boosted Trees sigue siendo el estado del arte empírico en relación costo-rendimiento y velocidad de inferencia. Más importante aún: en finanzas y operaciones no podemos operar con probabilidades descalibradas. Al acoplar el algoritmo con Platt Scaling (CalibratedClassifierCV), redujimos el Brier Score a 0.1370 en el conjunto de prueba intocable. Una red neuronal no calibrada o una caja negra opaca no me permitía justificar ante el CFO la inversión de $100 por cliente intervenido."*

### Trampa 2 (Pregunta del CFO / VP of Finance):
> *"Tu modelo dice que ganaremos $75k netos al año. Pero si le das un descuento de $90 a un cliente que de todos modos se iba a quedar (Falso Positivo), me estás destruyendo EBITDA. ¿Cómo controlas el riesgo de canibalización?"*
* **Tu Respuesta Ganadora:**  
  *"Esa es exactamente la razón por la que rechacé el umbral de IA del 50% y los modelos basados en Accuracy. Mi función de pérdida penaliza cada Falso Positivo con los $100 totales de la intervención ($10 de contacto + $90 de incentivo comercial). Aun absorbiendo ese costo en cada falso positivo, la asimetría económica favorece la intervención porque perder un cliente de alta gama cuesta $625.30 en margen anual. Además, diseñamos un protocolo de despliegue con un 15% de Grupo de Control (Universal Holdout) para medir el Incremental Uplift real antes de escalar la inversión a toda la base."*

### Trampa 3 (Pregunta del VP of Customer Success / Operaciones):
> *"Mi equipo de soporte y retención no tiene capacidad para llamar a miles de clientes cada mes. ¿Cómo se aterriza esto en su día a día?"*
* **Tu Respuesta Ganadora:**  
  *"El modelo fue diseñado con foco en la capacidad operativa instalada. De los 7,043 clientes de la cartera, la matriz prescriptiva aísla exactamente a 1,263 cuentas VIP en riesgo (Cuadrante Q1) a lo largo de un año. Eso representa un promedio de 5 llamadas diarias por agente para un equipo pequeño de 2 personas. Y con la explicabilidad local de SHAP, el agente no llama a tientas: ve en la pantalla si el motivo de riesgo es falta de soporte técnico o fricción en el medio de pago, ofreciendo la solución exacta en el primer contacto."*
