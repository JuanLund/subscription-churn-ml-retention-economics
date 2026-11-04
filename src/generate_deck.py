"""
Executive PowerPoint Presentation Generator.
Builds a high-impact 13-slide 16:9 widescreen presentation using McKinsey / Financial Times design principles:
- Deep Navy (#0A2540), Charcoal (#2D3748), Warm Terracotta (#C53030), Emerald (#276749), Light Neutral (#F8FAFC)
- Embeds verified PNG assets from assets/
- Includes comprehensive speaker notes in each slide.
"""
import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PPTX = os.path.join(os.path.dirname(__file__), "..", "deliverables", "Churn_Retention_Executive_Presentation_v2.pptx")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")

# Design System Colors
COLOR_NAVY = RGBColor(10, 37, 64)       # #0A2540 - Primary Brand
COLOR_CHARCOAL = RGBColor(45, 55, 72)   # #2D3748 - Body Text
COLOR_MUTED = RGBColor(113, 128, 150)   # #718096 - Subtitles & borders
COLOR_ACCENT = RGBColor(197, 48, 48)    # #C53030 - Risk / Churn Alert
COLOR_EMERALD = RGBColor(39, 103, 73)   # #276749 - Profit / Retained Margin
COLOR_BG_CARD = RGBColor(248, 250, 252) # #F8FAFC - Card Background
COLOR_WHITE = RGBColor(255, 255, 255)

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions: 13.333 x 7.5 inches
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    def add_header(slide, title_text, category_text="MOTOR DE RETENCIÓN PREDICTIVA & CAPITAL ALLOCATION"):
        # Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT
        
        # Action Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_NAVY
        
    def add_metric_card(slide, left, top, width, height, value_text, label_text, subtext="", border_color=COLOR_MUTED):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_BG_CARD
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)
        
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.15)
        
        p_val = tf.paragraphs[0]
        p_val.text = value_text
        p_val.font.size = Pt(24)
        p_val.font.bold = True
        p_val.font.color.rgb = COLOR_NAVY
        
        p_lbl = tf.add_paragraph()
        p_lbl.text = label_text
        p_lbl.font.size = Pt(11)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = COLOR_CHARCOAL
        p_lbl.space_before = Pt(4)
        
        if subtext:
            p_sub = tf.add_paragraph()
            p_sub.text = subtext
            p_sub.font.size = Pt(9)
            p_sub.font.color.rgb = COLOR_MUTED
            p_sub.space_before = Pt(2)

    # =========================================================================
    # SLIDE 1: Portada Ejecutiva
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.fill.background()
    
    t_box1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.5))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "RETENCIÓN PREDICTIVA & ECONOMÍA DE SUSCRIPCIONES"
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_ACCENT
    
    p2 = tf1.add_paragraph()
    p2.text = "Protección de Ingresos Recurrentes:\nDe la Predicción de Churn a la Maximización de EBITDA"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(14)
    
    p3 = tf1.add_paragraph()
    p3.text = "Optimización sobre una Cartera de $5.47M ARR mediante Expected Value Modeling, Calibración y SHAP"
    p3.font.size = Pt(16)
    p3.font.color.rgb = RGBColor(226, 232, 240)
    p3.space_before = Pt(14)
    
    p4 = tf1.add_paragraph()
    p4.text = "Autor: Juan E. Lund | Operations & Partner Manager & Data Scientist\nEcosistema: Tercer Proyecto de la Trilogía de Negocios (Cyclistic · Olist · Telco)"
    p4.font.size = Pt(12)
    p4.font.color.rgb = RGBColor(148, 163, 184)
    p4.space_before = Pt(36)
    
    s1.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 1 - Portada):\n"
        "Buenas tardes a todos. Hoy no venimos a presentar un modelo de inteligencia artificial como un ejercicio abstracto "
        "o una competencia de Kaggle, sino como una herramienta de toma de decisiones financieras y asignación de capital. "
        "En un negocio de suscripciones, perder clientes no es un problema de algoritmos; es un problema de P&L. "
        "Les mostraré cómo transformamos una cartera de 7,000 cuentas y $5.5M en ingresos anuales en un motor de retención "
        "quirúrgico que maximiza el beneficio neto de la empresa."
    )

    # =========================================================================
    # SLIDE 2: Resumen Ejecutivo (Answer-First)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Resumen Ejecutivo: Rescate de $47.5K en Margen Bruto con ROI del 46.6%")
    
    add_metric_card(s2, Inches(0.8), Inches(1.6), Inches(2.7), Inches(1.8), "$1.67M ARR", "Fuga Bruta en Riesgo", "30.50% Gross Revenue Churn", COLOR_ACCENT)
    add_metric_card(s2, Inches(3.8), Inches(1.6), Inches(2.7), Inches(1.8), "tau* = 0.44", "Umbral Óptimo de Decisión", "Vs 0.50 estándar de IA", COLOR_NAVY)
    add_metric_card(s2, Inches(6.8), Inches(1.6), Inches(2.7), Inches(1.8), "+17.9%", "Aumento en Fugas Capturadas", "+32 clientes reales rescatados", COLOR_EMERALD)
    add_metric_card(s2, Inches(9.8), Inches(1.6), Inches(2.7), Inches(1.8), "$3.94M ARR", "Cartera Leal Blindada", "5,415 cuentas en Q3/Q4 ($0 gasto)", COLOR_MUTED)
    
    tx2 = s2.shapes.add_textbox(Inches(0.8), Inches(3.8), Inches(11.7), Inches(3.0))
    tf2 = tx2.text_frame
    tf2.word_wrap = True
    
    p = tf2.paragraphs[0]
    p.text = "TESIS ESTRATÉGICA DE LA OPERACIÓN:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    points2 = [
        ("1. La Sangría Oculta de Facturación:", " Aunque la tasa de fuga en volumen es del 26.54%, la pérdida de ingresos es del 30.50% ($1.67M ARR). Los clientes que cancelan pagan +21.5% más al mes ($74.44 vs $61.27) que los leales."),
        ("2. Falla del Umbral Estándar (0.50):", " La inteligencia artificial por defecto asume costos simétricos. Como perder un cliente cuesta -$625 de margen y dar un descuento cuesta -$100, el umbral óptimo es 0.44, rescatando +$6,570 de margen en el test set."),
        ("3. Matriz Prescriptiva 2x2:", " El segmento VIP en riesgo (Q1) concentra $1.33M ARR (79.5% de la pérdida total). Se asigna retención humana exclusiva a este segmento y se prohíbe regalar descuentos al 76.9% de clientes leales (Q3/Q4), protegiendo $3.94M de ARR sin regalar margen.")
    ]
    for h, desc in points2:
        p = tf2.add_paragraph()
        p.space_before = Pt(8)
        run_h = p.add_run()
        run_h.text = h
        run_h.font.bold = True
        run_h.font.size = Pt(11.5)
        run_h.font.color.rgb = COLOR_CHARCOAL
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.size = Pt(11.5)
        run_d.font.color.rgb = COLOR_CHARCOAL
        
    s2.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 2 - Resumen Ejecutivo):\n"
        "Comenzamos con la conclusión directa: para frenar la pérdida de ingresos no debemos salir a regalar descuentos masivos "
        "ni confiar en el corte automático de 50% que trae cualquier librería de software. "
        "En una muestra de prueba certificada de 1,409 clientes, nuestro modelo calibrado en 44% capturó 211 cancelaciones reales, "
        "rescatando $47,505 en margen bruto con un ROI positivo de casi 47%. "
        "Y lo más importante para el CFO: blindamos $2.56M en ingresos de clientes leales a costo cero, eliminando el desperdicio comercial."
    )

    # =========================================================================
    # SLIDE 3: La Brecha Financiera (Logo Churn vs. Revenue Churn)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Diagnóstico Financiero: La Ilusión del Logo Churn vs. la Sangría del Revenue Churn")
    
    img_path1 = os.path.join(ASSETS_DIR, "01_logo_vs_revenue_churn_gap.png")
    if os.path.exists(img_path1):
        s3.shapes.add_picture(img_path1, Inches(0.8), Inches(1.6), width=Inches(7.2))
        
    tx3 = s3.shapes.add_textbox(Inches(8.3), Inches(1.6), Inches(4.2), Inches(5.2))
    tf3 = tx3.text_frame
    tf3.word_wrap = True
    
    p = tf3.paragraphs[0]
    p.text = "ANÁLISIS DE UNIT ECONOMICS:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    bullets3 = [
        "Volumen Engañoso: La empresa reportaba un 26.54% de bajas (1,869 clientes de 7,043).",
        "Hemorragia en Dólares: El Gross Revenue Churn alcanza el 30.50% ($139.1K MRR / $1.67M ARR).",
        "Disparidad de Ticket (+21.5%):",
        "  • Cliente Retenido: $61.27 / mes",
        "  • Cliente Fugado: $74.44 / mes",
        "Conclusión Operativa: La empresa no pierde clientes homogéneos; sufre una fuga desproporcionada de sus cuentas de mayor facturación."
    ]
    for b in bullets3:
        p = tf3.add_paragraph()
        p.text = b
        p.font.size = Pt(11)
        p.space_before = Pt(6)
        p.font.color.rgb = COLOR_CHARCOAL
        if "Conclusión" in b:
            p.font.bold = True
            p.font.color.rgb = COLOR_ACCENT
            
    s3.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 3 - Brecha Financiera):\n"
        "Miren el gráfico de la izquierda. Si Marketing nos presenta el informe mensual, nos dirá que perdemos el 26.5% de las cuentas. "
        "Pero cuando un Operations Manager audita el P&L, encontramos que estamos perdiendo el 30.5% de los ingresos. "
        "Son casi 4 puntos porcentuales más de daño económico. ¿Por qué ocurre esto? Porque el cliente que cancela paga en promedio "
        "$74.44 al mes, mientras que el cliente que se queda paga $61.27. Se nos están yendo los clientes premium."
    )

    # =========================================================================
    # SLIDE 4: El Valle de la Muerte en Onboarding
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Ciclo de Vida: El 'Valle de la Muerte' en los Primeros 6 Meses de Servicio")
    
    img_path2 = os.path.join(ASSETS_DIR, "02_tenure_hazard_curve.png")
    if os.path.exists(img_path2):
        s4.shapes.add_picture(img_path2, Inches(0.8), Inches(1.6), width=Inches(7.2))
        
    tx4 = s4.shapes.add_textbox(Inches(8.3), Inches(1.6), Inches(4.2), Inches(5.2))
    tf4 = tx4.text_frame
    tf4.word_wrap = True
    
    p = tf4.paragraphs[0]
    p.text = "HALLAZGO EN RETENCIÓN TEMPRANA:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    bullets4 = [
        "Punto Crítico (0 a 6 meses): En el primer semestre de vida, la tasa condicional de abandono es del 52.94% (784 cancelaciones).",
        "Concentración del Churn: El 41.95% de todas las bajas de la empresa suceden en los primeros 6 meses, y el 55.48% en el primer año.",
        "Estabilización a Largo Plazo: Pasados los 48 meses, la deserción se desploma al 9.5%.",
        "Diagnóstico de Operaciones: La retención no falla por desgaste después de años; falla en la adopción, configuración del servicio y onboarding del mes 1."
    ]
    for b in bullets4:
        p = tf4.add_paragraph()
        p.text = b
        p.font.size = Pt(11)
        p.space_before = Pt(8)
        p.font.color.rgb = COLOR_CHARCOAL
        if "Diagnóstico" in b:
            p.font.bold = True
            p.font.color.rgb = COLOR_ACCENT
            
    s4.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 4 - Valle de la Muerte):\n"
        "Este gráfico rompe con un mito habitual. Mucha gente cree que los clientes se van cuando se aburren tras años de servicio. "
        "Los datos demuestran exactamente lo contrario: más del 41% de todas las cancelaciones ocurren en los primeros 6 meses de contrato. "
        "En este periodo, más de la mitad (52.9%) de los nuevos suscriptores cancela. "
        "Si resolvemos la experiencia de instalación y bienvenida en los primeros 30 a 60 días, resolvemos la mitad del problema del negocio."
    )

    # =========================================================================
    # SLIDE 5: La Paradoja de la Fibra Óptica
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Causa Raíz #1: La Paradoja de la Fibra Óptica y el Blindaje Técnico")
    
    img_path3 = os.path.join(ASSETS_DIR, "03_fiber_optic_support_paradox.png")
    if os.path.exists(img_path3):
        s5.shapes.add_picture(img_path3, Inches(0.8), Inches(1.6), width=Inches(7.2))
        
    tx5 = s5.shapes.add_textbox(Inches(8.3), Inches(1.6), Inches(4.2), Inches(5.2))
    tf5 = tx5.text_frame
    tf5.word_wrap = True
    
    p = tf5.paragraphs[0]
    p.text = "VULNERABILIDAD EN PRODUCTO:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    bullets5 = [
        "Producto Estrella con Mayor Tarifa: La Fibra Óptica concentra 3,096 cuentas con el mayor ARPU ($91.50/mes).",
        "La Mayor Deserción (41.89%): Sufre el doble de fuga que las conexiones DSL tradicionales (18.96%).",
        "El Impacto del Soporte Técnico:",
        "  • Fibra sin Soporte ni Antivirus: 52.1% de deserción masiva.",
        "  • Fibra con Blindaje Completo: 17.8% de deserción (-34.3 pp).",
        "Conclusión Estratégica: Vender fibra de alta velocidad sin soporte técnico es la combinación más destructiva del catálogo. Un cliente con factura de $90+ al primer corte de internet cancela la cuenta."
    ]
    for b in bullets5:
        p = tf5.add_paragraph()
        p.text = b
        p.font.size = Pt(11)
        p.space_before = Pt(6)
        p.font.color.rgb = COLOR_CHARCOAL
        if "Conclusión" in b:
            p.font.bold = True
            p.font.color.rgb = COLOR_ACCENT
            
    s5.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 5 - Paradoja de la Fibra):\n"
        "Aquí está el descubrimiento más impactante del proyecto. Nuestro producto más caro y avanzado es la Fibra Óptica ($91.50/mes). "
        "Sin embargo, 4 de cada 10 clientes de fibra se van. ¿Por qué? Porque el 78% de los que cancelan no tienen contratado ni TechSupport ni OnlineSecurity. "
        "Cuando el cliente cuenta con ese escudo técnico, la deserción se desploma del 52% al 17%. "
        "La solución no es bajar el precio de la fibra; es empaquetar soporte técnico en cada suscripción."
    )

    # =========================================================================
    # SLIDE 6: Fricción en el Cobro (Cheque Electrónico)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Causa Raíz #2: El Dolor de Pago Mensual del Cheque Electrónico")
    
    add_metric_card(s6, Inches(0.8), Inches(1.6), Inches(3.6), Inches(2.2), "45.29%", "Tasa de Fuga con Cheque Electrónico", "2,365 cuentas ($76.26 ARPU)", COLOR_ACCENT)
    add_metric_card(s6, Inches(4.8), Inches(1.6), Inches(3.6), Inches(2.2), "15.24%", "Tasa de Fuga con Tarjeta Automática", "1,522 cuentas ($66.51 ARPU)", COLOR_EMERALD)
    add_metric_card(s6, Inches(8.8), Inches(1.6), Inches(3.6), Inches(2.2), "16.71%", "Tasa de Fuga con Débito Automático", "1,544 cuentas ($67.19 ARPU)", COLOR_EMERALD)
    
    tx6 = s6.shapes.add_textbox(Inches(0.8), Inches(4.2), Inches(11.7), Inches(2.6))
    tf6 = tx6.text_frame
    tf6.word_wrap = True
    
    p = tf6.paragraphs[0]
    p.text = "EL IMPACTO OPERATIVO DEL MÉTODO DE PAGO:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    bullets6 = [
        ("Disparidad 3x en Deserción:", " Los clientes que pagan mediante cheque electrónico cancelan tres veces más que aquellos en medios automáticos (45.3% vs ~16%)."),
        ("El Mecanismo de Fricción:", " El pago manual crea un 'momento de dolor' mensual recurrente donde el usuario cuestiona la tarifa y evalúa competidores. El cobro automático elimina esa fricción cognitiva."),
        ("Palanca de Retención Inmediata:", " Migrar a 1,000 clientes de cheque electrónico a pago automático con un bono de $15 reduce drásticamente el riesgo de deserción con un costo operativo marginal.")
    ]
    for h, desc in bullets6:
        p = tf6.add_paragraph()
        p.space_before = Pt(8)
        run_h = p.add_run()
        run_h.text = h
        run_h.font.bold = True
        run_h.font.size = Pt(11.5)
        run_h.font.color.rgb = COLOR_CHARCOAL
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.size = Pt(11.5)
        run_d.font.color.rgb = COLOR_CHARCOAL
        
    s6.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 6 - Fricción en el Cobro):\n"
        "La segunda causa raíz es el método de pago. El cheque electrónico tiene una tasa de deserción del 45.3%. "
        "En contraste, las tarjetas y transferencias automáticas están en el 15-16%. "
        "Cada vez que un cliente debe entrar a pagar manualmente, experimenta un 'dolor de pago' activo. "
        "Si logramos que el cliente adhiera su factura al débito automático con un incentivo único de $15, reducimos a un tercio su probabilidad de irse."
    )

    # =========================================================================
    # SLIDE 7: Asimetría de Costos y Falla de Métricas Tradicionales
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "La Falla de las Métricas Tradicionales: Por Qué Accuracy y 0.50 Destruyen Valor")
    
    add_metric_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.2), "-$625.30 USD", "Costo de Falso Negativo (FN)", "Cliente que se fuga sin detección = Pérdida de 12 meses de margen bruto ($74.44 x 70% x 12)", COLOR_ACCENT)
    add_metric_card(s7, Inches(6.8), Inches(1.6), Inches(5.6), Inches(2.2), "-$100.00 USD", "Costo de Falso Positivo (FP)", "Descuento innecesario = $10 contacto operativo + $90 incentivo comercial otorgado a cliente leal", COLOR_MUTED)
    
    tx7 = s7.shapes.add_textbox(Inches(0.8), Inches(4.1), Inches(11.7), Inches(2.8))
    tf7 = tx7.text_frame
    tf7.word_wrap = True
    
    p = tf7.paragraphs[0]
    p.text = "POR QUÉ EL CORTE ESTÁNDAR DE MACHINE LEARNING (0.50) ES UN ERROR DE NEGOCIO:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    bullets7 = [
        "Relación de Costos 6.25 a 1: Perder a un cliente de alta gama cuesta 6.25 veces más que entregar una oferta innecesaria a un cliente leal.",
        "El Error de Simetría: Fijar el umbral en 0.50 asume falsamente que el costo de FN y FP es idéntico.",
        "Derivación Analítica de Bayes: tau* = C_int / (gamma * V) = $100 / (0.35 * $625.30) = 0.457.",
        "Objetivo Directivo: El corte óptimo debe ser más agresivo (0.44) para capturar a clientes en riesgo antes de que se produzca la baja."
    ]
    for b in bullets7:
        p = tf7.add_paragraph()
        p.text = b
        p.font.size = Pt(11)
        p.space_before = Pt(6)
        p.font.color.rgb = COLOR_CHARCOAL
        
    s7.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 7 - Asimetría de Costos):\n"
        "Esta diapositiva es clave para cualquier Director de Finanzas. Cuando un modelo de Machine Learning usa el umbral por defecto de 0.50, "
        "asume implícitamente que equivocarse en una falsa alarma cuesta lo mismo que perder a un cliente. "
        "En nuestro negocio, perder un cliente de fibra cuesta -$625 en margen neto de un año. "
        "Darle un descuento por error a alguien leal solo nos cuesta -$100. "
        "Perder la cuenta es 6 veces más caro. Por eso la matemática financiera nos exige mover el corte hacia 0.44."
    )

    # =========================================================================
    # SLIDE 8: Optimización del Umbral de Decisión (tau* = 0.44)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Optimización de Valor Esperado: De la Probabilidad Estadística al EBITDA")
    
    img_path4 = os.path.join(ASSETS_DIR, "03_expected_value_threshold_optimization.png")
    if os.path.exists(img_path4):
        s8.shapes.add_picture(img_path4, Inches(0.8), Inches(1.6), width=Inches(7.2))
        
    tx8 = s8.shapes.add_textbox(Inches(8.3), Inches(1.6), Inches(4.2), Inches(5.2))
    tf8 = tx8.text_frame
    tf8.word_wrap = True
    
    p = tf8.paragraphs[0]
    p.text = "BENCHMARK FINANCIERO (TEST SET):"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    bullets8 = [
        "Métricas en Umbral Default (0.50):",
        "  • Contactos: 265 cuentas",
        "  • Fugas Capturadas: 179 clientes",
        "  • LTV Rescatado: $40,934.80",
        "  • Beneficio Neto: $14,434.80 | ROI: 54.5%",
        "Métricas en Umbral Óptimo (tau* = 0.44):",
        "  • Contactos: 324 cuentas (+59)",
        "  • Fugas Capturadas: 211 clientes (+32 / +17.9%)",
        "  • LTV Rescatado: $47,505.55 (+$6,570.75)",
        "  • BENEFICIO NETO: $15,105.55 (+$670.75 / +4.6%)",
        "Conclusión para el CFO: Usar 0.44 en lugar de 0.50 rescata +$6.5K adicionales de margen y genera mayor beneficio absoluto manteniendo un ROI de 46.6%."
    ]
    for b in bullets8:
        p = tf8.add_paragraph()
        p.text = b
        p.font.size = Pt(10)
        p.space_before = Pt(4)
        p.font.color.rgb = COLOR_CHARCOAL
        if "BENEFICIO NETO" in b or "Conclusión" in b:
            p.font.bold = True
            p.font.color.rgb = COLOR_EMERALD if "BENEFICIO" in b else COLOR_NAVY
            
    s8.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 8 - Optimización de Umbral):\n"
        "Aquí vemos el impacto directo en dólares. Si usáramos el 0.50 tradicional, capturaríamos 179 fugas y dejaríamos escapar a 32 clientes en riesgo. "
        "Al calibrar la política en tau* = 0.44, contactamos a 59 cuentas más, salvamos a esas 32 personas adicionales y aumentamos el LTV rescatado "
        "a $47,505. El beneficio neto salta a $15,105 en solo el 20% de la cartera. "
        "Proyectado al año y a toda la base de suscriptores, esto representa más de $75,000 en EBITDA protegido."
    )

    # =========================================================================
    # SLIDE 9: Benchmark de Modelos y Calibración
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Benchmark de Modelos: Rigor Metodológico y Calibración Sigmoidea")
    
    add_metric_card(s9, Inches(0.8), Inches(1.6), Inches(2.7), Inches(2.0), "0.6598", "PR-AUC (XGBoost)", "Métrica reina en desbalance (Std: ±0.022)", COLOR_NAVY)
    add_metric_card(s9, Inches(3.8), Inches(1.6), Inches(2.7), Inches(2.0), "0.8464", "ROC-AUC (Capacidad Ranking)", "Separación de sanos vs riesgo (Std: ±0.009)", COLOR_NAVY)
    add_metric_card(s9, Inches(6.8), Inches(1.6), Inches(2.7), Inches(2.0), "0.1370", "Brier Score (Calibrado)", "Platt Scaling / Probabilidades empíricas", COLOR_EMERALD)
    add_metric_card(s9, Inches(9.8), Inches(1.6), Inches(2.7), Inches(2.0), "5 Folds", "Stratified Cross-Validation", "Cero filtración de datos (Anti-Leakage)", COLOR_MUTED)
    
    tx9 = s9.shapes.add_textbox(Inches(0.8), Inches(3.9), Inches(11.7), Inches(3.0))
    tf9 = tx9.text_frame
    tf9.word_wrap = True
    
    p = tf9.paragraphs[0]
    p.text = "TABLA COMPARATIVA DE ALGORITMOS (5-FOLD STRATIFIED CV):"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    rows9 = [
        "1. XGBoost Calibrado (Campeón): PR-AUC: 0.6598 | ROC-AUC: 0.8464 | F2-Score: 0.7098 | Brier Loss: 0.1564",
        "2. Regresión Logística (Baseline): PR-AUC: 0.6567 | ROC-AUC: 0.8454 | F2-Score: 0.7234 | Brier Loss: 0.1655",
        "3. Random Forest (Bagging): PR-AUC: 0.6556 | ROC-AUC: 0.8446 | F2-Score: 0.7014 | Brier Loss: 0.1533",
        "4. LightGBM (Boosting): PR-AUC: 0.6521 | ROC-AUC: 0.8416 | F2-Score: 0.6957 | Brier Loss: 0.1558",
        "Certificación en Holdout Test (1,409 cuentas): PR-AUC = 0.6572 | ROC-AUC = 0.8451 | Brier Score = 0.1370."
    ]
    for r in rows9:
        p = tf9.add_paragraph()
        p.text = r
        p.font.size = Pt(10.5)
        p.space_before = Pt(5)
        p.font.color.rgb = COLOR_CHARCOAL
        if "XGBoost" in r or "Certificación" in r:
            p.font.bold = True
            
    s9.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 9 - Benchmark): \n"
        "En esta diapositiva demostramos solvencia técnica. No elegimos un algoritmo al azar. "
        "Sometimos 4 arquitecturas a validación cruzada estratificada de 5 pliegues. "
        "Nuestra Regresión Logística base funcionó muy bien gracias a las variables de negocio que creamos, "
        "pero XGBoost ganó en PR-AUC y ROC-AUC capturando interacciones complejas. "
        "Además, aplicamos calibración sigmoidea para que una probabilidad predicha del 44% signifique exactamente "
        "que 44 de cada 100 clientes se van en la vida real. Sin calibración, los cálculos en dólares no tendrían validez."
    )

    # =========================================================================
    # SLIDE 10: Explicabilidad Global con SHAP
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Explicabilidad Global con SHAP: Abriendo la Caja Negra del Algoritmo")
    
    img_path5 = os.path.join(ASSETS_DIR, "04_shap_global_beeswarm.png")
    if os.path.exists(img_path5):
        s10.shapes.add_picture(img_path5, Inches(0.8), Inches(1.6), width=Inches(7.2))
        
    tx10 = s10.shapes.add_textbox(Inches(8.3), Inches(1.6), Inches(4.2), Inches(5.2))
    tf10 = tx10.text_frame
    tf10.word_wrap = True
    
    p = tf10.paragraphs[0]
    p.text = "TEORÍA DE JUEGOS APLICADA AL CHURN:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    bullets10 = [
        "1. Contrato Mes a Mes: Principal disparador individual hacia la fuga (valores SHAP > +1.5). Los contratos anuales actúan como ancla de lealtad.",
        "2. Antigüedad Baja (Tenure < 12m): Clientes nuevos empujan masivamente hacia el riesgo de cancelación.",
        "3. Fibra sin Soporte Técnico: Dispara el riesgo en usuarios con facturas elevadas.",
        "4. Cheque Electrónico: Aumenta la fricción y el dolor de pago mensual.",
        "Transparencia para el Directorio: El modelo no es una caja negra; cada predicción responde a causas operativas concretas que podemos intervenir."
    ]
    for b in bullets10:
        p = tf10.add_paragraph()
        p.text = b
        p.font.size = Pt(10.5)
        p.space_before = Pt(6)
        p.font.color.rgb = COLOR_CHARCOAL
        if "Transparencia" in b:
            p.font.bold = True
            p.font.color.rgb = COLOR_NAVY
            
    s10.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 10 - SHAP Global):\n"
        "Para que la dirección confíe en el modelo, debemos abrir la 'caja negra'. "
        "Utilizamos SHAP, basado en la Teoría de Juegos de Shapley, para medir la contribución marginal de cada variable. "
        "En el gráfico vemos los 4 culpables principales de la fuga a nivel compañía: contratos mes a mes sin permanencia, "
        "antigüedad temprana menor a un año, fibra óptica sin soporte técnico y pagos mediante cheque electrónico. "
        "Esto nos da la receta exacta de qué políticas comerciales debemos rediseñar."
    )

    # =========================================================================
    # SLIDE 11: Explicabilidad Local para Operaciones (3 Casos Reales)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Explicabilidad Local para Operaciones: Qué Decirle a Cada Cliente en el CRM")
    
    img_path6 = os.path.join(ASSETS_DIR, "05_shap_waterfall_case_a_vip_churner.png")
    if os.path.exists(img_path6):
        s11.shapes.add_picture(img_path6, Inches(0.8), Inches(1.6), width=Inches(6.8))
        
    tx11 = s11.shapes.add_textbox(Inches(7.9), Inches(1.6), Inches(4.6), Inches(5.2))
    tf11 = tx11.text_frame
    tf11.word_wrap = True
    
    p = tf11.paragraphs[0]
    p.text = "ARQUETIPOS DE ACCIÓN EN EL CRM:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    cases11 = [
        ("Caso A: VIP en Riesgo (p = 78.4% | MRR $104.50)", "Cliente con fibra óptica y streaming, mes a mes y cheque electrónico. Acción: Llamada humana de Customer Success ofreciendo migración a contrato anual + TechSupport bonificado + $20 de descuento por 6 meses."),
        ("Caso B: Fuga en Onboarding (p = 74.2% | Tenure 2m)", "Abandono temprano por falta de adopción digital. Acción: Flujo automatizado in-app guiando la configuración y soporte técnico asistido."),
        ("Caso C: VIP Blindado (p = 4.8% | MRR $108.20)", "Contrato de 2 años, débito automático y 4 escudos técnicos activos. Acción: PROHIBIDO ENVIAR DESCUENTOS. Evitamos canibalizar margen; solo fidelización orgánica.")
    ]
    for h, desc in cases11:
        p = tf11.add_paragraph()
        p.space_before = Pt(6)
        run_h = p.add_run()
        run_h.text = h + "\n"
        run_h.font.bold = True
        run_h.font.size = Pt(10.5)
        run_h.font.color.rgb = COLOR_ACCENT if "VIP en Riesgo" in h else (COLOR_EMERALD if "Blindado" in h else COLOR_CHARCOAL)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.size = Pt(10)
        run_d.font.color.rgb = COLOR_CHARCOAL
        
    s11.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 11 - Explicabilidad Local):\n"
        "Esta es la traducción operativa de la IA. Cuando un agente de Customer Success abre la pantalla del CRM, no ve un score vacío. "
        "Ve exactamente qué factores están empujando la probabilidad de fuga hacia arriba o hacia abajo. "
        "En el Caso A, ve que el riesgo viene por el cheque electrónico y la fibra desprotegida; la oferta que le hace por teléfono "
        "resuelve exactamente esos dos dolores. Y en el Caso C, el sistema bloquea los descuentos, impidiendo que el agente "
        "le regale dinero a un cliente fidelizado."
    )

    # =========================================================================
    # SLIDE 12: La Matriz Prescriptiva 2x2
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Estrategia de Retención Prescriptiva: Matriz de Recursos 2x2")
    
    img_path7 = os.path.join(ASSETS_DIR, "06_strategic_retention_matrix_2x2.png")
    if os.path.exists(img_path7):
        s12.shapes.add_picture(img_path7, Inches(0.8), Inches(1.6), width=Inches(7.0))
        
    tx12 = s12.shapes.add_textbox(Inches(8.1), Inches(1.6), Inches(4.4), Inches(5.2))
    tf12 = tx12.text_frame
    tf12.word_wrap = True
    
    p = tf12.paragraphs[0]
    p.text = "ASIGNACIÓN EFICIENTE DE CAPITAL:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    quads12 = [
        ("Q1: Rescate VIP (1,263 cuentas | $1.33M ARR)", "17.9% de clientes concentran el 79.5% de la pérdida. Inversión: $100/cuenta ($126.3K). Agente humano + descuento agresivo condicionado a permanencia."),
        ("Q2: Retención Digital (365 cuentas | $207K ARR)", "Inversión: $15/cuenta ($5.5K). Campaña Zero-Touch in-app con bono por pasar a débito automático."),
        ("Q3: Blindaje & Expansión (2,328 cuentas | $2.56M ARR)", "Inversión: $0. Prohibición de descuentos. Fidelización orgánica y venta cruzada."),
        ("Q4: Monitoreo Pasivo (3,087 cuentas | $1.38M ARR)", "Inversión: $0. Operación estándar sin fricción comercial.")
    ]
    for h, desc in quads12:
        p = tf12.add_paragraph()
        p.space_before = Pt(5)
        run_h = p.add_run()
        run_h.text = h + "\n"
        run_h.font.bold = True
        run_h.font.size = Pt(10)
        run_h.font.color.rgb = COLOR_ACCENT if "Q1" in h else (COLOR_EMERALD if "Q3" in h else COLOR_CHARCOAL)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.size = Pt(9.5)
        run_d.font.color.rgb = COLOR_CHARCOAL
        
    s12.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 12 - Matriz 2x2):\n"
        "Esta matriz es el producto final de gestión. Cruzamos el riesgo calibrado con el valor de la cuenta. "
        "Miren el Cuadrante Q1: apenas 1,263 cuentas (el 18% de la base) explican casi el 80% de todo el dinero que se fuga ($1.33M ARR). "
        "Aquí es donde colocamos a nuestro equipo humano de retención con un presupuesto de $100 por cliente. "
        "En Q2 usamos canales digitales automáticos de $15. "
        "Y en Q3 y Q4, que representan al 77% de los suscriptores, gastamos exactamente cero dólares, protegiendo $2.56M en ingresos sanos."
    )

    # =========================================================================
    # SLIDE 13: Plan de Implementación y Protocolo A/B
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Plan de Implementación, Protocolo A/B y Llamado a la Acción (Ask)")
    
    add_metric_card(s13, Inches(0.8), Inches(1.6), Inches(3.6), Inches(1.8), "8 Semanas", "Sprint de Despliegue", "Integración CRM y capacitación", COLOR_NAVY)
    add_metric_card(s13, Inches(4.8), Inches(1.6), Inches(3.6), Inches(1.8), "15% Holdout", "Grupo de Control Universal", "Medición de Incremental Uplift", COLOR_EMERALD)
    add_metric_card(s13, Inches(8.8), Inches(1.6), Inches(3.6), Inches(1.8), "$32,400 USD", "Presupuesto Piloto (Test)", "324 cuentas (Rollout total: $126.3k)", COLOR_ACCENT)
    
    tx13 = s13.shapes.add_textbox(Inches(0.8), Inches(3.8), Inches(11.7), Inches(3.2))
    tf13 = tx13.text_frame
    tf13.word_wrap = True
    
    p = tf13.paragraphs[0]
    p.text = "HOJA DE RUTA Y GOBERNANZA OPERATIVA:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    steps13 = [
        ("Semanas 1 y 2 (Integración Técnica):", " Automatización del pipeline de scoring semanal conectado a Salesforce / HubSpot con banderas de Cuadrante Q1 a Q4."),
        ("Semanas 3 y 4 (Habilitación Comercial):", " Capacitación de 2 agentes de Customer Success en la oferta estructurada de Q1 (5 llamadas diarias por agente)."),
        ("Semanas 5 a 8 (Validación Experimental A/B):", " Activación del grupo de control universal (15% sin intervención) para aislar la tasa de retención incremental neta y certificar ante Finanzas que las cuentas se salvaron gracias a la intervención."),
        ("Llamado a la Acción (Ask al Directorio):", " Aprobación de un presupuesto piloto de $32,400 USD para intervenir el tramo crítico de Q1 con una meta auditada de rescatar $47,500 en margen bruto neto de 12 meses.")
    ]
    for h, desc in steps13:
        p = tf13.add_paragraph()
        p.space_before = Pt(6)
        run_h = p.add_run()
        run_h.text = h
        run_h.font.bold = True
        run_h.font.size = Pt(11)
        run_h.font.color.rgb = COLOR_CHARCOAL
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.size = Pt(11)
        run_d.font.color.rgb = COLOR_CHARCOAL
        if "Llamado a la Acción" in h:
            run_h.font.color.rgb = COLOR_ACCENT
            run_d.font.bold = True
            
    s13.notes_slide.notes_text_frame.text = (
        "NOTAS DEL ORADOR (Slide 13 - Implementación y Cierre):\n"
        "Para cerrar, proponemos un plan de despliegue en 8 semanas con gobernanza estricta. "
        "No pedimos un cheque en blanco. Implementaremos un grupo de control del 15% para demostrar con evidencia causal que las cuentas "
        "se quedaron por la oferta y no por azar. "
        "Solicitamos la aprobación de $32,400 para ejecutar el piloto en el conjunto de prueba con una meta certificada de capturar "
        "$47,500 en margen de vida útil, pagándose a sí mismo en los primeros 90 días. Muchas gracias y quedo abierto a sus preguntas."
    )

    # Save presentation
    os.makedirs(os.path.dirname(OUTPUT_PPTX), exist_ok=True)
    prs.save(OUTPUT_PPTX)
    print(f"Presentation generated successfully at: {OUTPUT_PPTX}")

if __name__ == "__main__":
    create_presentation()
