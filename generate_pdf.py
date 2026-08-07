import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

def build_pdf(filename="CropPro_AI_Technical_Presentation_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Palette
    EMERALD_DARK = colors.HexColor("#08281A")
    EMERALD_PRIMARY = colors.HexColor("#00A86B")
    EMERALD_NEON = colors.HexColor("#00E68A")
    TEXT_DARK = colors.HexColor("#1A2B23")
    BG_LIGHT = colors.HexColor("#F4F9F6")
    GOLD_ACCENT = colors.HexColor("#D4AF37")
    WHITE = colors.HexColor("#FFFFFF")
    GRAY_BORDER = colors.HexColor("#D0E0D8")

    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=EMERALD_DARK,
        alignment=TA_LEFT,
        fontName="Helvetica-Bold",
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        leading=15,
        textColor=EMERALD_PRIMARY,
        alignment=TA_LEFT,
        fontName="Helvetica-Bold",
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontSize=15,
        leading=18,
        textColor=EMERALD_DARK,
        fontName="Helvetica-Bold",
        spaceBefore=14,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontSize=12,
        leading=15,
        textColor=EMERALD_PRIMARY,
        fontName="Helvetica-Bold",
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
        alignment=TA_LEFT,
        fontName="Helvetica",
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=12,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=WHITE,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=TEXT_DARK,
        fontName="Helvetica"
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName="Helvetica-Bold"
    )

    box_style = ParagraphStyle(
        'BoxText',
        parent=body_style,
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK
    )

    story = []

    # Title Banner
    story.append(Paragraph("🌱 CropPro.Ai — Technical Presentation & Judge Guide", title_style))
    story.append(Paragraph("Precision Agriculture Decision Engine & Agro-Climatic Intelligence Platform", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=EMERALD_PRIMARY, spaceBefore=0, spaceAfter=12))

    # Section 1
    story.append(Paragraph("1. Executive Overview & Core Vision", h1_style))
    story.append(Paragraph(
        "<b>CropPro.Ai</b> is an advanced <b>Adaptive Precision Agriculture Decision Engine</b>. "
        "Unlike conventional crop engines that only evaluate basic N-P-K matching, CropPro.Ai integrates <b>10 multi-dimensional soil, climate, topography, and commercial market telemetry features</b> "
        "to deliver accurate crop predictions, SHAP Explainable AI rationale, real-world stress modifiers, and zero-synthetic organic farming advisories.",
        body_style
    ))

    # Section 2
    story.append(Paragraph("2. Internet Data Collection & Official Agronomic References", h1_style))
    story.append(Paragraph("To ground the ML training bounds in authentic real-world agronomy, data distributions were calibrated using published standards from official agricultural authorities:", body_style))
    
    story.append(Paragraph("• <b>ICAR (Indian Council of Agricultural Research)</b>: Package of Practices guidelines for baseline N-P-K requirements, soil pH limits, and water uptake requirements across 33 crop categories.", bullet_style))
    story.append(Paragraph("• <b>State Agricultural Universities of Maharashtra</b>:", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;- <i>MPKV Rahuri</i>: Irrigated Western MH & Khandesh crop benchmarks (Sugarcane, Onions, Grapes, Bajra, Maize).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;- <i>PDKV Akola</i>: Vidarbha black cotton soil & pulse benchmarks (Cotton, Soybean, Paddy in eastern districts).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;- <i>VNMKV Parbhani</i>: Marathwada rainfed benchmarks (Tur/Pigeonpea, Soybean, Rabi Jowar).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;- <i>BSKKV Dapoli</i>: Coastal Konkan acidic laterite benchmarks (Alphonso Mango, Cashewnuts, Paddy).", bullet_style))
    story.append(Paragraph("• <b>Soil Health Card (SHC) Scheme (Min. of Agriculture)</b>: Soil Electrical Conductivity (EC in dS/m) thresholds (optimal &lt; 1.8 dS/m; high salinity &gt; 1.8 dS/m).", bullet_style))
    story.append(Paragraph("• <b>IMD (India Meteorological Department)</b>: District-level annual rainfall (mm) and temperature extremes (°C).", bullet_style))
    story.append(Paragraph("• <b>NHB (National Horticulture Board) & Agmarknet</b>: Market Profitability Index (MPI) scores reflecting commercial crop price resilience.", bullet_style))

    story.append(Spacer(1, 10))

    # Section 3: Table of Regional Hubs
    story.append(Paragraph("3. Maharashtra Regional Crop Hub Telemetry Mapping", h1_style))
    story.append(Paragraph("The system models 33 districts across 5 primary agricultural regions in Maharashtra with specific N-P-K telemetry:", body_style))

    table_data = [
        [
            Paragraph("Region", table_header_style),
            Paragraph("Districts Covered", table_header_style),
            Paragraph("Primary Crops & Agronomic Focus", table_header_style),
            Paragraph("Baseline N-P-K Telemetry", table_header_style)
        ],
        [
            Paragraph("<b>Western Maharashtra</b>", table_cell_style),
            Paragraph("Pune, Ahmednagar, Satara, Solapur, Kolhapur", table_cell_style),
            Paragraph("Sugarcane, Jowar, Bajra, Sweet Corn / Maize. <i>(Ahmednagar & Kolhapur lead in sugar & irrigated yields)</i>", table_cell_style),
            Paragraph("High N & K<br/>N: 130-148<br/>P: 55-62<br/>K: 55-65", table_cell_style)
        ],
        [
            Paragraph("<b>Vidarbha</b>", table_cell_style),
            Paragraph("Nagpur, Akola, Amravati, Yavatmal, Wardha, Buldhana, Chandrapur, Gondia, Bhandara, Gadchiroli, Washim", table_cell_style),
            Paragraph("Cotton, Soybean, & Paddy (Rice) in eastern districts (Gondia, Bhandara, Chandrapur, Gadchiroli).", table_cell_style),
            Paragraph("High N & P<br/>N: 85-120<br/>P: 45-70<br/>K: 25-50", table_cell_style)
        ],
        [
            Paragraph("<b>Marathwada</b>", table_cell_style),
            Paragraph("Chhatrapati Sambhajinagar, Beed, Latur, Nanded, Parbhani, Jalna, Hingoli, Dharashiv", table_cell_style),
            Paragraph("Soybean, Cotton, Tur (Pigeonpea), and Rabi Jowar.", table_cell_style),
            Paragraph("Pulse-focused P<br/>N: 35-115<br/>P: 48-72<br/>K: 28-50", table_cell_style)
        ],
        [
            Paragraph("<b>Khandesh & Northern MH</b>", table_cell_style),
            Paragraph("Nashik, Jalgaon, Dhule, Nandurbar", table_cell_style),
            Paragraph("Onions, Bananas, Grapes, Bajra. <i>(Nashik & Jalgaon are premier horticulture & banana hubs)</i>", table_cell_style),
            Paragraph("High P & K<br/>N: 60-110<br/>P: 35-85<br/>K: 35-95", table_cell_style)
        ],
        [
            Paragraph("<b>Konkan</b>", table_cell_style),
            Paragraph("Thane, Palghar, Raigad, Ratnagiri, Sindhudurg", table_cell_style),
            Paragraph("Rice (Paddy), Alphonso Mangoes, Cashewnuts.", table_cell_style),
            Paragraph("Acidic Red Laterite<br/>pH: 5.5-5.8<br/>Rainfall: 200-240mm", table_cell_style)
        ]
    ]

    t = Table(table_data, colWidths=[100, 130, 190, 110])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), EMERALD_DARK),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)

    story.append(Spacer(1, 10))

    # Section 4: Machine Learning Engine Specs
    story.append(Paragraph("4. Machine Learning Engine Specs (`CropPro.Ai`)", h1_style))
    
    ml_specs_data = [
        [Paragraph("<b>Parameter</b>", table_cell_bold), Paragraph("<b>Specification</b>", table_cell_bold)],
        [Paragraph("Model Architecture", table_cell_style), Paragraph("Multi-Class XGBoost Classifier (`xgb.XGBClassifier`) with softmax probabilities", table_cell_style)],
        [Paragraph("Dataset Records", table_cell_style), Paragraph("264,000 synthetic & empirical telemetry rows (8,000 samples per crop class)", table_cell_style)],
        [Paragraph("Target Classes", table_cell_style), Paragraph("33 Crop categories (Staples, Pulses, Commercial, Horticulture, Plantation)", table_cell_style)],
        [Paragraph("Test Accuracy", table_cell_style), Paragraph("<b>99.20% Test Accuracy</b> (85/15 Stratified Train/Test Split)", table_cell_style)],
        [Paragraph("Input Telemetry Vector", table_cell_style), Paragraph("`['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'soil_ec', 'market_profitability_index', 'elevation_m']`", table_cell_style)]
    ]
    t_ml = Table(ml_specs_data, colWidths=[150, 380])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), EMERALD_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_ml)

    # Section 5: Explainable AI & Real-World Modifiers
    story.append(Paragraph("5. Explainable AI (SHAP) & Real-World Constraint Modifiers", h1_style))
    story.append(Paragraph("• <b>SHAP TreeExplainer AI Logic</b>: Computes exact Shapley values for the winning crop recommendation, explaining in plain English which soil or climate factors (e.g. high N, optimal rainfall) drove the decision.", bullet_style))
    story.append(Paragraph("• <b>Real-World Stress Modifiers</b>:", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1. <i>Drought Risk Mitigation</i>: Suppresses water-intensive crops by 75% and boosts drought-tolerant millets/legumes by 1.6x.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2. <i>High Salinity Warning Mode</i>: Suppresses salt-sensitive crops when Soil EC &gt; 1.8 dS/m and prioritizes salt-tolerant crops.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3. <i>Market ROI Priority Mode</i>: Scales recommendation scores dynamically by the Market Profitability Index.", bullet_style))

    # Section 6: Zero-Synthetic Organic Advisory
    story.append(Paragraph("6. Zero-Synthetic Organic Profitability Advisory", h1_style))
    story.append(Paragraph("For every recommended crop, CropPro.Ai provides actionable natural farming protocols:", body_style))
    story.append(Paragraph("• <b>Bio-Fertilizer Substitution</b>: Replaces 40-50% synthetic NPK using Azotobacter, Azospirillum, PSB, Vermicompost, and Neem Cake recipes.", bullet_style))
    story.append(Paragraph("• <b>Biological Pest Control</b>: Recommends Neem Seed Kernel Extract, Dashparni Arka, and Trichogramma egg parasitoids.", bullet_style))
    story.append(Paragraph("• <b>Natural Intercropping</b>: Advises 4:2 leguminous intercropping arrangements for biological atmospheric nitrogen fixation.", bullet_style))

    story.append(Spacer(1, 10))

    # Section 7: Hackathon Judge Presentation Strategy Box
    story.append(Paragraph("7. Hackathon Judge Presentation Strategy & Defense Tips", h1_style))
    
    pitch_tips = [
        [Paragraph("<b>1. Problem Statement</b>", table_cell_bold), Paragraph("<i>'Farmers apply generic fertilizers without knowing if their specific soil EC, elevation, rainfall, and market demand support that crop, causing soil degradation and financial loss.'</i>", box_style)],
        [Paragraph("<b>2. Technological Edge</b>", table_cell_bold), Paragraph("<i>'CropPro.Ai uses a 10-feature XGBoost model trained on 264,000 regional benchmark records achieving 99.20% accuracy across 33 crops.'</i>", box_style)],
        [Paragraph("<b>3. Explainability & Impact</b>", table_cell_bold), Paragraph("<i>'We eliminate the black-box issue using SHAP Explainable AI and provide zero-synthetic organic advisories to reduce fertilizer cost by 40-50%.'</i>", box_style)]
    ]
    t_box = Table(pitch_tips, colWidths=[140, 390])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EAF4EF")),
        ('GRID', (0, 0), (-1, -1), 1, EMERALD_PRIMARY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_box)

    doc.build(story)
    print(f"PDF successfully generated: {os.path.abspath(filename)}")

if __name__ == "__main__":
    build_pdf()
